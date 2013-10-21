from py2neo import neo4j
import os
#from py2neo import tool
import tool2 as tool
import CypherCreator as qc
import QueryFetcher as qf
import NamesCounter as nc
import re
from redmine_model import Issue as iss

uri = "http://marceli:7474/db/data";
graph_db = neo4j.GraphDatabaseService(uri);

def cypher(query):
    print query
    return neo4j.CypherQuery(graph_db, query).execute()

#cypher(qf.get_query("remove_all"))
#cypher(qc.CypherCreator().create_query())


def rel_weight():
    paths = cypher(qf.get_query("basic"))
    all_nodes = cypher(qf.get_query("get_all"))

    f = open("temp", "a+")
    writer = tool.ResultWriter(f)
    writer.write("text", all_nodes)
    writer.write("text", paths)
    f.seek(0)
    lines = f.read()
    print lines
    nc.NamesCounter().infer_names(lines)
    f.close()
    os.remove("temp")


def dist_matrix_(distance):
    paths = cypher(qf.get_query("distance", distance))

    f = open("temp", "a+")
    writer = tool.ResultWriter(f)
    writer.write("text", paths)

    f.seek(0)
    lines = f.read().split("\n")

    regex = re.compile("\((\d+)\).+\((\d+)\) \| (\d+)")
    matrix_ = {}

    for line in lines:
        l = regex.findall(line)

        if len(l) == 0:
            continue

        assign_values_to_diagonal_matrix(l, matrix_, 0, 1)
        assign_values_to_diagonal_matrix(l, matrix_, 1, 0)

    print_matrix(matrix_)

    f.close()
    os.remove("temp")

    return matrix_


def assign_values_to_diagonal_matrix(values, m1, r_index, c_index):

    r = int(values[0][r_index])
    c = int(values[0][c_index])

    if r == c:
        return

    w = int(values[0][2])

    if not r in m1:
        m1[r] = {}

    if not c in m1[r]:
        m1[r][c] = 0

    m1[r][c] += w


def print_matrix(matrix_):

    index = sorted(matrix_)

    print "--" + "\t",

    nodes_names = get_nodes_names()

    for r in index:
        print nodes_names[r] + "\t",

    print ""

    for r in index:
        print "--" + "\t",

    print "-"

    for r in index:
        print nodes_names[r] + "|\t",
        for c in index:
            if r == c:
                print "-\t",
            elif c in matrix_[r]:
                print str(matrix_[r][c]) + "\t",
            else:
                print "0\t",

        print ""


def get_nodes_names():
    all_nodes = cypher(qf.get_query("get_all"))

    f = open("temp", "a+")
    writer = tool.ResultWriter(f)
    writer.write("text", all_nodes)
    f.seek(0)
    lines = f.read()
    f.close()

    node_regex = '\(([\d]+) \{"name":"([\w]+)"\}'
    entries = re.findall(node_regex, lines, re.MULTILINE)

    maps = {}
    for entry in entries:
        maps[int(entry[0])] = entry[1]

    return maps


#get_nodes_names()

dist_matrix_(1)
#print "-------------------------------"
#dist_matrix_(2)
#print "-------------------------------"
#dist_matrix_(1)
#print "-------------------------------"
#dist_matrix(6)
#print "-------------------------------"
#dist_matrix(7)