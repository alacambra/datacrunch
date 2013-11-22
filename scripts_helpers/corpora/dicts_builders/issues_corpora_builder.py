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
        self.services_groups = {}
        self.load_services_groups()

    def generate_dicts(self):
        self.get_words()

    def get_words(self, query="SELECT invested_time, subject FROM activities_by_issue where activity_id = "):

        stop_words = WordHelper.get_stop_words()

        created_dicts_list = []
        times = self.get_total_services_time()

        for service in self.service_provider.get_services_as_tupples():

            service_name = service[RedmineServicesProvider.name_col]
            service_id = service[RedmineServicesProvider.id_col]

            if service_name in created_dicts_list or service_name == "not_used":
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

    def load_services_groups(self):

        self.services_groups["design"] = "design"
        self.services_groups["konzeption (inhaltlich)"] = "not_used"
        self.services_groups["besprechung (intern)"] = "not_used"
        self.services_groups["projektmanagement"] = "projektmanagement"
        self.services_groups["testing"] = "testing"
        self.services_groups["contentpflege"] = "html-_css-umsetzung"
        self.services_groups["deployment"] = "server administration"
        self.services_groups["medienerzeugung"] = "design"
        self.services_groups["recherche"] = "not_used"
        self.services_groups["schulung (extern)"] = "not_used"
        self.services_groups["anforderungsmanagement"] = "projektmanagement"
        self.services_groups["marketing (intern)"] = "not_used"
        self.services_groups["urlaub"] = "not_used"
        self.services_groups["sonstiges"] = "not_used"
        self.services_groups["analyse"] = "not_used"
        self.services_groups["briefing"] = "projektmanagement"
        self.services_groups["cms-umsetzung"] = "cms-umsetzung"
        self.services_groups["consulting"] = "not_used"
        self.services_groups["controlling und reporting"] = "not_used"
        self.services_groups["datenbank-umsetzung"] = "not_used"
        self.services_groups["dokumentation"] = "not_used"
        self.services_groups["flash-umsetzung"] = "flash-umsetzung"
        self.services_groups["fortbildung (intern)"] = "not_used"
        self.services_groups["html-_css-umsetzung"] = "html-_css-umsetzung"
        self.services_groups["javascript-umsetzung"] = "javascript-umsetzung"
        self.services_groups["java-umsetzung"] = "java-umsetzung"
        self.services_groups["key-account-management"] = "key-account-management"
        self.services_groups["konzeption (technisch)"] = "not_used"
        self.services_groups["meeting (extern)"] = "not_used"
        self.services_groups["motion design"] = "not_used"
        self.services_groups["nebenkosten"] = "not_used"
        self.services_groups["php-umsetzung"] = "php-umsetzung"
        self.services_groups["review"] = "not_used"
        self.services_groups["server administration"] = "server administration"
        self.services_groups["software-design"] = "not_used"
        self.services_groups["text und lektorat"] = "not_used"
        self.services_groups["intern"] = "not_used"
        self.services_groups["qualitätsmanagement"] = "qualitatsmanagement"
        self.services_groups["illustration"] = "not_used"
        self.services_groups["seo_sem"] = "seo_sem"
        self.services_groups["tracking"] = "not_used"

    def load_services_groups_ids(self):

        self.services_groups_ids["design"] = []
        self.services_groups_ids["projektmanagement"] = []
        self.services_groups_ids["html-_css-umsetzung"] = []
        self.services_groups_ids["server administration"] = []
        self.services_groups_ids["flash-umsetzung"] = []
        self.services_groups_ids["javascript-umsetzung"] = []
        self.services_groups_ids["java-umsetzung"] = []
        self.services_groups_ids["key-account-management"] = []
        self.services_groups_ids["php-umsetzung"] = []
        self.services_groups_ids["server administration"] = []
        self.services_groups_ids["qualitätsmanagement"] = []
        self.services_groups_ids["seo_sem"] = []
        self.services_groups_ids["not_used"] = []

        for service in self.service_provider.get_services_as_tupples():

            service_name = service[0]
            service_id = service[1]
            self.services_groups_ids[self.services_groups[service_name]].append(service_id)











































































