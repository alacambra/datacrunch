import codecs
import MySQLdb

db = MySQLdb.connect(
        host="marceli", # your host, usually localhost
        user="root", # your username
        passwd="root", # your password
        db="redmine") # name of the data base


class RedmineServicesProvider:

    name_col = 0
    id_col = 1

    def __init__(self):
        self.name_col = 0
        self.id_col = 1
        self.services = []
        self.__load_services_with_entries__()

    def get_services_names(self):

        services_names = []

        for s in self.services:
            if s[self.name_col] not in services_names:
                services_names.append(s[self.name_col])

        return services_names

    def get_services_ids(self):

        services_ids = []

        for s in self.services:
            if s[self.id_col] not in services_ids:
                services_ids.append(s[self.id_col])

        return services_ids

    def get_services_as_tupples(self):
        return self.services

    def get_services_as_dict(self):

        services_dict = {}

        for s in self.services:
            services_dict[s[self.id_col]] = s[self.name_col]

        return services_dict

    def get_all_ids_for_service(self, service):

        ids = []
        for s in self.services:
            if s[self.name_col] == service:
                ids.append(s[self.id_col])

        return ids


    def __load_services_with_entries__(self):
        query = "SELECT e.name, activity_id " \
            "FROM redmine.time_entries as te, enumerations as e " \
            "where te.activity_id=e.id group by(activity_id);"

        cursor = db.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        self.services = [(self.prepare_services_name_for_use(r[self.name_col]), r[self.id_col]) for r in res]

    @staticmethod
    def prepare_services_name_for_use(service):
        service = codecs.decode(service.replace("/", "_"), "unicode_escape").lower()
        service = codecs.encode(service, "utf8").lower()
        return service
