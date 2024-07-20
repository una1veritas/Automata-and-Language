
import sys
import bisect

class OrderedSet(object):
    
    def __init__(self, collection):
        self.elements = list()
        self.insert_all(collection)
    
    def __str__(self)->str:
        return str(self.elements)

    def insert_all(self, collection):
        for e in collection:
            self.insert(e)
    
    def insert(self, elem):
        idx = bisect.bisect_left(self.elements, elem)
        #print(self.elements, elem, self.elements[:idx])
        if len(self.elements) == 0 or self.elements[idx] != elem :
            self.elements.insert(idx, elem)
            
    def pop(self, elem):
        if len(self.elements) == 0 :
            return
        idx = bisect.bisect_left(self.elements, elem)
        if self.elements[idx] == elem :
            self.elements.pop(idx)
    
    def clear(self):
        self.elements.clear()

print(sys.argv[1:])
s = OrderedSet(sys.argv[1:])
print(s)
s.delete('y')
s.delete('f')
s.delete('t')
print(s)