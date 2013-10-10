import re
import operator

names_ = {}
class NamesCounter:

    def __init__(self):
        self.final_points = {}

    def get_final_points(self, results):

        #node_regex = '\{name:"([\w]+)"\}'
        node_regex = '\((\w+)\)'
        entry_regex = "([^|]+)\|[\s]{1}(\d+)[ ]+\|[\s]{1}(\d+)[ ]+\|[\s]{1}(\d+)[ ]+"
        for result in results:
            entry = re.findall(entry_regex, result)
            if len(entry) == 0:
                continue

            path = entry[0][0]
            names = re.findall(node_regex, path)
            for name in names:
                if self.final_points.has_key(name):
                    self.final_points[name] += 1;
                else:
                    self.final_points[name] = 1

        final_points = sorted(self.final_points.iteritems(), key=operator.itemgetter(1), reverse=True)
        for (name, points) in final_points:
            print name + ":" + str(points)

    def infer_names(self, paths):

        node_regex = '\(([\d]+) \{"name":"([\w]+)"\}'
        entry_regex = "(\([^|]+)\|[\s]{1}(\d+)[ ]+\|[\s]{1}(\d+)[ ]+\|[\s]{1}(\d+)[ ]+"
        path_id_regex = "\(([\d]+)\)"

        entries = re.findall(node_regex, paths, re.MULTILINE)

        for entry in entries:
            names_[entry[0]] = entry[1]

        s = re.sub(path_id_regex, map_replace, paths)
        #print self.get_final_points(s.split("\n"))
        return s

def map_replace(matchobj):
    return "(" + names_[matchobj.group(1)] + ")";




