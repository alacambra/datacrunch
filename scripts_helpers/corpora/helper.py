import re
import MySQLdb
import codecs


db = MySQLdb.connect(
        host="marceli", # your host, usually localhost
        user="root", # your username
        passwd="root", # your password
        db="redmine") # name of the data base


class Service:

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return str(id) + ":" + self.name


def get_services():

    query_ids = "SELECT id, name FROM enumerations"
    cursor = db.cursor()
    cursor.execute(query_ids)
    res = cursor.fetchall()

    services = {}

    for r in res:
        s = Service(r[0], r[1])

        if s.name not in services:
            services[s.name] = []

        services[s.name].append(s)

    return services


def clean_word(w):

    w = w.strip()

    w = w.replace(".", "iamadot")
    w = re.sub("^\W*(\w+[^\w]*\w+)+\W*$", r"\1", w)
    w = w.replace("iamadot", ".")

    if len(w) > 0 and w[-1] == ".":
        w = w[:-1]

    return w


def word_is_valid(w):

    if len(re.findall("[0-9a-z]+", w)) == 0:
        return False

    return True


def get_stop_words():

    stop_words = codecs.open("resources/stop-words-de.txt", "r", "utf8")
    stop_words = codecs.encode(stop_words.read(), "unicode_escape")
    stop_words = stop_words.split("\\n")

    return stop_words
