__author__ = 'alacambra'


class ConfigReader:

    def __init__(self, config_file=None):
        if not config_file:
            self.config_file = "resources/config.cfg"
        else:
            self.config_file = config_file

        self.props = self._load_props_()

    def _load_props_(self):

        f = open(self.config_file, "r+")
        properties = {}

        for prop in f.readlines():
            prop = prop.split(":")
            properties[prop[0]] = prop[1][:-1]

        return properties

    def get_properties(self):
        return self.props

    def get_property(self, property_name):
        return self.props[property_name]

    def get_int_property(self, property_name):
        return int(self.props[property_name])