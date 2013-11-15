import MySQLdb
import matplotlib.pyplot as plt
import datetime
import time

#s = "01/01/2012"
#t = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())
#
#q = "SELECT UNIX_TIMESTAMP(i.created_on) as t, i.created_on, UNIX_TIMESTAMP(i.updated_on), spi.total_services " \
#    "FROM redmine.total_number_of_services_per_issue as spi inner join issues as i on spi.issue_id=i.id " \
#    "HAVING t > " + str(t) + "" \
#    "order by created_on DESC"

#db = MySQLdb.connect(
#        host="marceli", # your host, usually localhost
#        user="root",    # your username
#        passwd="root",  # your password
#        db="redmine")   # name of the data base
#cursor = db.cursor()
#cursor.execute(q)

services = {}
services_inv = {}
matrix = []


d = open("../resources/R/services_pairs_2_levels-2012.csv", "r")

i = 0
max_length = 0
for line in d.readlines():

    line = line[:-1].split(",")[0]

    if not line in services:
        services[line] = i
        if len(line) > max_length:
            max_length = len(line)

        services_inv[i] = line
        i += 1

num_services = i
d.seek(0)


def get_element(row, column):
    for element in matrix:
        if element[0] == row and element[1] == column:
            return element[2]
    return 0


def complete_line(name):
    dif = (max_length-len(name)) / 2
    #return name
    return " "*dif + name + " "*dif

for line in d.readlines():
    line = line[:-1].split(",")
    matrix.append((services[line[0]], services[line[2]], line[1]))

r = ""
for i in range(0, num_services):
    r += complete_line(services_inv[i]) + "\t"

print r

for i in range(0, num_services):
    r = complete_line(services_inv[i]) + "\t"
    r = ""
    for j in range(0, num_services):
        r += str(get_element(i, j)) + "\t"

    print r
