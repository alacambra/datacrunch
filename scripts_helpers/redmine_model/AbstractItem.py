__author__ = 'alacambra'


class AbstractItem:
    def __init__(self, type, order):
        self.order = order
        self.type = type