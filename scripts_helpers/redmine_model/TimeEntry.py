from AbstractItem import AbstractItem


class TimeEntry(AbstractItem):

    def __init__(self, row, order):

        self.project_id = row[1]
        self.user_id = row[2]
        self.issue_id = row[3]
        self.hours = row[4]
        self.comment = row[5].decode(encoding="latin1")
        self.activity_id = row[6]
        self.activity_name = row[7].decode(encoding="latin1")
        AbstractItem.__init__(self, row[0], "TIME_ENTRY", order)
