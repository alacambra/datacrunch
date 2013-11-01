# -*- coding: utf-8 -*-

import operator
import issues_corpora_builder as iss
import activities_corpora_builder as act
import helper


def individual_test(to_test):
#txt = 'Contentpflege + HTML / CSS Anpassung'
#txt = 'Wiki-Artikel um lokale Entwicklungsumgebung für das NPS Backend'
#txt = "und den Trouble Assistant einzurichten erstellt"

    s1 = iss.test(to_test)
    s2 = act.test(to_test)
    final = {}

    issue_weigth = 0
    activity_weight = 1

    for s in s1:
        #print str(s1[s]) + str(s2[s])

        final[s] = issue_weigth*s1[s] + activity_weight*s2[s]

    return order_results(final)



def order_results(final):

    sorted_x = sorted(final.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_x

    for x in sorted_x:
        print x


def full_test():

    query = "select e.id AS activity_id, e.name AS activity_name, te.comments AS comments from(redmine.time_entries te join redmine.enumerations e ON ((te.activity_id = e.id))) order by te.id"
    cursor =helper.db.cursor()
    cursor.execute(query)
    entries = cursor.fetchall()

    total = 0
    correct = 0
    false = 0

    results = {}

    for s in helper.get_services():
        results[s] = [0,0,0]

    for entry in entries:
        comments = entry[2]
        expected = entry[1]

        res = individual_test(comments)

        print comments

        if res[0][0] == expected:
            correct += 1
            results[expected][0] += 1
        else:
            results[expected][1] += 1
            false += 1

        results[expected][2] += 1
        total += 1

        print "@"*15
        for r in results:
            print r + ":" + str(results[r])

    print "correct:" + str(correct) + "||" + str(float(correct) / float(total))
    print "false:" + str(false)
    print "total:" + str(total)

full_test()