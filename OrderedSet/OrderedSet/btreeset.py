'''
Created on 2024/07/22

@author: sin
'''

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
            outstr = "("
            if self.is_leaf() :
                outstr += ", ".join(self.elements)
            else:
                for i in range(self.size()) :
                    outstr += str(self.children[i]) + ", " + str(self.elements[i]) + ", "
                outstr += str(self.children[-1])
            outstr += ") "
            return outstr
        
        def __repr__(self):
            return str(self.elements) #+ ", " + str(self.children)
        
        def size(self):
            return len(self.elements)
        
        def is_root(self):
            return self.parent == None
        
        def is_leaf(self):
            return len(self.children) == 0
        
        def has_rightsibling(self, parent, poshint = None, data=None):
            if poshint == None and data != None:
                poshint = parent.find_node_position(data)
            elif poshint == None and data == None :
                for i in range(parent.size()+1) :
                    if parent.children[i] == self :
                        poshint = i
                        break
            if poshint + 1 <= parent.size() and parent.children[poshint+1].size() < BTree.SIZE_UPPERBOUND :
                return True
            else:
                return False
                
        def has_leftsibling(self, parent, poshint = None, data=None):
            if poshint == None and data != None:
                poshint = parent.find_node_position(data)
            elif poshint == None and data == None :
                for i in range(parent.size()+1) :
                    if parent.children[i] == self :
                        poshint = i
                        break
            if poshint > 0 and parent.children[poshint - 1].size() < BTree.SIZE_UPPERBOUND :
                return True
            else:
                return False
                
                
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
    
        def insert_internal(self, ix, data, left, right):
            print(data, ix, "left", left, "right", right)
            self.elements.insert(ix, data)
            print("self.elements=",self.elements)
            self.children.insert(ix+1,right)
            self.children[ix] = left
            print("insert internal: ", self.elements, self.children)
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
        
        def rotate_right(self, parent, posatp = None):
            if posatp == None :
                for i in range(parent.size()+1) :
                    if parent.children[i] == self :
                        posatp = i
                        break
            rsibling = parent.children[posatp+1]
            if rsibling.is_leaf() :
                updata = self.elements.pop()
                downdata = parent.elements[posatp]
                parent.elements[posatp] = updata
                rsibling.elements.insert(0,downdata)
        
        def rotate_left(self, parent, posatp = None):
            if posatp == None :
                for i in range(parent.size()+1) :
                    if parent.children[i] == self :
                        posatp = i
                        break
            lsibling = parent.children[posatp - 1]
            if lsibling.is_leaf() :
                updata = self.elements.pop(0)
                downdata = parent.elements[posatp-1]
                parent.elements[posatp-1] = updata
                lsibling.elements.insert(lsibling.size(), downdata)

    def __init__(self, key= lambda x: x):
        self.root = None
        self.sortkey = key
    
    def __str__(self):
        return "BTree"+str(self.root)
    
    def find_node_position(self, data):
        path = [[self.root, None]]
        while True:
            node = path[-1][0]
            ix = node.lower_bound(data, self.sortkey)
            path[-1][1] = ix
            if ix < len(node.elements) and node.elements[ix] == data :
                ''' found the data '''
                break
            if node.is_leaf() :
                ''' reached to the leaf '''
                break
            #print(node)
            path.append([node.children[ix], None])
        return path
        
    def insert(self, data):
        if self.root == None :
            self.root = BTree.Node(data)
            return
        
        path = self.find_node_position(data)
        print("path = ", path, " data = ", data)
        node, position = path.pop()
        if position < node.size() and node.elements[position] == data :
            print(data, " found. Cancel insertion.")
            return 
        # node must be a leaf.
        node.elements.insert(position, data)
        while node.size() > self.SIZE_UPPERBOUND :
            print(path)
            if len(path) == 0 :
                # the node is the root
                print("the node is the root.", node)
                updata, left, right = node.split()
                print("updata = ", updata, "left = ", left, "right = ", right)
                self.root = BTree.Node(updata,left,right)
                left.parent = self.root
                right.parent = self.root
                break
            elif len(path) > 0 : 
                ''' node has the parent '''
                parent, ppos = path[-1]
                print("path=",path)
                print("parent = ", parent, " node = ", node)
                if node.has_rightsibling(parent, ppos) :
                    ''' has only left siblings '''
                    node.rotate_right(parent,ppos)
                    break
                elif node.has_leftsibling(parent, ppos):
                    ''' must have right siblings '''
                    node.rotate_left(parent, ppos)
                    break
                else:
                    print("no siblings with sufficient space!")
                    updata, left, right = node.split()
                    #print("split ", updata, left, ",", right)
                    # left or right is node
                    parent.insert_internal(ppos,updata,left,right)
                    #print("parent =", parent)
                    #print("parent.children =", parent.children)
                    node, ppos = path.pop()
                    