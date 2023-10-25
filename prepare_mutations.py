from math import log, ceil
from generators import mutations
import os, sys

base = 'mutations'
choices = 'ABCD'
instances = 10
rep = 10
m = 2
l = 100
for n in range(11000, 20000+1, 1000):
    for i in range(1, instances+1):
        h = (n + ceil(log(n,m))) // 2
        t = (n, h, m, l, choices)
        filename = base + '/n%dh%dm%dl%d%s%d.txt' % (t + tuple([i]))
        os.system('python3 generators.py mutations %d %d %d %d "%s" > "%s"' %
            (t + tuple([filename])))
        os.system('echo %s/gaxis.yrd,%s,-1,%d >> %s/script.txt' %
            (base, filename, rep, base))
