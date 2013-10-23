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