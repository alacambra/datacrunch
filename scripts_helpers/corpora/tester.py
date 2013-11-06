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
from multiprocessing import Pipe


class TestSet(multiprocessing.Process):

    def __init__(self, entries, permutations, pipe, ordinal, services_dicts):

        self.entries = entries
        self.permutations = permutations
        self.pipe = pipe
        self.ordinal = ordinal
        self.services_dicts = services_dicts

        super(TestSet, self).__init__()

    def run(self):

        f = open("tmp/" + str(self._parent_pid) + "/" + str(self.ordinal) + ".tmp", "w+")

        service_id_col = 0
        service_name_col = 1
        comment_col = 2

        issue_weigth_col = 1
        activity_weight_col = 2

        results = {}

        for permutation in self.permutations:

            correct = 0
            false = 0
            total = 0

            for services_entry in self.entries:
                for entry in services_entry:

                    res = individual_test(
                        entry[comment_col],
                        permutation[issue_weigth_col],
                        permutation[activity_weight_col],
                        self.services_dicts)

                    expected = entry[service_name_col]

                    s = entry[service_name_col] + helper.field_separator + str(permutation[issue_weigth_col]) + \
                        helper.field_separator + str(permutation[activity_weight_col]) + helper.field_separator

                    if res[0][0] == expected:
                        f.write(s + "1" + "\n")
                    else:
                        f.write(s + "0" + "\n")

                    total += 1

                    if total%10 == 0:
                        total = 0
                        self.pipe.send(10)

        self.pipe.send(total)
        self.pipe.close()
        f.close()

class PrinerProcess(multiprocessing.Process):

    def __init__(self, total, pipes_counter, pipe_finish):

        self.pipes_counter = pipes_counter
        self.pipe_finish = pipe_finish
        self.total = total
        self.partial = 0

        super(PrinerProcess, self).__init__()

    def run(self):
        while not self.pipe_finish.poll(0.1):
            for pipe in self.pipes_counter:
                if pipe.poll(0.2):
                    new_part = pipe.recv()
                    self.partial += new_part
                    print_done(self.partial, self.total)

        for pipe in self.pipes_counter:
            if pipe.poll():
                new_part = pipe.recv()
                self.partial += new_part
                print_done(self.partial, self.total)


class ServicesBuffer:

    def __init__(self, num_samples_per_activity):

        self.services = {}
        for service_id in helper.get_services_ids():
            self.services[service_id] = False

        self.num_samples_per_activity = num_samples_per_activity
        self.services_names = []
        self.load_all_entries()

    def load_all_entries(self):
        ids = helper.get_services_ids()

        for service_id in ids:

            self.services[service_id] = get_entries(service_id, self.num_samples_per_activity)
            service_name = self.services[service_id][0][1]

            if service_name not in self.services_names:
                self.services_names.append(service_name)

    def get_entries_for_service(self, service_id):

        if service_id in self.services:
            return self.services[service_id]

        else:
            entries = get_entries(service_id, self.num_samples_per_activity)
            self.services[service_id] = entries
            return self.entries

    def get_entries(self):
        return self.services

    def get_total_entries(self):

        total = 0
        for i in self.services.values():
            total += len(i)

        return total

    def get_services(self):
        return self.services_names


class TestSetList:

    def __init__(self):
        self.testSets = []

    def add_testset_and_start(self, testSet):
        testSet.start()
        self.testSets.append(testSet)

    def wait_for_test_ready(self):
        for test in self.testSets:
            test.join()


def individual_test(to_test, issue_weigth, activity_weight, services_dicts):

    s1 = iss.test(to_test, services_dicts)
    s2 = act.test(to_test, services_dicts)
    final = {}

    for s in s1:
        final[s] = issue_weigth*s1[s] + activity_weight*s2[s]

    return order_results(final)


def order_results(final):

    sorted_x = sorted(final.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_x


def compute():

    num_process = 8
    num_samples_per_activity = 100

    start_issue_weight = 1
    end_issue_weight = 20
    start_activity_weight = 1
    end_activity_weight = 20
    step = 4

    service_buffer = ServicesBuffer(num_samples_per_activity)

    permutations = {}
    os.mkdir("tmp/" + str(os.getpid()))

    for issue_weigth in range(start_issue_weight, end_issue_weight+1, step):
        for activity_weight in range(start_activity_weight, end_activity_weight+1, step):

            proportion = round(float(activity_weight) / float(issue_weigth), 2)

            if proportion in permutations:
                continue

            permutations[proportion] = (proportion, activity_weight, issue_weigth)

    total_to_analyze = service_buffer.get_total_entries() * len(permutations)

    assign = []

    i = 0
    j = 1
    ordianl = 0
    test_set_list = TestSetList()
    printer_connections = []

    for perm in permutations.values():

        if i >= round(len(permutations) * j / num_process):

            printer_conn, subprocess_conn = Pipe()
            printer_connections.append(printer_conn)
            test_set_list.add_testset_and_start(assign_permutations(assign, service_buffer, ordianl, subprocess_conn))
            ordianl += 1
            j += 1
            assign = []

        assign.append(perm)
        i += 1

    printer_conn, subprocess_conn = Pipe()
    printer_connections.append(printer_conn)
    test_set_list.add_testset_and_start(assign_permutations(assign, service_buffer, ordianl, subprocess_conn))

    main_process_conn, printer_conn = Pipe()
    PrinerProcess(total_to_analyze, printer_connections, printer_conn).start()
    test_set_list.wait_for_test_ready()
    main_process_conn.send("ready")
    print("ready")


def assign_permutations(permutations, service_buffer, ordinal, child_conn):
    return TestSet(
        service_buffer.get_entries().values(),
        permutations,
        child_conn,
        ordinal,
        service_buffer.get_services())


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

compute()



















































































