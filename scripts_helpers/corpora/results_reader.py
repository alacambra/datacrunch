import re
import os
import codecs
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class ResultsReader:

    def __init__(self, results_file):

        self.img_directory = results_file[:-4] + str(time.time()) + "/"
        os.mkdir(self.img_directory[:-1])
        self.results_file = results_file
        self.results = {}
        self.load_results()
        self.plot()

    def plot(self):

        for service in self.results:

            results = {}
            for result in self.results[service]:

                if result.proportion in results:
                    raise Exception(result.proportion)

                results[result.proportion] = result.result

            plt.scatter(results.keys(), results.values())

            plt.grid(True)
            plt.title(service)
            #plt.axis([0, 10, 0, 100])
            plt.xlabel("activity_weigth / issue_weight")
            plt.ylabel("perfect matches(% over " + str(self.results[service][0].total) + ")")

            try:
                plt.savefig(self.img_directory + codecs.encode(service.replace("/", "_"), "utf8") + ".png")
            except Exception as e:
                print service
                print e
                continue

            plt.close()

    def load_results(self):

        f = codecs.open(self.results_file, "r+", encoding="latin1")

        for l in f.readlines():
            r = Result(l)

            if r.service not in self.results:
                self.results[r.service] = []
            self.results[r.service].append(r)

        return self.results


class Result():

    def __init__(self, result_line):
        r = "(?:([^\t]+)\t\t)(?:([^\t]+)\t\t)(?:([^\t]+)\t\t)(?:([^\t]+)\t\t)([\d]+)"
        a = re.findall(r, result_line)[0]
        self.service, self.issue_weigth, self.activity_weigth, self.total, self.ok = re.findall(r, result_line)[0]
        self.proportion = round(float(self.activity_weigth) / float(self.issue_weigth), 5)
        self.result = round(float(self.ok) / float(self.total), 2) * 100

    def __str__(self):
        return "service:\"" +self.service + \
               "\"\nissue weigth:" + self.issue_weigth + \
               "\nactivity_weigth:" + self.activity_weigth + \
               "\nproportion:" + str(self.proportion) + \
               "\nok:" + self.ok + \
               "\ntotal:" + self.total + \
               "\nresult:" + str(self.result)