__author__ = 'alacambra'


class AbstractItem:
    def __init__(self, id, item_type, order):
        self.id = id
        self.order = order
        self.item_type = item_type

    def get_unique_name(self):
        return self.item_type + "|" + str(self.id)

    def __repr__(self):
        return str(self.id) + "|" + str(self.item_type) + "|" + str(self.order)

    def __str__(self):
        return str(self.id) + "|" + str(self.item_type) + "|" + str(self.order)


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


class Activity(AbstractItem):

    def __init__(self, row, order):

        self.name = row[1].decode(encoding="latin1")
        AbstractItem.__init__(self, row[0], "ACTIVITY", order)


class Issue(AbstractItem):
    def __init__(self, row, order):

        self.project_id = row[1]
        self.subject = row[2].decode(encoding="latin1")
        self.description = row[3].decode(encoding="latin1")
        AbstractItem.__init__(self, row[0], "ISSUE", order)


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


class User(AbstractItem):

    def __init__(self, row, order):

        self.login = row[1].decode(encoding="latin1")
        AbstractItem.__init__(self, row[0], "USER", order)