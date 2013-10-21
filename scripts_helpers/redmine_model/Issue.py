from AbstractItem import AbstractItem

class Object(AbstractItem):
    def __init__(self, row, order):

        self.id = row[0]
        self.project_id = row[1]
        self.subject = row[2]
        self.description = row[3]
        AbstractItem.__init__(self, "ISSUE", order)

