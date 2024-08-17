'''
Created on 2024/07/22

@author: sin
'''

class BTreeSet:
    MIN_CHILDREN_COUNT = 2
    
    def __init__(self, collection = None, key= lambda x: x, minsize = 2):
        self.root = None
        self.sortkey = key
        self.min_children = max(minsize, self.MIN_CHILDREN_COUNT)
        self.count = 0
        if collection != None and len(collection) :
            for e in collection:
                self.add(e)
    
    def min_keycount(self, node = None):
        if node == self.root :
            return 1
        return self.min_children - 1
    
    def max_keycount(self):
        return (self.min_children << 1) - 1
    
    class Node:
        def __init__(self, data = None, children = None):
            self.elements = list()
            if data != None :
                self.elements.append(data)
            if isinstance(children, list) :
                self.children = list(children)[:len(self.elements)+2]
            else:
                self.children = None
        
        def __str__(self):
            outstr = "("
            if self.is_leaf() :
                outstr += ", ".join(["'"+e+"'" if isinstance(e, str) else str(e) for e in self.elements])
            else:
                for i in range(self.elementcount()) :
                    outstr += str(self.children[i]) + ", " + str(self.elements[i]) + ", "
                outstr += str(self.children[-1])
            outstr += ") "
            return outstr
        
        def __repr__(self):
            return str(self.elements) #+ ", " + str(self.children)

        def __getitem__(self, x):
            return self.elements[x]

        def __setitem__(self, x, val):
            self.elements[x] = val

        def elementcount(self):
            return len(self.elements)
        
        def is_leaf(self):
            return self.children == None
        
        def right_sibling(self, parent, selfidx = None):
            if selfidx != None and parent.children[selfidx] == self :
                if 0 <= selfidx < parent.elementcount() :
                    return parent.children[selfidx+1]
                else:
                    return None
            for i in range(parent.elementcount()) :
                if parent.children[i] == self :
                    return parent.children[i+1]
            else:
                return None
                
        def left_sibling(self, parent, selfidx = None):
            if selfidx != None and parent.children[selfidx] == self :
                if 0 < selfidx <= parent.elementcount() :
                    return parent.children[selfidx - 1]
                else:
                    return None
            for i in range(1, parent.elementcount() + 1) :
                if parent.children[i] == self :
                    return parent.children[i-1]
            else:
                return None
                
        def lower_bound(self, elem, key):
            # print()
            ridx = self.elementcount()
            lidx = 0
            # cnt = 0
            while lidx < ridx :
                idx = (lidx + ridx) >> 1
                if key(self.elements[idx]) < key(elem) :
                    lidx = idx + 1
                else:
                    ridx = idx
            return ridx
    
        def insert_internal(self, ix, data, left, right):
            #print(data, ix, "left", left, "right", right)
            self.elements.insert(ix, data)
            #print("self.elements=",self.elements)
            self.children.insert(ix+1,right)
            self.children[ix] = left
            #print("add internal: ", self.elements, self.children)
            return ix
        
        def merge(self, parent, posatp):
            if parent.children[posatp] == self :
                pass
            else:
                raise ValueError("wrong posatp")
            if posatp < parent.elementcount() :
                rsibling = parent.children[posatp + 1]
                ix = posatp
                self.elements = self.elements + parent.elements[ix:ix+1] + rsibling.elements
                if not self.is_leaf() :
                    self.children = self.children + rsibling.children
                parent.elements.pop(ix)
                parent.children.pop(ix+1)
                del rsibling
            elif posatp > 0 :
                lsibling = parent.children[posatp - 1]
                ix = posatp - 1
                self.elements =  lsibling.elements + parent.elements[ix:ix+1] + self.elements
                if not self.is_leaf() :
                    self.children = lsibling.children + self.children
                parent.elements.pop(ix)
                parent.children.pop(ix)
                del lsibling
        
        def remove_leaf(self, ix):
            #print(self.elements, ix)
            self.elements.pop(ix)
            return ix
                
        
        def split(self):
            ix = self.elementcount() >> 1
            goesup = self.elements[ix]
            rsibling = BTreeSet.Node()
            rsibling.elements = self.elements[ix+1:]
            self.elements = self.elements[:ix]
            if not self.is_leaf() :
                rsibling.children = self.children[ix+1:]
                self.children = self.children[:ix+1]
            return (goesup, self, rsibling)
        
        def rotate_right(self, parent, posatp = None):
            if posatp == None :
                for i in range(parent.elementcount()+1) :
                    if parent.children[i] == self :
                        posatp = i
                        break
            rsibling = parent.children[posatp+1]
            goesup = self.elements.pop()
            goesdwn = parent.elements[posatp]
            parent.elements[posatp] = goesup
            rsibling.elements.insert(0, goesdwn)
            if not rsibling.is_leaf() :
                nephew = self.children.pop()
                rsibling.children.insert(0, nephew)
        
        def rotate_left(self, parent, posatp = None):
            if posatp == None :
                for i in range(parent.elementcount()+1) :
                    if parent.children[i] == self :
                        posatp = i
                        break
            lsibling = parent.children[posatp - 1]
            goesup = self.elements.pop(0)
            goesdwn = parent.elements[posatp-1]
            parent.elements[posatp-1] = goesup
            lsibling.elements.append(goesdwn)
            if not lsibling.is_leaf() :
                nephew = self.children.pop(0)
                lsibling.children.append(nephew)

    def __str__(self):
        return "BTreeSet"+str(self.root)
    
    def __iter__(self):
        if self.root :
            path = [[self.root, 0]]
        else:
            raise StopIteration()
        goingdown = True
        while len(path) :
            node = path[-1][0]
            ix = path[-1][1]
            if goingdown :
                if not node.is_leaf() :
                    path.append([node.children[ix], 0])
                else:
                    if ix < node.elementcount() :
                        yield node.elements[ix]
                        path[-1][1] += 1
                    else:
                        path.pop()
                        goingdown = False
            else:
                if ix < node.elementcount() :
                    yield node.elements[ix]
                    path[-1][1] += 1
                    goingdown = True
                else:
                    path.pop()

    def __len__(self) -> int :
        return self.count
    
    def __contains__(self, data) -> bool :
        if self.root == None :
            return False
        path = self.find_path(data)
        node, pos = path[-1]
        if pos < node.elementcount() :
            return path[-1][0].elements[path[-1][1]] == data
        else:
            return False
        # try:
        # except IndexError:
        #     print(path)
        #     print(path[-1][0].elementcount(),path[-1][1], data)
        #     exit(1)
    
    def hight(self) -> int:
        node = self.root
        h = 0
        while node != None and not node.is_leaf() :
            node = node.children[0]
            h += 1
        return h

    def find_last(self):
        path = [[self.root, None]]
        while path[-1][0] != None:
            if path[-1][0].is_leaf() :
                path[-1][1] = path[-1][0].elementcount() - 1
                break
            else:
                path[-1][1] = path[-1][0].elementcount()
                path.append([path[-1][0].children[-1], None])
        return path
                
    def find_path(self, data):
        path = [[self.root, None]]
        while path[-1][0] != None:
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
        
    def further_path(self, data, path):
        node, ix = path[-1]
        while not node.is_leaf() :
            node = node.children[ix]
            ix = node.lower_bound(data, self.sortkey)
            path.append([node, ix])
        return path
    
    def add(self, data):
        print("data = '{}'".format(data), type(data))
        if self.root == None :
            self.root = BTreeSet.Node(data)
            print(self.root)
            self.count = self.root.elementcount()
            return
        
        path = self.find_path(data)
        node, position = path.pop()
        if position < node.elementcount() and node.elements[position] == data :
            #print(data, " existing. Cancel insertion.")
            return
        # node must be a leaf.
        node.elements.insert(position, data)
        self.count += 1
        while node.elementcount() > self.max_keycount():
            #print("path = ", path)
            #print("temporarily over sized node = ", node)
            if len(path) == 0 :
                ''' the node is the root '''
                #print("the node is the root.", node)
                updata, left, right = node.split()
                #print("updata = ", updata, "left = ", left, "right = ", right)
                self.root = BTreeSet.Node(updata,[left,right])
                break
            elif len(path) > 0 : 
                ''' node has the parent '''
                parent, ppos = path[-1]
                
                rs = node.right_sibling(parent, ppos) 
                if rs != None and rs.elementcount() < self.max_keycount() :
                    node.rotate_right(parent,ppos)
                    break
                ls = node.left_sibling(parent, ppos)
                if ls != None and ls.elementcount() < self.max_keycount() :
                    node.rotate_left(parent, ppos)
                    break
                else:
                    #print("no siblings with sufficient space!")                    
                    updata, left, right = node.split()
                    parent.insert_internal(ppos,updata,left,right)
                    # going up
                    node, ppos = path.pop()
        return

    def remove(self, data):
        if self.root == None :
            raise KeyError(data)
        #print("to remove ", data)
        path = self.find_path(data)
        #print("searched path = ", path)
        #print("path top = ", path[-1])
        node, pos = path[-1]
        if pos >= node.elementcount() or node.elements[pos] != data :
            ''' does not contain data '''
            raise KeyError(data)
        if not node.is_leaf() :
            #print("find the leaf")
            path = self.further_path(data, path)
            leaf, lpos = path[-1]
            ''' lpos indicate the next (non-existing index) '''
            lpos -= 1
            #print("path[-1] = ", path[-1])
            ''' swap data and elements '''
            #print("swap", node[pos], leaf[lpos])
            target = node[pos]
            node[pos] = leaf[lpos]
            leaf[lpos] = target
            node = leaf
            pos = lpos 
        path.pop()
        node.remove_leaf(pos)
        self.count -= 1
        while node.elementcount() < self.min_keycount(node) :
            #print("node, elements, pos = ", node, node.elements, pos)
            #print("current path =", path)
            if node == self.root :
                #print("got an empty root", self.root.elementcount(), len(self.root.children))
                self.root = self.root.children.pop()
                if len(node.children) > 0 :
                    raise ValueError("???")
                del node
                break
            else:
                parent, posatparent = path[-1]
                #print(parent, posatparent)
            ls = node.left_sibling(parent, posatparent)
            if ls != None and ls.elementcount() > self.min_keycount() :
                #print("rr from ", ls)
                ls.rotate_right(parent, posatparent - 1)
                break
            rs = node.right_sibling(parent, posatparent)
            if rs != None and rs.elementcount() > self.min_keycount() :
                #print("rl from ", rs)
                rs.rotate_left(parent, posatparent + 1)
                break
            else:
                #print("merge", parent.elements, parent.children)
                ''' merge down '''
                node.merge(parent, posatparent)
                node, pos = path.pop()

        return
