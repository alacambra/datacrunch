from AbstractItem import AbstractItem


class Project(AbstractItem):

    def __init__(self, row, order):
        self.name = row[1].decode(encoding="latin1")
        self.description = row[2].decode(encoding="latin1")
        self.parent_id = row[3]
        AbstractItem.__init__(self, row[0], "PROJECT", order)

    def __repr__(self):
        return AbstractItem.__repr__(self) + "|" + str(self.parent_id)

    def __str__(self):
        return AbstractItem.__str__(self) + "|" + str(self.parent_id)