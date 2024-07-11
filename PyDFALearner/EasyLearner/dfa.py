'''
Created on 2024/06/01

@author: Sin Shimozono
'''
import itertools
from idlelib.idle_test.test_configdialog import root

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
        sufxs = sorted(ot[2], key = lambda x: x[::-1])
        if pref in ot[0] :
            result = "".join([ot[0][pref][s] if s in ot[0][pref] else '*' for s in sufxs])
            return result
        if pref in ot[1] :
            result = ""
            result = "".join([ot[1][pref][s] if s in ot[1][pref] else '*' for s in sufxs])
            return result
        return ''.join(['*' for i in range(len(sufxs))])
    
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
        (prefdict, extdict, sufxes) = self.observationTable(exs)
        # for k in extdict:
        #     prefdict[k] = extdict[k]
        unionfind = UnionFindSet(prefdict.keys())
        if learn_debug : 
            #print(unionfind)
            pass
        
        while True:
            for row0, row1 in itertools.product(prefdict.keys(), prefdict.keys()):
                if row0 >= row1 :
                    continue
                rowstr0 = self.row_string((prefdict, extdict, sufxes), row0)
                rowstr1 = self.row_string((prefdict, extdict, sufxes), row1)
                if self.consistent(rowstr0,rowstr1) :
                    print(row0, rowstr0, row1, rowstr1, self.consistent(rowstr0,rowstr1))
                    # merge states
                    if learn_debug : 
                        print("row0 = '"+row0+"'", prefdict[row0])
                        print("row1 = '"+row1+"'", prefdict[row1] ) #, sorted(prefdict[row1].items()))
                    row01dict = self.union_rowdict(prefdict[row0], prefdict[row1])
                    prefdict.pop(row1)
                    prefdict[row0] = row01dict
                    unionfind.mergetoleft(row0, row1)
                    print(unionfind)
                    # prefitems = sorted(prefdict.items())
                    # for k, d in prefitems :
                    #     if row1 in d :
                    #         d.pop(row1)
                    if learn_debug : 
                        print("row01dict = ",sorted(row01dict.items()))
                        print("states = " + str(prefdict.keys()) )
                        print("prefdict[{}] = {}".format(row0,str(prefdict[row0])))
                        print()
                    break
            else:
                break
        print("prefdict = ",prefdict)
        self.states = set(prefdict.keys())
        #define transfer function
        for s in prefdict :
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
            if s in prefdict and '' in prefdict[s] and prefdict[s][''] == self.POSITIVE :
                self.acceptingStates.add(s)
        return (prefdict, extdict, sufxes)
    
    def observationTable(self, exs):
        prefdict = dict()
        extdict = dict()
        suffixes = set()
        for xs, xc in exs :
            for i in range(0, len(xs)+1):
                # s 
                prefx = xs[:i]
                sufx = xs[i:]
                suffixes.add(sufx)
                if not prefx in prefdict :
                    prefdict[prefx] = dict()
                if sufx in prefdict[prefx] and prefdict[prefx] != xc:
                    print("error: a contradicting example, ", xs, xc)
                    return 
                prefdict[prefx][sufx] = xc
                #print('"'+prefx+'"', '"'+sufx+'"', xc)
                
                # s.a
                for a in self.alphabet :
                    if prefx + a in prefdict :
                        extdict[prefx + a] = prefdict[prefx+a]
                    else:
                        extdict[prefx + a] = dict()
        # if '' not in prefdict :
        #     prefdict[''] = dict()
        print("ovtbl = ")
        sufexs = sorted(suffixes, key = lambda x: x[::-1] )
        print(sufexs)
        for key in sorted(prefdict.keys()):
            print(" {0:8} ".format(key), end="")
            for s in sufexs:
                if s in prefdict[key]:
                    print(prefdict[key][s],end="")
                else:
                    print("*",end="")
            print()
        print("-----")
        for key in sorted(extdict):
            print(" {0:8} ".format(key[:-1]+"."+key[-1:]), end="")
            for s in sufexs:
                if s in extdict[key]:
                    print(extdict[key][s],end="")
                else:
                    print("*",end="")
            print()
        print()
        return (prefdict, extdict, suffixes)
    
    def commonPrefix(self, str1, str2):
        preflen = 0
        while preflen < min(len(str1), len(str2)) and str1[preflen] == str2[preflen] : 
            preflen += 1
        return str1[:preflen]
    