import MySQLdb
import matplotlib.pyplot as plt
import datetime
import time

s = "01/01/2012"
t = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())

q = "SELECT UNIX_TIMESTAMP(i.created_on) as t, i.created_on, UNIX_TIMESTAMP(i.updated_on), spi.total_services " \
    "FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id " \
    "HAVING t > " + str(t) + "" \
    "order by created_on DESC"

db = MySQLdb.connect(
        host="marceli", # your host, usually localhost
        user="root",    # your username
        passwd="root",  # your password
        db="redmine")   # name of the data base


cursor = db.cursor()
cursor.execute(q)
row = cursor.fetchall()
x = []
y = []

last = []

for r in row:
    print r
    #x.append(r[0])
    #y.append(r[2])
#
#plt.scatter(x, y)
#plt.grid(True)
#plt.title("")
#plt.axis([0, 10, 0, 100])
#plt.xlabel("activity_weigth / issue_weight")
#plt.ylabel("perfect matches(% over " + str(self.results[service][0].total) + ")")
#try:
#    plt.savefig("removeme.png")
#except Exception as e:
#    print e


#plt.close()
