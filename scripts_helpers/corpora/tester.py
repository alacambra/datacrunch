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
import cStringIO as cstr


class TestSet(multiprocessing.Process):

    def __init__(self, entries, permutations, pipe, ordinal, services_dicts):

        self.entries = entries
        self.permutations = permutations
        self.pipe = pipe
        self.ordinal = ordinal
        self.services_dicts = services_dicts

        super(TestSet, self).__init__()

    def is_successfull(self, result, expected):

        for i in range(0, 5):
            if result[i][0] == expected:
                return True

        return False

    def run(self):

        f = open("results/tmp/" + str(self._parent_pid) + "/" + str(self.ordinal) + ".tmp", "w+")

        service_id_col = 0
        service_name_col = 1
        comment_col = 2

        issue_weigth_col = 1
        activity_weight_col = 2

        results = {}
        s = cstr.StringIO()

        total = 0

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

                    s.write(entry[service_name_col])
                    s.write(helper.field_separator)
                    s.write(str(permutation[issue_weigth_col]))
                    s.write(helper.field_separator)
                    s.write(str(permutation[activity_weight_col]))
                    s.write(helper.field_separator)

                    if self.is_successfull(res, expected):
                        s.write("1\n")
                    else:
                        s.write("0\n")

                    total += 1

                    if total%10 == 0:
                        total = 0
                        self.pipe.send(10)

        f.write(s.getvalue())
        self.pipe.send(total)
        self.pipe.close()
        f.close()


class PrinterProcess(multiprocessing.Process):

    def __init__(self, total, pipes_counter, pipe_finish):

        self.pipes_counter = pipes_counter
        self.pipe_finish = pipe_finish
        self.total = total
        self.partial = 0

        super(PrinterProcess, self).__init__()

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
    print(s1)
    for s in s1:
        final[s] = issue_weigth*s1[s] + activity_weight*s2[s]

    return order_results(final)


def order_results(final):

    sorted_x = sorted(final.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_x


def compute():

    num_process = 8
    num_samples_per_activity = 10

    start_issue_weight = 1
    end_issue_weight = 10
    start_activity_weight = 1
    end_activity_weight = 10
    step = 3

    service_buffer = ServicesBuffer(num_samples_per_activity)

    permutations = {}
    os.mkdir("results/tmp/" + str(os.getpid()))

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
    ordinals = []
    test_set_list = TestSetList()
    printer_connections = []

    for perm in permutations.values():

        if i >= round(len(permutations) * j / num_process):

            printer_conn, subprocess_conn = Pipe()
            printer_connections.append(printer_conn)
            test_set_list.add_testset_and_start(assign_permutations(assign, service_buffer, ordianl, subprocess_conn))
            ordinals.append(ordianl)
            ordianl += 1
            j += 1
            assign = []

        assign.append(perm)
        i += 1

    printer_conn, subprocess_conn = Pipe()
    printer_connections.append(printer_conn)
    test_set_list.add_testset_and_start(assign_permutations(assign, service_buffer, ordianl, subprocess_conn))

    main_process_conn, printer_conn = Pipe()
    PrinterProcess(total_to_analyze, printer_connections, printer_conn).start()
    test_set_list.wait_for_test_ready()
    main_process_conn.send("ready")
    summarize_results(ordinals)


def summarize_results(ordinals):

    service_col = 0
    issue_weigth_col = 1
    activity_weight_col = 2
    result_col = 3
    rf = open(get_results_file_name(), "w+")
    results = {}

    for ordinal in ordinals:

        f = open("results/tmp/" + str(os.getpid()) + "/" + str(ordinal) + ".tmp", "r+")

        for line in f.readlines():
            line = line[:-1]
            line = line.split(helper.field_separator)

            if not line[service_col] in results:
                results[line[service_col]] = {}

            r = results[line[service_col]]

            if not line[issue_weigth_col] in r:
                r[line[issue_weigth_col]] = {}

            r = r[line[issue_weigth_col]]

            if not line[activity_weight_col] in r:
                r[line[activity_weight_col]] = []
                r[line[activity_weight_col]].append(0)
                r[line[activity_weight_col]].append(0)

            r = r[line[activity_weight_col]]
            r[0] += int(line[result_col])
            r[1] += 1

    for service in results:
        for p_iss_w in results[service]:
            for p_act_w in results[service][p_iss_w]:
                s = cstr.StringIO()
                s.write(service)
                s.write(helper.results_field_separator)
                s.write(p_iss_w)
                s.write(helper.results_field_separator)
                s.write(p_act_w)
                s.write(helper.results_field_separator)
                s.write(str(results[service][p_iss_w][p_act_w][1]))
                s.write(helper.results_field_separator)
                s.write(str(results[service][p_iss_w][p_act_w][0]))
                s.write("\n")
                rf.write(s.getvalue())
                s.close()

    rf.close()


def assign_permutations(permutations, service_buffer, ordinal, child_conn):
    return TestSet(
        service_buffer.get_entries().values(),
        permutations,
        child_conn,
        ordinal,
        service_buffer.get_services())


def get_results_file_name():
    now = datetime.datetime.now()
    return "results/results_" + str(os.getpid()) + "_-" + str(now.day) + "-" + str(now.month) + "-" \
           + str(now.year) + "_" + str(now.hour) + "_" + str(now.minute) + "-" + str(now.second) + ".dat"


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


def print_done(done, total):

    new = float(done*100) / float(total)
    sys.stdout.write("%3f%%\r" % new)
    sys.stdout.flush()

compute()


#service_buffer = ServicesBuffer(40)
#for a in individual_test("Neues HTML-Template erstellen", 1, 1000, service_buffer.get_services()):
#    print(a)














































































