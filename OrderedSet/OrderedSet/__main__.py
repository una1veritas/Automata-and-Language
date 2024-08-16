'''
Created on 2024/07/21

@author: Sin Shimozono
'''

import sys
import random
import time

from orderedset import OrderedSet
from btreeset import BTreeSet

btree = BTreeSet(minsize=16)
s = set()

oplist = list()
for i in range(1000000):
    op = 'A' if random.uniform(0,3) > 1 else 'R'
    n = int(random.uniform(0, 1024*128))
    oplist.append((op,n))

sw = time.time()
for e in oplist:
    if e[0] == 'A' :
        s.add(e[1])
    elif e[1] in s:
        s.remove(e[1])
sw = time.time() - sw
print(sw)
sw = time.time()
s = sorted(s)
sw = time.time() - sw
print(sw)

print(len(s))

sw = time.time()
for e in oplist:
    if e[0] == 'A' :
        btree.add(e[1])
    elif e[1] in btree:
        btree.remove(e[1])
sw = time.time() - sw
print(sw)
sw = time.time()
s = sorted(s)
sw = time.time() - sw
print(sw)
print(len(btree))
print(btree.hight())


'''
Ameli Alice Anette Amy Brad Bob Betty Ben Bolis Cathy Charles Claudia Cindy Colin David Daisy Aderyn Abbie Ada
'''