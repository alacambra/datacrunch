# -*- coding: utf-8 -*-
import operator
from nltk import Text
from nltk.probability import FreqDist
import MySQLdb
import codecs
import os.path
import helper

db = MySQLdb.connect(
        host="marceli",
        user="root",
        passwd="root",
        db="redmine")


def get_words():

    query = "SELECT comments FROM comments_with_activity where activity_id = "
    stop_words = helper.get_stop_words()
    services = helper.get_services().values()

    services_dict = {}

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
        txt = cursor.fetchall()
        to_analyze = []

        if len(txt) == 0:
            continue

        for text in txt:
            text = text[0]
            #try:
            text = codecs.decode(text, "latin1").lower()
            text = codecs.encode(text, "unicode_escape")

            for w in text.split(" "):
                if w not in stop_words:
                    w = helper.clean_word(w)

                    if helper.word_is_valid(w):
                        to_analyze.append(w)

        services_dict[service[0].name] = to_analyze

    return services_dict


def generate_weight_dictionary(service, words):

    df = codecs.open(get_dict_service_file_name(service), "w+", "utf8");

    services_dict = {}
    services_dict[service] = words

    t = Text(words)
    f = FreqDist(t)

    for w in f:
        weight = 100 * f.freq(w)
        df.write(codecs.decode(w, "unicode_escape") + "\t" + str(weight) + "\n")


    df.close()


def generate_dicts():
    all = get_words()

    for service in all:
        generate_weight_dictionary(service.replace("/", "-").lower(), all[service])


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
                try:
                    score += float(service_words[w])
                except ValueError as e:
                    print service + ":" + w + ":" + service_words[w]
                    print e

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
    return "dicts/from_comments/"

#generate_dicts()
#test("November-TAGs erstellt, getestet und übergeben")


























































