'''
Created on 2024/07/21

@author: Sin Shimozono
'''

class UnionFindSet(object):
    def __init__(self, a_collection):
        # elements ib a_collection must be hashable.
        self.parent = dict()
        for x in a_collection:
            self.parent[x] = x
    
    def mergetoleft(self, x, y):
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
    
    def __str__(self)->str:
        t = "UnionFindSet{"
        for k in sorted(self.parent) :
            if k == self.parent[k] :
                if isinstance(k, str) :
                    t+= "'"+k+"'" + " :"
                else:
                    t+= str(k) + " :"
                tmpset = set()
                for x, r in self.parent.items():
                    if r == k :
                        tmpset.add(x)
                t += str(tmpset) + ", "
        return t +"} "
    
