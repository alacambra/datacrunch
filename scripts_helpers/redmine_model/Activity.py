from AbstractItem import AbstractItem


class Activity(AbstractItem):

    def __init__(self, row, order):

        self.name = row[1].decode(encoding="latin1")
        AbstractItem.__init__(self, row[0], "ACTIVITY", order)
