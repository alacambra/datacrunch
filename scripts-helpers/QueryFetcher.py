queryBoundary = "-NEXT-"
keySeparator = "||||"
f = open('queries.txt', 'r')
f = f.read().split(queryBoundary)
queries = {}

for query in f:
    if len(query) == 0:
        break

    entry = query.split(keySeparator)

    if entry[0][0] == '\n':
        entry[0] = entry[0][1:]

    queries[entry[0]] = entry[1]


def get_query(name):
    return queries[name]

