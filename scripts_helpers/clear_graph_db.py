import QueryFetcher as qf
from py2neo import neo4j

uri = "http://marceli:7474/db/data";
graph_db = neo4j.GraphDatabaseService(uri);


def run():
    print cypher(qf.get_query("remove_all"))


def cypher(query):
    print query
    r = neo4j.CypherQuery(graph_db, query).execute()
    return r
