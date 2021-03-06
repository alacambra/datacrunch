# -*- coding: utf-8 -*-
from __future__ import print_function
import operator
import datetime
import random
import sys
import os
import multiprocessing
from multiprocessing import Pipe
import cStringIO as cstr
import scripts_helpers.corpora.helper as helper
from scripts_helpers.corpora.dicts_builders.issues_corpora_builder import Builder as IssueCorporaBuilder
from scripts_helpers.corpora.dicts_builders.activities_corpora_builder import Builder as ActivityCorporaBuilder
from scripts_helpers.corpora.redmine_services_provider import RedmineServicesProvider
from scripts_helpers.corpora.config_loader import ConfigReader
from scripts_helpers.corpora.helper import Dictionary
from scripts_helpers.corpora.results_reader import ResultsReader


class EntriesTestSet(multiprocessing.Process):

    def __init__(self, config_reader, service_buffer, permutations, pipe, ordinal):
        """
        @type config_reader: ConfigReader
        @type services_entries: dict
        @type permutations: list
        @type pipe: multiprocessing.connection
        @type: int
        @type services_names: dict
        """

        self.services_entries = service_buffer.get_entries_tupples()
        self.permutations = permutations
        self.pipe = pipe
        self.ordinal = ordinal
        self.services_names = service_buffer.services_provider.get_services_as_dict()
        self.config_reader = config_reader
        self.service_provider = service_buffer.services_provider
        super(EntriesTestSet, self).__init__()

    def is_successfull(self, result, expected):

        for i in range(0, self.config_reader.get_int_property("consider_valid_range")):
            if result[i][0] == expected:
                return True

        return False

    def run(self):

        f = open(self.config_reader.get_property("tmp_dir") + str(self._parent_pid) + "/" + str(self.ordinal) + ".tmp", "w+")

        issue_weigth_col = 1
        activity_weight_col = 2

        s = cstr.StringIO()

        total = 0

        for permutation in self.permutations:

            total = 0

            for services_entry in self.services_entries.items():
                service_id = services_entry[0]
                service_name = self.services_names[service_id]
                for service_entry in services_entry[1]:

                    res = individual_test(
                        service_entry,
                        permutation[issue_weigth_col],
                        permutation[activity_weight_col],
                        self.config_reader,
                        self.service_provider
                    )

                    expected = service_name

                    s.write(service_name)
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

    def __init__(self, num_samples_per_activity, services_provider):
        """
         @type services_provider: RedmineServicesProvider
        """
        self.services_provider = services_provider
        self.services_entries_tupples = {}
        self.num_samples_per_activity = num_samples_per_activity
        self.load_all_entries()

    def load_all_entries(self):
        for service_id in self.services_provider.get_services_ids():
            self.get_entries(service_id)

    def get_entries_tupples(self):
        return self.services_entries_tupples

    def get_total_entries(self):

        total = 0
        for i in self.services_entries_tupples.values():
            total += len(i)

        return total

    def get_entries(self, activity_id):
        random_ids = get_random_id(self.num_samples_per_activity, activity_id)

        if not random_ids:
            return False

        query = "select te.comments AS comments " \
                "from(redmine.time_entries te join redmine.enumerations e ON ((te.activity_id = e.id)))"

        query += " WHERE (" + random_ids + ") and activity_id=" + str(activity_id) + \
                 " order by te.id limit " + str(self.num_samples_per_activity)

        cursor = helper.db.cursor()
        cursor.execute(query)
        entries = cursor.fetchall()

        self.services_entries_tupples[activity_id] = [service_entry[0] for service_entry in entries]


class TestSetList:

    def __init__(self):
        self.testSets = []

    def add_testset_and_start(self, testSet):
        testSet.start()
        self.testSets.append(testSet)

    def wait_for_test_ready(self):
        for test in self.testSets:
            test.join()


def individual_test(to_test, issue_weigth, activity_weight, config_reader, service_provider):

    activity_dictionary = Dictionary(config_reader, "from_comments", service_provider)
    issue_dictionary = Dictionary(config_reader, "from_issues", service_provider)
    iss = IssueCorporaBuilder(config_reader, service_provider, issue_dictionary)
    act = ActivityCorporaBuilder(config_reader, service_provider, activity_dictionary)

    services_issues_res = iss.test(to_test)
    services_activity_res = act.test(to_test)
    final = {}
    for service in services_issues_res:
        final[service] = issue_weigth*services_issues_res[service] + activity_weight*services_activity_res[service]

    return order_results(final)


def order_results(final):

    sorted_x = sorted(final.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_x


def compute(config_reader):
    """
    @type config_reader: ConfigReader
    """
    print("Starting:" + str(os.getpid()))

    num_process = config_reader.get_int_property("num_process")
    num_samples_per_activity = config_reader.get_int_property("num_samples_per_activity")

    start_issue_weight = config_reader.get_int_property("start_issue_weight")
    end_issue_weight = config_reader.get_int_property("end_issue_weight")
    start_activity_weight = config_reader.get_int_property("start_activity_weight")
    end_activity_weight = config_reader.get_int_property("end_activity_weight")
    step = config_reader.get_int_property("step")

    service_provider = RedmineServicesProvider()

    service_buffer = ServicesBuffer(num_samples_per_activity, service_provider)

    permutations = {}
    os.mkdir(config_reader.get_property("tmp_dir") + str(os.getpid()))

    for issue_weigth in range(start_issue_weight, end_issue_weight+1, step):
        for activity_weight in range(start_activity_weight, end_activity_weight+1, step):

            proportion = round(float(activity_weight) / float(issue_weigth), 2)

            if proportion in permutations:
                continue

            permutations[proportion] = (proportion, issue_weigth, activity_weight)

    total_to_analyze = service_buffer.get_total_entries() * len(permutations)
    assigned_premutations = []
    i = 0
    j = 1
    ordinal = 0
    ordinals = []
    test_set_list = TestSetList()
    printer_connections = []

    for permutation in permutations.values():

        if i >= round(len(permutations) * j / num_process):

            printer_conn, subprocess_conn = Pipe()
            printer_connections.append(printer_conn)

            test_set_list.add_testset_and_start(
                assign_permutations(
                    config_reader, assigned_premutations, service_buffer, ordinal, subprocess_conn))

            ordinals.append(ordinal)
            ordinal += 1
            j += 1
            assigned_premutations = []

        assigned_premutations.append(permutation)
        i += 1

    printer_conn, subprocess_conn = Pipe()
    printer_connections.append(printer_conn)

    ordinals.append(ordinal)
    test_set_list.add_testset_and_start(
        assign_permutations(
            config_reader, assigned_premutations, service_buffer, ordinal, subprocess_conn))

    main_process_conn, printer_conn = Pipe()
    PrinterProcess(total_to_analyze, printer_connections, printer_conn).start()
    test_set_list.wait_for_test_ready()
    main_process_conn.send("stop")
    summarize_results(config_reader, ordinals)


def summarize_results(config_reader, ordinals):
    """
    @type config_reader: ConfigReader
    """

    service_col = 0
    issue_weigth_col = 1
    activity_weight_col = 2
    result_col = 3
    results_file_name = get_results_file_name(config_reader)
    rf = open(results_file_name, "w+")
    results = {}

    for ordinal in ordinals:

        f = open(config_reader.get_property("tmp_dir") + str(os.getpid()) + "/" + str(ordinal) + ".tmp", "r+")

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

    ResultsReader(results_file_name)


def assign_permutations(config_reader, assigned_premutations, service_buffer, ordinal, child_conn):
    """
    @type service_buffer: ServicesBuffer
    @type config_reader: ConfigReader
    @type service_provider: RedmineServicesProvider
    """

    return EntriesTestSet(
        config_reader,
        service_buffer,
        assigned_premutations,
        child_conn,
        ordinal
    )


def get_results_file_name(config_reader):
    now = datetime.datetime.now()
    return config_reader.get_property("results_dir") + "results_" + str(os.getpid()) + "_-" + str(now.day) + "-" + str(now.month) + "-" \
           + str(now.year) + "_" + str(now.hour) + "_" + str(now.minute) + "-" + str(now.second) + ".dat"

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


if __name__ == "__main__":
    os.chdir(sys.path[0])
    if len(sys.argv) == 1:
        conf_file = "../../resources/config.cfg"
    else:
        conf_file = sys.argv[1]

    compute(ConfigReader(conf_file))













































