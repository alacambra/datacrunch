from py2neo import neo4j
import os
#from py2neo import tool
import tool2 as tool
import CypherCreator as qc
import QueryFetcher as qf
import NamesCounter as nc
import re


uri = "http://marceli:7474/db/data";
graph_db = neo4j.GraphDatabaseService(uri);


def cypher(query):
    return neo4j.CypherQuery(graph_db, query).execute()

#cypher(qf.get_query("remove_all"))
#cypher(qc.CypherCreator().create_query())


def rel_weight():
    paths = cypher(qf.get_query("basic"))
    all = cypher(qf.get_query("get_all"))

    f = open("temp", "a+")
    writer = tool.ResultWriter(f)
    writer.write("text", all)
    writer.write("text", paths)
    f.seek(0)
    lines = f.read()
    print lines
    nc.NamesCounter().infer_names(lines)
    f.close()
    os.remove("temp")


def dist_matrix(distance):
    paths = cypher(qf.get_query("distance", 1))

    f = open("temp", "a+")
    writer = tool.ResultWriter(f)
    writer.write("text", paths)

    f.seek(0)
    lines = f.read().split("\n")

    path_id_regex = "\(([\d]+)\)-\[:"R"\]->\(([\d]+)\)\s\|\s(\d+)"
    regex = re.compile("\(([\d]+)\)-\[:\"R\"\]->\(([\d]+)\)\s\|\s(\d+)")
    m1 = {}

    for line in lines:
        l = regex.findall(line)

        if len(l) == 0:
            continue

        r = int(l[0][0])
        c = int(l[0][1])

        if r == c:
            continue

        w = int(l[0][2])

        if not m1.has_key(r):
            m1[r] = {}

        if not m1[r].has_key(c):
            m1[r][c] = 0

        m1[r][c] += w

    print m1


    s = ""

    for r, c in m1.iteritems():
        s += str(r) + "|"

    f.close()
    os.remove("temp")

dist_matrix(1)