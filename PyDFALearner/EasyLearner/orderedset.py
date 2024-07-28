
import sys

class OrderedSet(object):
    
    def __init__(self, collection = None, key= lambda x: x):
        self.elements = list()
        self.sortkey = key
        if collection is not None :
            self.insert_all(collection)
    
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
        if ix >= len(self.elements) : 
            return False 
        return self.elements[ix] == d
    
    def __getitem__(self, idx):
        return self.elements[idx]
    
    def insert_all(self, collection):
        for e in collection:
            self.insert(e)
    
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
    
    def insert(self, elem):
        idx = self.lower_bound(elem) #bisect.bisect_left(self.elements, elem, key=self.sortkey)
        # print(self.elements, elem, idx, self.elements[:idx])
        if len(self.elements) == 0 or len(self.elements) == idx or self.elements[idx] != elem :
            self.elements.insert(idx, elem)
            
    def pop(self, elem):
        if len(self.elements) == 0 :
            return
        idx = self.lower_bound(elem) #bisect.bisect_left(self.elements, elem,self.sortkey)
        if self.elements[idx] == elem :
            self.elements.pop(idx)
    
    def clear(self):
        self.elements.clear()
