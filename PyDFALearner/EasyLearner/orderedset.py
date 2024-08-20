
import sys

class OrderedSet(object):
        
    def __init__(self, collection = None, key= lambda x: x):
        self.sortkey = key
        if collection == None :
            self.elements = list()
        else:
            if isinstance(collection, OrderedSet) :
                self.elements = collection.elements.copy()
                self.sortkey = collection.sortkey
            else:
                self.elements = list()
                self.add_all(collection)
                
                
    def __str__(self)->str:
        return str(self.elements)

    def __iter__(self):
        return self.elements.__iter__()
    
    def __next__(self):
        return self.elements.__next__()
    
    def __len__(self):
        return len(self.elements)
    
    def __contains__(self, d):
        ix = self.lower_bound(d)
        if ix < len(self.elements) : 
            return self.elements[ix] == d
        return False 

    def __getitem__(self, idx):
        return self.elements[idx]
    
    def add_all(self, collection):
        for e in collection:
            self.add(e)
    
    def lower_bound(self, elem):
        # print()
        ridx = len(self.elements)
        lidx = 0
        # cnt = 0
        while lidx < ridx :
            idx = (lidx + ridx) >> 1
            # print(lidx, ridx,end="->") # "idx=",idx, elem, self.elements)
            key_e = self.sortkey(elem)
            key_idx = self.sortkey(self.elements[idx]) 
            if key_idx < key_e :
                lidx = idx + 1
            else:
                ridx = idx
            # print(lidx, ridx)
            # cnt += 1
            # if cnt > 4 :
            #     print("bug!!!")
            #     break
        return ridx
    
    def union(self, another):
        if isinstance(another, (set, list, tuple)) :
            os = OrderedSet(self)
            os.add_all(another)
            return os
        raise ValueError("OrderedSet union: Error, the argument is neither set, list nor tuple.")
    
    def insert(self, idx, elem):
        return self.elements.insert(idx, elem)
        
    def add(self, elem):
        idx = self.lower_bound(elem) #bisect.bisect_left(self.elements, elem, key=self.sortkey)
        # print(self.elements, elem, idx, self.elements[:idx])
        if len(self.elements) == 0 or len(self.elements) == idx or self.elements[idx] != elem :
            self.elements.insert(idx, elem)

    def pop(self, *args):
        return self.elements.pop(*args)
        
    def remove(self, elem):
        if len(self.elements) == 0 :
            raise KeyError(elem)
        idx = self.lower_bound(elem) #bisect.bisect_left(self.elements, elem,self.sortkey)
        if idx < len(self.elements) and self.elements[idx] == elem :
            self.elements.pop(idx)
        else:
            raise KeyError(elem)
    
    def clear(self):
        self.elements.clear()
