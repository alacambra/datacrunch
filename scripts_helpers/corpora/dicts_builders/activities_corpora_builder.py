# -*- coding: utf-8 -*-
from nltk import Text
from nltk.probability import FreqDist
import codecs
import os.path
import scripts_helpers.corpora.helper as helper
from scripts_helpers.corpora.helper import Dictionary
import math
from scripts_helpers.corpora.redmine_services_provider import RedmineServicesProvider
from scripts_helpers.corpora.config_loader import ConfigReader
import sys
from scripts_helpers.corpora.helper import WordHelper


class Builder:

    def __init__(self, config_reader, service_provider, dictionary):
        """
        @type config_reader: ConfigReader
        @type service_provider:RedmineServicesProvider
        @type dictionary:Dictionary
        """
        self.config_reader = config_reader
        self.service_provider = service_provider
        self.dictionary = dictionary

    def get_words(self):

        query = "SELECT comments FROM comments_with_activity where activity_id = "

        stop_words = WordHelper.get_stop_words()

        services_dict = {}

        for service in self.service_provider.get_services_as_tupples():

            service_name = service[RedmineServicesProvider.name_col]
            service_id = service[RedmineServicesProvider.id_col]

            q = query
            print "analysing for " + service_name + 50*"-"

            q += str(service_id)
            cursor = helper.db.cursor()

            cursor.execute(q)
            txt = cursor.fetchall()
            to_analyze = []

            if len(txt) == 0:
                continue

            for text in txt:
                text = text[0]
                text = codecs.decode(text, "latin1").lower()
                text = codecs.encode(text, "utf8")
                for w in text.split(" "):
                    if w not in stop_words:
                        w = WordHelper.clean_word(w)

                        if WordHelper.word_is_valid(w):
                            to_analyze.append(w)

            if service_name in services_dict:
                services_dict[service_name] += to_analyze
            else:
                services_dict[service_name] = to_analyze

        return services_dict

    def generate_weight_dictionary(self, service, words):

        df = open(self.dictionary.get_dict_service_file_name(service), "w+")

        t = Text(words)
        freq_dist = FreqDist(t)

        for w in freq_dist:
            weight = 100 * freq_dist.freq(w)
            df.write(w + helper.results_field_separator + str(weight) + "\n")

        df.close()

    def generate_dicts(self):

        all_services_words = self.get_words()

        for service in all_services_words:
            self.generate_weight_dictionary(service.replace("/", "-").lower(), all_services_words[service])

        self.dictionary.generate_dictionary_size_file()

    def test(self, s):

        scores = {}
        s = s.lower()
        dict_weights = self.dictionary.get_dicts_weight()

        for service in self.service_provider.get_services_names():

            service_words = self.load_dict(service)
            if not service_words:
                continue

            dict_weight = dict_weights[service]
            words = [WordHelper.clean_word(w) for w in s.split(" ") if WordHelper.word_is_valid(w)]

            score = 0

            for w in words:
                if w in service_words:
                    try:
                        score += float(service_words[w])
                    except ValueError as e:
                        print service + ":" + w + ":" + service_words[w]
                        print e

            scores[service] = score * Builder.dict_weight_balance(float(dict_weight))

        return scores

    @staticmethod
    def dict_weight_balance(raw_dict_weight):
        w = math.log(raw_dict_weight*100)
        return w

    def load_dict(self, service_name):
        file_name = self.dictionary.get_dict_service_file_name(service_name)

        if not os.path.isfile(file_name):
            return False

        service_file = open(file_name, "r+")
        service_words = service_file.readlines()
        dict = {}

        for w in service_words:
            w = w.split(helper.results_field_separator)
            dict[w[0]] = w[1][:-1]

        return dict


































