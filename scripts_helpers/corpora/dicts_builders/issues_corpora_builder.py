# -*- coding: utf-8 -*-
import os
import codecs
import scripts_helpers.corpora.helper as helper
from scripts_helpers.corpora.helper import Dictionary
from scripts_helpers.corpora.redmine_services_provider import RedmineServicesProvider
from scripts_helpers.corpora.config_loader import ConfigReader
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

    def generate_dicts(self):
        self.get_words()

    def get_words(self):

        query = "SELECT invested_time, subject FROM activities_by_issue where activity_id = "
        stop_words = WordHelper.get_stop_words()

        created_dicts_list = []
        times = self.get_total_services_time()

        for service in self.service_provider.get_services_as_tupples():

            service_name = service[RedmineServicesProvider.name_col]
            service_id = service[RedmineServicesProvider.id_col]

            if service_name in created_dicts_list:
                continue

            q = query

            print "analysing for " + service_name + 50*"-"

            ids = [str(i) for i in self.service_provider.get_all_ids_for_service(service_name)]

            if len(ids) > 1:
                q += " OR activity_id = ".join(ids)
            else:
                q += str(service_id)

            created_dicts_list.append(service_name)
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
                        w = WordHelper.clean_word(w)

                        if w in to_analyze:
                            to_analyze[w] += current_score
                            continue

                        if WordHelper.word_is_valid(w):
                            to_analyze[w] = current_score

            self.generate_weight_dictionary(service_name, to_analyze)

    def generate_weight_dictionary(self, service, words):
        df = open(self.dictionary.get_dict_service_file_name(service), "w+")

        for w in words:
            df.write(w + helper.results_field_separator + str(words[w]) + "\n")

        self.dictionary.generate_dictionary_size_file()

        df.close()

    @staticmethod
    def get_total_services_time():

        total_activity_time_query = "SELECT activity_id, activity, total FROM total_activity_time"
        cursor = helper.db.cursor()
        cursor.execute(total_activity_time_query)
        entries = cursor.fetchall()
        times = {}

        for entry in entries:
            times[entry[0]] = entry[2]

        return times

    def test(self, s):

        scores = {}
        s = s.lower()

        dict_weights = self.dictionary.get_dicts_weight()

        for service in self.service_provider.get_services_names():

            service_words = self.load_dict(service)

            if not service_words:
                print "no words for services " + service
                continue

            dict_weight = dict_weights[service]
            words = [WordHelper.clean_word(w) for w in s.split(" ") if WordHelper.word_is_valid(w)]
            score = 0

            for w in words:
                if w in service_words:
                    score += float(service_words[w])

            scores[service] = score * float(dict_weight)

        return scores

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














