from AbstractItem import AbstractItem


class Object(AbstractItem):

    def __init__(self, row, order):
        self.id = row[0]
        self.project_id = row[1]
        self.user_id = row[2]
        self.issue_id = row[3]
        self.hours = row[4]
        self.comment = row[5]
        self.activity_id = row[6]
        self.activity_name = row[7]
        AbstractItem.__init__(self, "TIME_ENTRY", order)
