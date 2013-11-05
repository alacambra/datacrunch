# -*- coding: utf-8 -*-
from __future__ import print_function
import operator
import datetime
import issues_corpora_builder as iss
import activities_corpora_builder as act
import helper
import random
import sys
import os
import multiprocessing
import time


class MultiQuery(multiprocessing.Process):

    def __init__(self, query, db, pipe):
        self.query = query
        self.db = db
        self.pipe = pipe
        super(MultiQuery, self).__init__()

    def run(self):
        cur = self.db.cursor()
        q = cur.execute(self.query)
        self.pipe.send(cur.fetchall())
        self.pipe.close()


class ServicesBuffer:

    def __init__(self, act_id, num_samples_per_activity):

        self.services = {}
        for service_id in helper.get_services_ids():
            self.services[service_id] = False

        self.act_id = act_id
        self.num_samples_per_activity = num_samples_per_activity

    def get_entries_for_service(self, service_id):

        if service_id in self.services:
            return self.services[service_id]

        else:
            entries = get_entries(self.act_id, self.num_samples_per_activity)


def individual_test(to_test, issue_weigth, activity_weight):

    s1 = iss.test(to_test)
    s2 = act.test(to_test)
    final = {}

    for s in s1:
        final[s] = issue_weigth*s1[s] + activity_weight*s2[s]

    return order_results(final)


def order_results(final):

    sorted_x = sorted(final.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_x

    #for x in sorted_x:
    #    print(x)


def compute():

    num_process = 8
    num_samples_per_activity = 1000
    helper.get_services()
    services_ids = helper.get_services_ids()

    start_issue_weight = 1
    end_issue_weight = 20
    start_activity_weight = 1
    end_activity_weight = 20
    step = 1

    total_to_analyze_per_process = num_samples_per_activity * len(services_ids) * (end_activity_weight / step) \
        * (end_activity_weight / step) / num_process

    print(total_to_analyze_per_process)
    permutations = {}

    for issue_weigth in range(start_issue_weight, end_issue_weight+1, step):
        for activity_weight in range(start_activity_weight, end_activity_weight+1, step):

            proportion = round(float(activity_weight) / float(issue_weigth), 2)

            if proportion in permutations:
                continue

            permutations[proportion] = (proportion, activity_weight, issue_weigth)

    assign = []

    i = 0
    j = 1
    for perm in permutations.values():

        if i >= round(len(permutations) * j / num_process):

            assign_permutations(assign)
            j += 1
            assign = []

        assign.append(perm)

        i += 1

    assign_permutations(assign)


def assign_permutations(permutations):
    print(permutations)
    print("-"*85)


def full_test():

    num_samples_per_activity = 2
    helper.get_services()
    services_ids = helper.get_services_ids()

    start_issue_weight = 1
    end_issue_weight = 20
    start_activity_weight = 1
    end_activity_weight = 20
    step = 5

    fn = get_results_file_name()
    if os.path.isfile(fn):
        raise Exception("File already exists: " + fn)

    f = open(fn, "w+")
    done = 1

    total_to_analyze = num_samples_per_activity * (end_activity_weight / step) * (end_activity_weight / step) * len(services_ids)

    for act_id in services_ids:
        proportions = []
        entries = get_entries(act_id, num_samples_per_activity)

        if len(entries) < num_samples_per_activity:
            total_to_analyze -= (num_samples_per_activity - len(entries)) * (end_activity_weight / step) * (end_activity_weight / step)

        uid = time.time()
        for issue_weigth in range(start_issue_weight, end_issue_weight+1, step):
            for activity_weight in range(start_activity_weight, end_activity_weight+1, step):

                print_done(done, total_to_analyze)

                if activity_weight == 0 and start_activity_weight == 0:
                    continue

                proportion = float(activity_weight) / float(issue_weigth)
                if proportion in proportions:
                    continue

                proportions.append(proportion)

                results = {}

                total = 0
                correct = 0
                false = 0

                if len(entries) == 0:
                    done += 1
                    continue

                for entry in entries:

                    comments = entry[2]
                    expected = entry[1]

                    if not expected in results:
                        results[expected] = [0, 0, 0]

                    res = individual_test(comments, issue_weigth, activity_weight)

                    if res[0][0] == expected:
                        correct += 1
                        results[expected][0] += 1
                    else:
                        results[expected][1] += 1
                        false += 1

                    results[expected][2] += 1
                    total += 1

                    done += 1

                for r in results.items():
                    f.write(str(proportion) + ":" + str(issue_weigth) + ":" + str(activity_weight)
                            + str(r[1]) + ":" + str(r[0]) + "\n")

    f.close()


def get_results_file_name():
    now = datetime.datetime.now()
    return "resources/results-" + str(now.day) + "-" + str(now.month) + "-" \
           + str(now.year) + "-" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second) + ".dat"


def get_entries(activity_id, num_samples_per_activity):
    random_ids = get_random_id(num_samples_per_activity, activity_id)

    if not random_ids:
        return False

    query = "select e.id AS activity_id, e.name AS activity_name, te.comments AS comments " \
            "from(redmine.time_entries te join redmine.enumerations e ON ((te.activity_id = e.id)))"

    query += " WHERE (" + random_ids + ") and activity_id=" + str(activity_id) +\
             " order by te.id limit " + str(num_samples_per_activity)

    cursor = helper.db.cursor()
    cursor.execute(query)
    entries = cursor.fetchall()

    return entries


def print_done(done, total):

    new = float(done*100) / float(total)
    sys.stdout.write("%3f%%\r" % new)
    sys.stdout.flush()


def get_random_id(max, service_id):

    q = "SELECT id  " \
        "FROM redmine.time_entries as te " \
        "where te.activity_id=" + str(service_id)

    cursor = helper.db.cursor()

    try:
        cursor.execute(q)
    except Exception as e:
        print(e)
        print(q)
        return False

    result = cursor.fetchall()

    all_ids = []

    for id in result:
        all_ids.append(id[0])

    random.shuffle(all_ids)

    if len(all_ids) == 0:
        return False

    if len(all_ids) < max:
        max = len(all_ids)

    selected = []

    rep = 0
    if max > 1:

        for i in range(0, max):

            selected.append(str(all_ids[i]))

        s = " OR te.id=".join(selected)
        s = "te.id=" + s

    else:
        s = "te.id=" + str(all_ids[0])

    return s

#full_test()
compute()



















































































