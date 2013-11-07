import helper
import re
import matplotlib.pyplot as plt
import operator
import math
import os
import time


class ResultsReader:

    def __init__(self, results_file):

        self.img_directory = results_file[:-4] + str(time.time()) + "/"
        os.mkdir(self.img_directory[:-1])
        self.results_file = results_file
        self.results = {}
        self.load_results()
        self.plot()

    def get_results_by_service(self):
        a = 0

    def plot(self):

        for service in self.results:

            results = {}
            for result in self.results[service]:

                if result.proportion in results:
                    raise Exception(result.proportion)

                results[result.proportion] = result.result

            x = [x for x in results]
            y = [y for y in results.values()]
            plt.scatter(x, y)

            plt.grid(True)
            plt.title(service)
            plt.axis([0, 10, 0, 100])
            plt.xlabel("activity_weigth / issue_weight")
            plt.ylabel("perfect matches(% over " + str(self.results[service][0].total) + ")")

            try:
                plt.savefig(self.img_directory + service + ".png")
            except Exception:
                continue

            plt.close()

    def load_results(self):

        f = open(self.results_file, "r+")

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

print ResultsReader("results/results_18875_-7-11-2013_11_39-41.dat")
#plt.plot([1,3,2,5,4], [4,67,3,5,1])
#plt.show()
