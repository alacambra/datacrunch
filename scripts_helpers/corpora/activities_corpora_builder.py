# -*- coding: utf-8 -*-
import operator
from nltk import Text
from nltk.probability import FreqDist
import MySQLdb
import codecs
import os.path
import helper
from helper import Dictionary
import math

dictionary = Dictionary("from_comments")

def get_words():

    query = "SELECT comments FROM comments_with_activity where activity_id = "
    stop_words = helper.get_stop_words()
    services = helper.get_services()

    services_dict = {}

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
        txt = cursor.fetchall()
        to_analyze = []

        if len(txt) == 0:
            continue

        for text in txt:
            text = text[0]
            text = codecs.decode(text, "latin1").lower()
            text = codecs.encode(text, "unicode_escape")
            for w in text.split(" "):
                if w not in stop_words:
                    w = helper.clean_word(w)


                    if helper.word_is_valid(w):
                        to_analyze.append(w)

        services_dict[service] = to_analyze

    return services_dict


def generate_weight_dictionary(service, words):

    df = codecs.open(dictionary.get_dict_service_file_name(service), "w+", "utf8");

    services_dict = {}
    services_dict[service] = words

    t = Text(words)
    f = FreqDist(t)

    for w in f:
        weight = 100 * f.freq(w)
        df.write(codecs.decode(w, "unicode_escape") + helper.field_separator + str(weight) + "\n")


    df.close()


def generate_dicts():
    all = get_words()

    for service in all:
        generate_weight_dictionary(service.replace("/", "-").lower(), all[service])

    helper.generate_dictionary_size_file(dictionary)


def test(s, services):

    #services = helper.get_services()

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
                try:
                    score += float(service_words[w])
                except ValueError as e:
                    print service + ":" + w + ":" + service_words[w]
                    print e

        scores[service] = score * dict_weight_balance(float(dict_weight))

    return scores


def dict_weight_balance(raw_dict_weight):
    w = math.log(raw_dict_weight*100)
    return w


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



















































