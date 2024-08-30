'''
Created on 2024/07/21

@author: Sin Shimozono
'''
from typing import Iterable

class UnionFindSet(object):
    def __init__(self, a_collection = None):
        # elements ib a_collection must be hashable.
        self.parent = dict()
        if hasattr(a_collection, "__iter__") :
            for x in a_collection:
                self.parent[x] = x
    
    def mergeinto(self, x, y):
        x = self.find(x)
        y = self.find(y)
        self.parent[y] = x
    
    def find(self, x):
        if x not in self.parent :
            return None
        root = x
        while root != self.parent[root] :
            root = self.parent[root]
        while x != self.parent[x] :
            t = x
            x = self.parent[x]
            self.parent[t] = root
        return x
    
    def elements(self):
        return self.parent.keys()
    
    def __iter__(self):
        if len(self.parent) == 0 :
            raise StopIteration()
        for k in self.parent.keys() :
            if k == self.find(k) :
                yield k
        
    def __len__(self):
        return len([k for k in self.parent if k == self.parent[k]])
    
    def __contains__(self, d):
        return self.parent.__contains__(d) 
    
    def __str__(self)->str:
        t = "UnionFindSet{"
        for k in self.parent :
            if k == self.parent[k] :
                if isinstance(k, str) :
                    t+= "'"+k+"'" + " :"
                else:
                    t+= str(k) + " :"
                tmpset = set()
                for x in self.parent:
                    if k == self.find(x) :
                        tmpset.add(x)
                t += str(tmpset) + ", "
        return t +"} "
    
