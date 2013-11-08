# -*- coding: utf-8 -*-
import os
import codecs
import scripts_helpers.corpora.helper as helper
from scripts_helpers.corpora.helper import Dictionary
from scripts_helpers.corpora.redmine_services_provider import RedmineServicesProvider


dictionary = Dictionary("from_issues")
service_provider = RedmineServicesProvider()

def generate_dicts():
    get_words()


def get_words():

    query = "SELECT invested_time, subject FROM activities_by_issue where activity_id = "
    stop_words = helper.get_stop_words()

    services = service_provider.get_services_as_tupples()

    services_dict = {}
    times = get_total_services_time()

    for service in services:

        service_name = service[RedmineServicesProvider.name_col]
        service_id = service[RedmineServicesProvider.id_col]

        if service_name in services_dict:
            continue

        q = query

        print "analysing for " + service_name + 50*"-"

        ids = [str(i) for i in service_provider.get_all_ids_for_service(service_name)]

        if len(ids) > 1:
            q += " OR activity_id = ".join(ids)
        else:
            q += str(service_id)

        cursor = helper.db.cursor()
        cursor.execute(q)
        entries = cursor.fetchall()

        to_analyze = {}

        if len(entries) == 0:
            continue

        for entry in entries:

            #the query view already groups the activity by name and not by id
            if service_id not in times:
                continue

            current_score = entry[0] / times[service_id] * 100

            subject = entry[1]
            subject = codecs.decode(subject, "latin1").lower()
            subject = codecs.encode(subject, "utf8")

            for w in subject.split(" "):
                if w not in stop_words:
                    w = helper.clean_word(w)

                    if w in to_analyze:
                        to_analyze[w] += current_score
                        continue

                    if helper.word_is_valid(w):
                        to_analyze[w] = current_score

        generate_weight_dictionary(service_name, to_analyze)


def generate_weight_dictionary(service, words):

    #df = codecs.open(dictionary.get_dict_service_file_name(service), "w+", "utf8");
    df = open(dictionary.get_dict_service_file_name(service), "w+")

    for w in words:
        #df.write(codecs.decode(w, "unicode_escape") + helper.field_separator + str(words[w]) + "\n")
        df.write(w + helper.field_separator + str(words[w]) + "\n")

    helper.generate_dictionary_size_file(dictionary)

    df.close()


def get_total_services_time():

    total_activity_time_query = "SELECT activity_id, activity, total FROM total_activity_time"
    cursor = helper.db.cursor()
    cursor.execute(total_activity_time_query)
    entries = cursor.fetchall()
    times = {}

    for entry in entries:
        times[entry[0]] = entry[2]

    return times


def test(s, services):

    scores = {}
    s = s.lower()

    dict_weights = dictionary.get_dicts_weight()

    for service in services:

        service_words = load_dict(service)

        if not service_words:
            print "no words for services " + service
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
        w = w.split(helper.field_separator)
        dict[w[0]] = w[1][:-1]

    return dict

generate_dicts()


















































