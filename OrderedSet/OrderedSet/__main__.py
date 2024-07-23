'''
Created on 2024/07/21

@author: Sin Shimozono
'''

import sys
from orderedset import OrderedSet
from btreeset import BTree

t = BTree()
for d in sys.argv[1:] :
    print("inserting ", d)
    t.insert(d)
    print("updated btree =", t, "\n")

print("finished. ")
'''
Ameli Alice Anette Amy Brad Bob Betty Ben Bolis Cathy Charles Claudia Cindy Colin David Daisy
'''