import MySQLdb
import operator

db = MySQLdb.connect(
    host="marceli", # your host, usually localhost
    user="root",    # your username
    passwd="root",  # your password
    db="redmine")   # name of the data base

date = "2013-01-01"
cond_num_services = "=1"
q = "select " \
    "i.id AS issue_id," \
    "i.parent_id AS parent_id," \
    "e.name AS activity," \
    "sum(te.hours) AS invested_time," \
    "count(te.hours) as num_of_services," \
    "i.subject AS subject " \
    "from " \
    "((time_entries te " \
    "join issues i ON ((te.issue_id = i.id))) " \
    "join enumerations e) " \
    " where " \
    " te.activity_id = e.id " \
    " and i.created_on > \"" + date + "\"" \
    "group by i.id , e.name " \
    " having num_of_services " + cond_num_services + " " \
    "order by i.id, invested_time desc"

#" i.created_on > \"2013-01-01\""
print q
cursor = db.cursor()
cursor.execute(q)
res = cursor.fetchall()

issues = {}


class Row:

    def __init__(self, row):
        self.issue_id = row[0]
        self.parent_id = row[1]
        self.activity = row[2]
        self.invested_time = row[3]
        self.num_of_services = row[4]
        self.subject = row[5]

class LongestService:

    def __init__(self):
        self.issues = {}
        self.total_time_of_activities = {}
        self.absolute_activities_freqs = {}
        self.absolute_invested_time = {}
        self.load_activities()

    def load_activities(self):
        q = "select " \
            "e.name AS activity, " \
            "count(te.hours) as num_of_services " \
            "from " \
            "((time_entries te " \
            "join issues i ON ((te.issue_id = i.id))) " \
            "join enumerations e) " \
            " where " \
            " te.activity_id = e.id " \
            " and i.created_on > \"" + date + "\"" \
            " group by i.id , e.name " \
            " having num_of_services>0"

        print q
        cursor = db.cursor()
        cursor.execute(q)
        res = cursor.fetchall()

        for r in res:
            self.total_time_of_activities[r[0]] = 0
            self.absolute_activities_freqs[r[0]] = 0
            self.absolute_invested_time[r[0]] = 0

    def compare_row(self, row):
        """
        @type row: Row
        """
        if row.issue_id in self.issues:
            activity, time = self.issues[row.issue_id]
            if time < row.invested_time:
                self.issues[row.issue_id] = (row.activity, row.invested_time)

        else:
            self.issues[row.issue_id] = (row.activity, row.invested_time)

        self.total_time_of_activities[row.activity] += 1

    def print_results(self):
        for i in self.issues.values():
            print i

    def get_absolute_frequency(self):
        for activity, time in self.issues.values():
            self.absolute_activities_freqs[activity] += 1

    def get_absolute_invested_time(self):
        for activity, time in self.issues.values():
            self.absolute_invested_time[activity] += time

    def print_absolute_frequency(self):

        self.get_absolute_frequency()
        sorted_x = sorted(self.absolute_activities_freqs.items(), key=operator.itemgetter(0), reverse=False)
        for activity in sorted_x:
             #print activity[0] + ":" + str(activity[1])
            print activity[1]

    def print_absolute_ponderated_frequency(self):
        activities = {}

        threshold = 0
        total = 0

        for a in self.get_absolute_frequency().values():
            total += a

        for activity in self.absolute_activities_freqs:

            #if self.get_absolute_frequency()[activity] * 100 / total < threshold:
            #    continue

            activities[activity] = self.absolute_activities_freqs[activity] * 100
            activities[activity] /= (self.total_time_of_activities[activity])

        sorted_x = sorted(activities.items(), key=operator.itemgetter(0), reverse=False)
        for activity in sorted_x:
            #print activity[0] + ":" + str(activity[1])
            print activity[1]

    def print_absolute_invested_time(self):

        self.get_absolute_invested_time()
        sorted_x = sorted(self.absolute_invested_time.items(), key=operator.itemgetter(0), reverse=False)
        for activity in sorted_x:
             #print activity[0] + ":" + str(activity[1])
            print activity[1]

ls = LongestService()

for r in res:
    ls.compare_row(Row(r))

#ls.print_absolute_frequency()
#ls.print_absolute_ponderated_frequency()
ls.print_absolute_invested_time()
























































































