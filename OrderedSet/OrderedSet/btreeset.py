'''
Created on 2024/07/22

@author: sin
'''
from pickle import NONE

class BTree:
    SIZE_UPPERBOUND = 4 - 1
    
    class Node:
        def __init__(self, data = None, lchild = None, rchild = None, parent = None):
            self.elements = list()
            if data != None :
                self.elements.append(data)
            self.children = list()
            if lchild != None or rchild != None :
                self.children.append(lchild)
                self.children.append(rchild)
            self.parent = parent
        
        def __str__(self):
            outstr = "Node("
            if not self.is_leaf() :
                outstr += str(self.children[0])
                outstr += ", "
            for i in range(self.size() - 1) :
                outstr += str(self.elements[i])
                if not self.is_leaf() :
                    outstr += ", " + str(self.children[i])
                outstr += ", "
            outstr += str(self.elements[-1])
            if not self.is_leaf() :
                outstr += ", " + str(self.children[-1])
            outstr += ") "
            return outstr
        
        def __repr__(self):
            return self.__str__()
        
        def size(self):
            return len(self.elements)
        
        def is_root(self):
            return self.parent == None
        
        def is_leaf(self):
            return len(self.children) == 0
        
        def lower_bound(self, elem, key):
            # print()
            ridx = self.size()
            lidx = 0
            # cnt = 0
            while lidx < ridx :
                idx = (lidx + ridx) >> 1
                key_e = key(elem)
                key_idx = key(self.elements[idx]) 
                if key_idx < key_e :
                    lidx = idx + 1
                else:
                    ridx = idx
            return ridx
    
        def insert_internal(self, data, left, right, key):
            ix = self.lower_bound(data, key)
            self.elements.insert(ix, data)
            self.children[ix] = left
            self.children.insert(ix+1,right)
            return ix
        
        def split(self):
            if self.size() <= BTree.SIZE_UPPERBOUND :
                return # nothing is worng.
            ix = self.size() >> 1
            updata = self.elements[ix]
            rsibling = BTree.Node()
            rsibling.elements = self.elements[ix+1:]
            rsibling.chldren = self.children[ix+1:]
            self.elements = self.elements[:ix]
            self.children = self.children[:ix+1]
            return updata, self, rsibling

    def __init__(self, key= lambda x: x):
        self.root = None
        self.sortkey = key
    
    def __str__(self):
        return str(self.root)
    
    def find_node_position(self, data):
        path = [self.root]
        while True:
            node = path[-1]
            ix = node.lower_bound(data, self.sortkey)
            if ix < len(node.elements) and node.elements[ix] == data :
                ''' found the data '''
                break
            if node.is_leaf() :
                ''' reached to the leaf '''
                break
            print(node)
            path.append(node.children[ix])
        return (path, ix)
        
    def insert(self, data):
        if self.root == None :
            self.root = BTree.Node(data)
        else:
            path, position = self.find_node_position(data)
            #print(path, position)
            node = path[-1]
            if position < node.size() and node.elements[position] == data :
                print(data, " found. Cancel insertion.")
                return 
            # node must be a leaf.
            node.elements.insert(position, data)
            if node.size() > self.SIZE_UPPERBOUND :
                parent = node.parent
                print(node)
                updata, left, right = node.split()
                # left or right is node
                if parent == None : # node was the root
                    self.root = BTree.Node(updata,left,right)
                    left.parent = self.root
                    right.parent = self.root
                else:
                    parent.insert_internal(updata,left,right, self.sortkey)
    