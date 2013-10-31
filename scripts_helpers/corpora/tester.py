# -*- coding: utf-8 -*-

import operator
import issues_corpora_script as iss
import activities_corpora_script as act

txt = "Bitte das Logo aktualisieren. Es wurde im Projektordner abgelegt."
s1 = iss.test(txt)
s2 = act.test(txt)
final = {}

issue_weigth = 100
activity_weight = 1

for s in s1:
    final[s] = issue_weigth*s1[s] + activity_weight*s2[s]

sorted_x = sorted(final.iteritems(), key=operator.itemgetter(1), reverse=True)

for x in sorted_x:
    print x

