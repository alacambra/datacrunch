#from nltk.corpus import gutenberg
from nltk import Text
from nltk.probability import FreqDist
import MySQLdb
import codecs
import re
import nltk

#print gutenberg.words('php_comments.csv')

#t = Text(gutenberg.words('php_comments.csv'))
#print t.common_contexts(["javascript"])
#print t.similar("javascrit")
#t.dispersion_plot(["javascript"])

#f = FreqDist(t)
#f.plot(50)
#print f.hapaxes()
#v = f.keys()
#print v[0:1000]

db = MySQLdb.connect(
        host="marceli", # your host, usually localhost
        user="root", # your username
        passwd="root", # your password
        db="redmine") # name of the data base


def get_words():

    query = "SELECT comments FROM comments_with_activity where activity_id = "

    cursor = db.cursor()

    stop_words = codecs.open("resources/stop-words-de.txt", "r", "utf8")
    stop_words = codecs.encode(stop_words.read(), "unicode_escape")
    stop_words = stop_words.split("\\n")

    services = get_services().values()

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
                    w = clean_word(w)

                    if word_is_valid(w):
                        to_analyze.append(w)


            #except Exception as e:
            #    print e
            #    print text

        services_dict[service[0].name] = to_analyze

    return services_dict


def generate_weight_dictionary(service, words):

    df = codecs.open("dicts/" + service + ".dict", "w+", "utf8");

    services_dict = {}
    services_dict[service] = words

    t = Text(words)
    f = FreqDist(t)

    for w in f:
        df.write(codecs.decode(w, "unicode_escape") + "\t" + str(f[w]) + "\n")

    df.close()

        #print w + ":" + str(f.freq(w))
        #v += f.freq(w)
    #f.plot(100)


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

all = get_words()

for service in all:
    generate_weight_dictionary(service.replace("/", "-"), all[service])

































