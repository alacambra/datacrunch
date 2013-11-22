import os
import re
import MySQLdb
import codecs
from scripts_helpers.corpora.config_loader import ConfigReader
from scripts_helpers.corpora.redmine_services_provider import RedmineServicesProvider

db = MySQLdb.connect(
        host="marceli", # your host, usually localhost
        user="root", # your username
        passwd="root", # your password
        db="redmine") # name of the data base


field_separator = "[[[[[]]]]]"
results_field_separator = "\t\t"

class WordHelper:

    word_dot_replacement = "iamadot"

    def __init__(self, cr):
        """
        @type cr: ConfigReader
        """
        self.cr = cr
        self.word_dot_replacement = "iamadot"

    @staticmethod
    def clean_word(w):
        w = w.strip()
        w = w.replace(".", WordHelper.word_dot_replacement)
        w = re.sub("^\W*(\w+[^\w]*\w+)+\W*$", r"\1", w)
        w = w.replace(WordHelper.word_dot_replacement, ".")

        if len(w) > 0 and w[-1] == ".":
            w = w[:-1]

        return w

    @staticmethod
    def word_is_valid(w):

        if len(re.findall("[0-9a-z]+", w)) == 0:
            return False

        return True

    @staticmethod
    def get_stop_words():

        stop_words = codecs.open("../resources/stop-words-de.txt", "r", "utf8")
        stop_words = codecs.encode(stop_words.read(), "unicode_escape")
        stop_words = stop_words.split("\\n")

        return stop_words


class Dictionary:

    def __init__(self, cr, dictionary_name, service_provider):
        """
        @type cr: ConfigReader
        @type service_provider:RedmineServicesProvider
        """
        self.dict_folder_name = cr.get_property("dicts_dir")
        self.dictionary_name = dictionary_name
        self.service_provider = service_provider

        if not os.path.isdir(self.get_dict_directory()):
            os.mkdir(self.get_dict_directory())

    def get_dict_service_file_name(self, service):
        return self.get_dict_directory() + service + ".dict"

    def get_dict_directory(self):
        return self.dict_folder_name + self.dictionary_name + "/"

    def get_dict_length(self, service):
        d = open(self.get_dict_service_file_name(service))
        return len(d.readlines())

    def get_file_for_service(self, service, mode):
        return open(self.get_dict_service_file_name(service), mode)

    def get_dicts_weight_file(self):
        return open(self.get_dict_directory() + "dicts_weight.dat", "r+")

    def get_dicts_weight(self):

        f = self.get_dicts_weight_file()
        d = {}

        for entry in f.readlines():
            w = entry.split("\t")
            d[w[0]] = w[2][:-1]

        return d

    def generate_dictionary_size_file(self, services_names=None):

        if not services_names:
            services_names = self.service_provider.get_services_names()

        sf = open(self.get_dict_directory() + "dicts_weight.dat", "w+")

        lengths = {}
        total_length = 0
        for service in services_names:
            file_name = self.get_dict_service_file_name(service)
            if not os.path.isfile(file_name):
                continue

            f = open(file_name, "r+")
            length = len(f.readlines())
            total_length += length
            lengths[service] = length
            f.close()

        for service in lengths:
            weight = float(lengths[service]) / float(total_length)*100
            sf.write(service + "\t" + str(lengths[service]) + "\t" + str(weight) + "\n")

        sf.close()


















































































