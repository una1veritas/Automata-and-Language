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
    
class OvserbationTable(object):
    EMPTYSTRING = ''
    
    def __init__(self):
        self.rows = dict()
        self.rows[self.EMPTYSTRING] = dict()
        self.extends = set()
        self.suffixes = set()
        self.suffixes.add(self.EMPTYSTRING)
    
    def __str__(self)->str:
        suflist = sorted(self.suffixes, key = lambda x: x[::-1] )
        result =  "OvserbationTable(\n" + str(suflist) 
        result += ", \n"
        for prefix in self.rows :
            result += " {0:8} ".format(prefix)
            result += self.row_string(prefix) + '\n'
        result += ", {" + str(self.extends) + "}"
        result += ")"
        return result
    
    def observe(self, falphabet, exstring, exclass):
        for i in range(0, len(exstring)+1):
            prefix = exstring[:i]
            suffix = exstring[i:]
            if prefix not in self.rows :
                self.rows[prefix] = dict()
            self.rows[prefix][suffix] = exclass
            self.suffixes.add(suffix)  # duplicate addition will be ignored. 
            for a in falphabet :
                if prefix + a not in self.rows :
                    self.extends.add(prefix+a)
    
    def row_string(self, pref):
        suflist = sorted(self.suffixes, key = lambda x: x[::-1])
        if pref in self.rows :
            result = "".join([self.rows[pref].get(s, '*') for s in suflist])
            return result
        return ''.join(['*' for i in range(len(suflist))])
    
    def consistent(self, pref1, pref2):
        for c1, c2 in zip(self.row_string(pref1), self.row_string(pref2)) :
            if c1 == c2 :
                continue
            if c1 == "*" or c2 == "*" :
                continue
            return False
        return True
    
    def is_prefix_complete(self):
        S = set(self.rows.keys()).union(self.extends)
        prefixes = set(self.rows.keys())
        print("S=",S)
        removed = set()
        while len(prefixes) > 0:
            n = len(prefixes)
            for longest in sorted(S, key = lambda x: len(x), reverse=True) :
                for i in range(0,len(longest)+1):
                    pfx = longest[:i]
                    if pfx in prefixes :
                        prefixes.remove(pfx)
                        removed.add(pfx)
                    elif pfx not in removed :
                        return False
            if len(prefixes) == n :
                break
        return True
                
    def is_suffix_complete(self):
        suffxs = self.suffixes
        removed = set()
        while len(suffxs) > 0:
            n = len(suffxs)
            for longest in sorted(suffxs, key = lambda x: len(x), reverse=True) :
                for i in range(0,len(longest)+1):
                    sfx = longest[i:]
                    if sfx in suffxs :
                        suffxs.remove(sfx)
                        removed.add(sfx)
                    elif sfx not in removed :
                        return False
            if len(suffxs) == n :
                break
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
        ovstable = OvserbationTable()
        for exs, exc in exs :
            ovstable.observe(self.alphabet, exs, exc)
            print(exs, exc)
            print(ovstable)
            if ovstable.is_prefix_complete() :
                print("prefix complete!")
            if ovstable.is_suffix_complete() :
                print("suffix complete!")
            print()
        print()
        ovstable.is_prefix_complete()
        return
        # for k in extdict:
        #     prefdict[k] = extdict[k]
        unionfind = UnionFindSet(prefixrows.keys())
        if learn_debug : 
            #print(unionfind)
            pass
         
        print("rows = ", prefixrows)
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
        #         rowstr0 = self.row_string((rows, prefixes, suffixes), row0)
        #         rowstr1 = self.row_string((rows, prefixes, suffixes), row1)
        #         if self.consistent(rowstr0, rowstr1) :
        #             print(row0, rowstr0, row1, rowstr1, self.consistent(rowstr0,rowstr1))
        #             # merge states
        #             if learn_debug : 
        #                 print("row0 = '"+row0+"'", rows[row0])
        #                 print("row1 = '"+row1+"'", rows[row1] ) #, sorted(prefdict[row1].items()))
        #             row01dict = self.union_rowdict(rows[row0], rows[row1])
        #             rows.pop(row1)
        #             rows[row0] = row01dict
        #             unionfind.mergetoleft(row0, row1)
        #             print(unionfind)
        #             # prefitems = sorted(prefdict.items())
        #             # for k, d in prefitems :
        #             #     if row1 in d :
        #             #         d.pop(row1)
        #             if learn_debug : 
        #                 print("row01dict = ",sorted(row01dict.items()))
        #                 print("states = " + str(prefixes) )
        #                 print("rows[{}] = {}".format(row0,str(rows[row0])))
        #                 print()
        #             break
        #     else:
        #         break
        return (rows, prefixes, suffixes)
    