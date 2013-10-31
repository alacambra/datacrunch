# -*- coding: utf-8 -*-
import os
import MySQLdb
import helper
import codecs
import operator

db = MySQLdb.connect(
        host="marceli",
        user="root",
        passwd="root",
        db="redmine")


def get_words():

    query = "SELECT invested_time, subject FROM activities_by_issue where activity_id = "
    stop_words = helper.get_stop_words()
    services = helper.get_services().values()

    services_dict = {}
    times = get_total_services_time()

    for service in services:
        if service[0].name in services_dict:
            continue

        q = query
        print "analysing for " + service[0].name + 50*"-"

        for s in service:
            q = q + str(s.id) + " OR activity_id = "

        q = q[0:-len(" OR activity_id = ")]
        cursor = db.cursor()
        cursor.execute(q)
        entries = cursor.fetchall()

        to_analyze = {}

        if len(entries) == 0:
            continue

        for entry in entries:

            current_score = entry[0] / times[service[0].name] * 100

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

        generate_weight_dictionary(service[0].name, to_analyze)


def generate_weight_dictionary(service, words):

    df = codecs.open(get_dict_service_file_name(service), "w+", "utf8");

    for w in words:
        df.write(codecs.decode(w, "unicode_escape") + "\t" + str(words[w]) + "\n")

    df.close()


def get_total_services_time():

    total_activity_time_query = "SELECT * FROM total_activity_time"
    cursor = db.cursor()
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
    for service in services:

        service_words = load_dict(service)

        if not service_words:
            continue

        words = [helper.clean_word(w) for w in s.split(" ") if helper.word_is_valid(w)]

        score = 0

        for w in words:
            if w in service_words:
                score += float(service_words[w])

        scores[service] = score

    return scores

    #sorted_x = sorted(scores.iteritems(), key=operator.itemgetter(1), reverse=True)
    #
    #for x in sorted_x:
    #    print x


def load_dict(service_name):
    file_name = get_dict_service_file_name(service_name)

    if not os.path.isfile(file_name):
        return False

    service_file = open(file_name, "r+")
    service_words = service_file.readlines()
    dict = {}

    for w in service_words:
        w = w.split("\t")
        dict[w[0]] = w[1][:-1]

    return dict


def get_dict_service_file_name(service):
    return get_dict_directory()+ service.replace("/", "-").lower() + ".dict"


def get_dict_directory():
    return "dicts/from_issues/"

#get_words()
#test("November-TAGs erstellt, getestet und übergeben")



























































