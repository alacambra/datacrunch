f = open("removeme.del", "r")
l = f.readlines()
s = 0
for res in l:
    res = res.split(" ")
    s += int(res[0])

print s