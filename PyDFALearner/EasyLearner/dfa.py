'''
Created on 2024/06/01

@author: Sin Shimozono
'''
import itertools
from pickle import FALSE

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
    
class ObservationTable(object):
    EMPTYSTRING = ''
    
    def __init__(self, finitealphabet):
        self.alphabet = set(finitealphabet)
        self.prefixes = set()
        self.rows = dict()
        self.rows[self.EMPTYSTRING] = dict()
        self.suffixes = set()
        self.suffixes.add(self.EMPTYSTRING)
    
    def __str__(self)->str:
        suflist = sorted(self.suffixes, key = lambda x: x[::-1] )
        result =  "ObservationTable(" \
        + "'" + ''.join(sorted(self.alphabet)) + "', " \
        + "\n" + str(suflist) 
        result += ", [\n"
        for pfx in self.prefixes :
            result += " {0:8} ".format(pfx)
            result += self.row_string(pfx) + '\n'
        result += "--------\n"
        for pfx in set(self.rows.keys()) - self.prefixes :
            result += " {0:8} ".format(pfx)
            result += self.row_string(pfx) + '\n'
        result += "])"
        return result
    
    def extend(self, xstr, xclass):
        for i in range(0, len(xstr)+1):
            pfx = xstr[:i]
            sfx = xstr[i:]
            self.suffixes.add(sfx)  # duplicate addition will be ignored. 
            if pfx in self.rows :
                self.rows[pfx][sfx] = xclass
            else:
                self.rows[pfx] = dict()
                self.rows[pfx][sfx] = xclass
            
            if len(pfx) > 0 :
                for a in self.alphabet :
                    if pfx[:-1] + a not in self.rows :
                        break
                else:
                    #print("move ", pfx[:-1])
                    if pfx[:-1] in self.rows :
                        self.prefixes.add(pfx[:-1])
    
    
    def row_string(self, pfx):
        suflist = sorted(self.suffixes, key = lambda x: x[::-1])
        if pfx in self.rows :
            result = "".join([self.rows[pfx].get(s, '*') for s in suflist])
            return result
        return ''.join(['*' for i in range(len(suflist))])
    
    def consistent_rows(self, s1, s2):
        row1 = self.rows.get(s1, None)
        row2 = self.rows.get(s2, None)
        if row1 is None or row2 is None :
            return False
        #print("prefix {}, {}".format(row1, row2))
        for e in self.suffixes:
            if (e in row1 and e in row2) and row1[e] != row2[e] :
                return False
        return True
    
    def closed(self):
        for t in set(self.rows.keys()) - self.prefixes :
            for s in self.prefixes :
                if self.consistent_rows(t, s) :
                    break
            else:
                return False
        return True
    
    def consistent(self):
        if len(self.prefixes) == 0 :
            return False
        for s1, s2 in itertools.product(self.prefixes, self.prefixes) :
            if s1 >= s2:
                continue
            if self.consistent_rows(s1, s2):
                #print("consistency chk:")
                for a in self.alphabet :
                    if not self.consistent_rows(s1+a, s2+a) :
                        return False
                #print("passed", s1, s2)
        return True
    
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
        
    def learn(self, exs):
        learn_debug = True
        for xm, clabel in exs:
            for c in xm:
                self.alphabet.add(c)
        obtable = ObservationTable(self.alphabet)
        print()
        for exs, exc in exs :
            obtable.extend(exs, exc)
            print("'{}', {}".format(exs,exc))
            print(obtable)
            print("closed" if obtable.closed() else "not closed", ",", "consistent" if obtable.consistent() else "not consistent")
            print()
        else:
            if not (obtable.consistent() and obtable.closed() ) :
                print("DFA is not constructable")
                return
        print()
        print("DFA is constructable by ")
        print(obtable)
        return
        # for k in extdict:
        #     prefdict[k] = extdict[k]
        unionfind = UnionFindSet(prefixrows.keys())
        if learn_debug : 
            #print(unionfind)
            pass
         
        print("prefixes = ", prefixrows)
        self.states = set(prefixrows.keys())
        #define transfer function
        for a_state in sorted(sorted(self.states), key = lambda x : len(x)) :
            if '' in prefixrows[a_state] and prefixrows[a_state][''] == self.POSITIVE :
                self.acceptingStates.add(a_state)
            for a in self.alphabet :
                if a_state + a in prefixrows and '' in prefixrows[a_state+a] :
                    self.transfunc[a_state, a] = prefixrows[a_state+a]['']
                else:
                    # find some consistent state/prefix
                    constate = self.consistent_with((prefixrpws, suffixes), a_state+a)
        return 
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
        # while True:
        #     for row0, row1 in itertools.product(prefixes, prefixes):
        #         if row0 >= row1 :
        #             continue
        #         rowstr0 = self.row_string((prefixes, prefixes, suffixes), row0)
        #         rowstr1 = self.row_string((prefixes, prefixes, suffixes), row1)
        #         if self.consistent(rowstr0, rowstr1) :
        #             print(row0, rowstr0, row1, rowstr1, self.consistent(rowstr0,rowstr1))
        #             # merge states
        #             if learn_debug : 
        #                 print("row0 = '"+row0+"'", prefixes[row0])
        #                 print("row1 = '"+row1+"'", prefixes[row1] ) #, sorted(prefdict[row1].items()))
        #             row01dict = self.union_rowdict(prefixes[row0], prefixes[row1])
        #             prefixes.pop(row1)
        #             prefixes[row0] = row01dict
        #             unionfind.mergetoleft(row0, row1)
        #             print(unionfind)
        #             # prefitems = sorted(prefdict.items())
        #             # for k, d in prefitems :
        #             #     if row1 in d :
        #             #         d.pop(row1)
        #             if learn_debug : 
        #                 print("row01dict = ",sorted(row01dict.items()))
        #                 print("states = " + str(prefixes) )
        #                 print("prefixes[{}] = {}".format(row0,str(prefixes[row0])))
        #                 print()
        #             break
        #     else:
        #         break
        return (rows, prefixes, suffixes)
    