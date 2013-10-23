from AbstractItem import AbstractItem


class User(AbstractItem):

    def __init__(self, row, order):

        self.login = row[1].decode(encoding="latin1")
        AbstractItem.__init__(self, row[0], "USER", order)
