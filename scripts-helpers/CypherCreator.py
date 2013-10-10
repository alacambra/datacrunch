from gi.overrides.GLib import child_watch_add
from nis import match
from random import randint


class CypherCreator:

    def __init__(self):
        self.create = "CREATE";
        self.created_nodes = []
        self.rel_str = "-[:R{w:#w#}]-"
        self.query = []
        self.rel = []

    def create_relations(self, group):

        """
         @type group: NodeGroup
        """

        lvl_childs = group.get_childs_lvl();
        childs = group.get_childs();
        lvl_parent = group.get_parent_lvl()
        parent = group.get_parent();

        while len(childs):
            child = childs.pop()
            v = child + self.rel_str.replace("#w#", str(lvl_parent)) + parent;
            self.rel.append(v);

            for c in childs:
                v = child + self.rel_str.replace("#w#", str(lvl_childs)) + c
                self.rel.append(v);

    def create_nodes(self, group):

        """
         @type group: NodeGroup
        """

        nodes = group.get_names()

        for node in nodes:
            if node not in self.created_nodes:
                self.created_nodes.append(node)
                self.query.append("(" + node + "{ name:'" + node + "'})")

    def create_query(self):

        f = open('sch.in', 'r');

        for group in f:
            group = group[:-1].split("|")
            group = NodeGroup(group);
            self.create_nodes(group);
            self.create_relations(group);

        query = ",\n\r".join(self.query);
        rel = ",\n\r".join(self.rel);

        #print self.create + "\n\r" + query + ",\r\n" + rel
        return self.create + "\n\r" + query + ",\r\n" + rel


class NodeGroup:

    def __init__(self, group):
        self.parent = group[0];
        self.childs = group[1].split(",")
        self.parent_lvl = group[2];
        self.childs_lvl = group[3];

    def get_parent(self):
        return self.parent;

    def get_childs(self):
        return self.childs;

    def get_childs_lvl(self):
        return self.childs_lvl;

    def get_parent_lvl(self):
        return self.parent_lvl;

    def get_names(self):
        names = self.childs
        names.append(self.parent)
        return names

#CypherCreator().create_query();