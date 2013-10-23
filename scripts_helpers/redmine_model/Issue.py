from AbstractItem import AbstractItem

class Issue(AbstractItem):
    def __init__(self, row, order):

        self.project_id = row[1]
        self.subject = row[2].decode(encoding="latin1")
        self.description = row[3].decode(encoding="latin1")
        AbstractItem.__init__(self, row[0], "ISSUE", order)

