'''
Created on 2024/06/01

@author: Sin Shimozono
'''
import itertools

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
    
class DFA(object):
    '''
    classdocs
    '''
    INITIAL_STATE = ''
    POSITIVE = '+'
    NEGATIVE = '0'
    UNDEFINED = '-'

    def __init__(self, falphabet = ''):
        '''
        the definitions of the initial empty automata 
        accepts no strings
        '''
        self.alphabet = set()
        if len(falphabet) > 0 :
            for c in str(falphabet) :
                self.alphabet.add(c)
        self.initialState = self.INITIAL_STATE
        self.states = set()
        self.states.add(self.initialState)
        self.transfunc = dict()
        self.acceptingStates = set()
        '''
        computing mechanizm
        '''
        self.current = self.initialState
        
    def __str__(self):
        return "DFA('alphabet = " + ''.join(sorted(self.alphabet)) + "', \n states = {" \
            + ', '.join([ s if len(s) > 0 else "'"+s+"'" for s in sorted(self.states)]) + "}, \n initial = '" + str(self.initialState) + "', \n" \
            + " transition = {" + ', '.join(sorted(["{} -> {}".format(k, v) if len(v) > 0 else "{} -> '{}'".format(k, v) for k, v in self.transfunc.items()])) \
            + "}, \n finals = " + str(self.acceptingStates) + ")"
        
    def initiate(self):
        self.current = self.initialState
    
    def isAccept(self, q) -> bool:
        return (q in self.acceptingStates)
    
    def defined(self, q, c):
        if (q, c) in self.transfunc :
            return True
        return False
    
    def transfer(self, q, c):
        if (q,c) in self.transfunc :
            return self.transfunc[(q, c)]
        return self.UNDEFINED
    
    def row_string(self, ot, pref):
        rows, prefs, sufs = ot
        sufslist = sorted(sufs, key = lambda x: x[::-1])
        if pref in rows :
            result = "".join([rows[pref][s] if s in rows[pref] else '*' for s in sufslist])
            return result
        return ''.join(['*' for i in range(len(sufslist))])
    
    def consistent(self, left, right):
        if len(left) != len(right) :
            return False
        for i in range(len(left)) :
            if right[i] == left[i] :
                continue
            else:
                if left[i] == "*" or right[i] == "*" :
                    continue
                else:
                    return False
        return True
    
    def union_rowdict(self, ldict, rdict):
        unified = dict()
        for k in set(ldict.keys()).union(set(rdict.keys())) :
            l, r = ldict.get(k), rdict.get(k)
            if l == None :
                unified[k] = rdict[k]
            elif r == None :
                unified[k] = ldict[k]
            else:
                if rdict[k] == ldict[k] :
                    unified[k] = ldict[k]
                else:
                    unified[k] = "*"
        return unified
        
    
    def learn(self, exs):
        learn_debug = True
        for xm, clabel in exs:
            for c in xm:
                self.alphabet.add(c)
        (rows, prefixes, suffixes) = self.observationTable(exs)
        # for k in extdict:
        #     prefdict[k] = extdict[k]
        unionfind = UnionFindSet(prefixes)
        if learn_debug : 
            #print(unionfind)
            pass
         
        while True:
            for row0, row1 in itertools.product(prefixes, prefixes):
                if row0 >= row1 :
                    continue
                rowstr0 = self.row_string((rows, prefixes, suffixes), row0)
                rowstr1 = self.row_string((rows, prefixes, suffixes), row1)
                if self.consistent(rowstr0, rowstr1) :
                    print(row0, rowstr0, row1, rowstr1, self.consistent(rowstr0,rowstr1))
                    # merge states
                    if learn_debug : 
                        print("row0 = '"+row0+"'", rows[row0])
                        print("row1 = '"+row1+"'", rows[row1] ) #, sorted(prefdict[row1].items()))
                    row01dict = self.union_rowdict(rows[row0], rows[row1])
                    rows.pop(row1)
                    rows[row0] = row01dict
                    unionfind.mergetoleft(row0, row1)
                    print(unionfind)
                    # prefitems = sorted(prefdict.items())
                    # for k, d in prefitems :
                    #     if row1 in d :
                    #         d.pop(row1)
                    if learn_debug : 
                        print("row01dict = ",sorted(row01dict.items()))
                        print("states = " + str(prefixes) )
                        print("rows[{}] = {}".format(row0,str(rows[row0])))
                        print()
                    break
            else:
                break
        print("rows = ", rows)
        self.states = set(rows.keys())
        #define transfer function
        for s in rows :
            for a in self.alphabet :
                eqvstate = unionfind.find(s+a)
                if eqvstate != None:
                    print("transfunc[{},{}] -> {}".format(s,a,eqvstate))
                    self.transfunc[(s,a)] = eqvstate
                else:
                    print("not defined: ({}, {})".format(s, a))
                    # print("open {},{} -> {}".format(s,a,s+a))
                    for st in self.states :
                        if st not in self.acceptingStates :
                            self.transfunc[(s,a)] = st
                            print("force ({}, {}) -> {}".format(s,a,st))
                            break
                    #         print("transfunc[{},{}] -> {}".format(s,a,st))
                    # else:
                    #     self.transfunc[(s,a)] = s+a
                    #     print("transfunc[{},{}] -> {}".format(s,a,s+a))
                    #     for a in self.alphabet :
                    #         self.transfunc[(s+a,a)] = s+a
                    #         print("transfunc[{},{}] -> {}".format(s+a,a,s+a))
        for s in self.states :
            if s in rows and '' in rows[s] and rows[s][''] == self.POSITIVE :
                self.acceptingStates.add(s)
        return (rows, prefixes, suffixes)
    
    def observationTable(self, exs):
        rows = dict()
        prefixes = set()
        suffixes = set()
        for xs, xc in exs :
            for i in range(0, len(xs)+1):
                # s 
                prefix = xs[:i]
                suffix = xs[i:]
                prefixes.add(prefix) # duplicate addition will be ignored. 
                suffixes.add(suffix)  # duplicate addition will be ignored. 
                if not prefix in rows :
                    rows[prefix] = dict()
                if suffix in rows[prefix] and rows[prefix][suffix] != xc:
                    print("error: a contradicting example, ", xs, xc)
                    return None 
                rows[prefix][suffix] = xc
                #print('"'+prefix+'"', '"'+suffix+'"', xc)
                # s.a
                for a in self.alphabet :
                    if not prefix + a in rows :
                        rows[prefix + a] = dict()
                    # if not a + suffix in suffixes :
                    #     suffixes.add(a+suffix)
                
        print("ovtbl = ")
        sufexs = sorted(suffixes, key = lambda x: x[::-1] )
        print(sufexs)
        for key in sorted(rows.keys()):
            if not key in prefixes :
                continue
            print(" {0:8} ".format(key), end="")
            for s in sufexs:
                if s in rows[key]:
                    print(rows[key][s],end="")
                else:
                    print("*",end="")
            print()
        print("-----")
        for key in sorted(rows.keys()):
            if key in prefixes :
                continue
            print(" {0:8} ".format(key[:-1]+"."+key[-1:]), end="")
            for s in sufexs:
                if s in rows[key]:
                    print(rows[key][s],end="")
                else:
                    print("*",end="")
            print()
        print()
        return (rows, prefixes, suffixes)
    
    def commonPrefix(self, str1, str2):
        preflen = 0
        while preflen < min(len(str1), len(str2)) and str1[preflen] == str2[preflen] : 
            preflen += 1
        return str1[:preflen]
    