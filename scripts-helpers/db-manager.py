from py2neo import neo4j
import os
#from py2neo import tool
import tool2 as tool
import CypherCreator as qc
import QueryFetcher as qf
import NamesCounter as nc


uri = "http://marceli:7474/db/data";
graph_db = neo4j.GraphDatabaseService(uri);


def cypher(query):
    return neo4j.CypherQuery(graph_db, query).execute()

cypher(qf.get_query("remove_all"))
cypher(qc.CypherCreator().create_query())
paths = cypher(qf.get_query("basic"))
all = cypher(qf.get_query("get_all"))

f = open("temp", "a+")
writer = tool.ResultWriter(f)
writer.write("text", all)
writer.write("text", paths)
f.seek(0)
lines = f.read()
nc.NamesCounter().infer_names(lines)
f.close()
os.remove("temp")
