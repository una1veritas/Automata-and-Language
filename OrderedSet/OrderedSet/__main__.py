'''
Created on 2024/07/21

@author: Sin Shimozono
'''

import sys
from orderedset import OrderedSet
from btreeset import BTree

t = BTree()
for d in sys.argv[1:] :
    t.insert(d)
    print(t)
    

print("finished. ")