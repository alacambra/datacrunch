# -*- coding: utf-8 -*-
import os
import helper
import codecs
from helper import Dictionary

dictionary = Dictionary("from_issues")


def generate_dicts():
    get_words()


def get_words():

    query = "SELECT invested_time, subject FROM activities_by_issue where activity_id = "
    stop_words = helper.get_stop_words()
    services = helper.get_services()

    services_dict = {}
    times = get_total_services_time()

    for service in services:
        if service in services_dict:
            continue

        q = query
        print "analysing for " + service + 50*"-"

        for s in services[service]:
            q = q + str(s.id) + " OR activity_id = "

        q = q[0:-len(" OR activity_id = ")]
        cursor = helper.db.cursor()
        cursor.execute(q)
        entries = cursor.fetchall()

        to_analyze = {}

        if len(entries) == 0:
            continue

        for entry in entries:

            current_score = entry[0] / times[service] * 100

            subject = entry[1]
            subject = codecs.decode(subject, "latin1").lower()
            subject = codecs.encode(subject, "unicode_escape")

            for w in subject.split(" "):
                if w not in stop_words:
                    w = helper.clean_word(w)

                    if w in to_analyze:
                        to_analyze[w] += current_score
                        continue

                    if helper.word_is_valid(w):
                        to_analyze[w] = current_score

        generate_weight_dictionary(service, to_analyze)


def generate_weight_dictionary(service, words):

    df = codecs.open(dictionary.get_dict_service_file_name(service), "w+", "utf8");
    helper.generate_dictionary_size_file(dictionary)

    for w in words:
        df.write(codecs.decode(w, "unicode_escape") + "\t" + str(words[w]) + "\n")

    df.close()


def get_total_services_time():

    total_activity_time_query = "SELECT * FROM total_activity_time"
    cursor = helper.db.cursor()
    cursor.execute(total_activity_time_query)
    entries = cursor.fetchall()
    times = {}

    for entry in entries:
        times[entry[1]] = entry[2]

    return times


def test(s):

    services = helper.get_services()
    scores = {}
    s = s.lower()

    dict_weights = dictionary.get_dicts_weight()

    for service in services:

        service_words = load_dict(service)

        if not service_words:
            continue

        dict_weight = dict_weights[service]
        words = [helper.clean_word(w) for w in s.split(" ") if helper.word_is_valid(w)]
        score = 0

        for w in words:
            if w in service_words:
                score += float(service_words[w])

        scores[service] = score * float(dict_weight)

    return scores


def load_dict(service_name):
    file_name = dictionary.get_dict_service_file_name(service_name)

    if not os.path.isfile(file_name):
        return False

    service_file = open(file_name, "r+")
    service_words = service_file.readlines()
    dict = {}

    for w in service_words:
        w = w.split("\t")
        dict[w[0]] = w[1][:-1]

    return dict


























































