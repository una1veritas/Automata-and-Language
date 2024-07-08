'''
Created on 2024/06/01

@author: Sin Shimozono
'''
import itertools

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
    
    def unified_rowdict(self, ldict, rdict):
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
        learn_debug = False
        for xm, clabel in exs:
            for c in xm:
                self.alphabet.add(c)
        (prefdict, extdict, sufxes) = self.observationTable(exs)
        
        idtfytbl = dict()
        for k in prefdict:
            idtfytbl[k] = k
        if learn_debug : print(idtfytbl)
        
        while True:
            for row0, row1 in itertools.product(prefdict.keys(), prefdict.keys()):
                rowstr0 = self.row_string((prefdict, extdict, sufxes), row0)
                rowstr1 = self.row_string((prefdict, extdict, sufxes), row1)
                if row0 >= row1 :
                    continue
                #print(row0, rowstr0, row1, rowstr1, self.consistent(rowstr0,rowstr1))
                if self.consistent(rowstr0,rowstr1) :
                    # merge states
                    if learn_debug : 
                        print("'"+row0+"', '"+row1+"'", "-> ", end="" ) #, sorted(prefdict[row1].items()))
                    row01dict = self.unified_rowdict(prefdict[row0], prefdict[row1])
                    prefdict.pop(row1)
                    prefdict[row0] = row01dict
                    idtfytbl[row1] = row0
                    for k in idtfytbl:
                        if idtfytbl[k] == row1 :
                            idtfytbl[k] = row0
                    # prefitems = sorted(prefdict.items())
                    # for k, d in prefitems :
                    #     if row1 in d :
                    #         d.pop(row1)
                    if learn_debug : 
                        print("'"+row0+"'", sorted(row01dict.items()))
                        print(idtfytbl)
                        print()
                    break
            else:
                break
        self.states = set(prefdict.keys())
        if '' in self.states :
            self.initialState = ''
        else:
            print("no initial state error")
            return None
        for s in prefdict :
            if idtfytbl[s] != s : continue
            for a in self.alphabet :
                if s+a in idtfytbl :
                    self.transfunc[(s,a)] = idtfytbl[s + a]
                else:
                    self.transfunc[(s,a)] = s + a
        for s in self.states :
            if prefdict[s][''] == self.POSITIVE :
                self.acceptingStates.add(s)
        return (prefdict, extdict, sufxes)
    
    def observationTable(self, exs):
        prefdict = dict()
        extdict = dict()
        sufxes = set()
        for exstr, exclass in exs :
            for i in range(0, len(exstr)+1):
                # s 
                prefx = exstr[:i]
                sufx = exstr[i:]
                sufxes.add(sufx)
                if not prefx in prefdict :
                    prefdict[prefx] = dict()
                if prefx in extdict:
                    row_dict = extdict.pop(prefx)
                    for k, v in row_dict.items() :
                        prefdict[prefx][k] = v
                if sufx in prefdict[prefx] and prefdict[prefx] != exclass:
                    print("error: a contradicting example, ", exstr, exclass)
                    return 
                prefdict[prefx][sufx] = exclass
                #print('"'+prefx+'"', '"'+sufx+'"', exclass)
                
                # s.a
                for a in self.alphabet :
                    if prefx + a not in prefdict :
                        extdict[prefx + a] = dict()
                    
        print("ovtbl = ")
        sufexs = sorted(sufxes, key = lambda x: x[::-1] )
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
        return (prefdict, extdict, sufxes)
    
    def commonPrefix(self, str1, str2):
        preflen = 0
        while preflen < min(len(str1), len(str2)) and str1[preflen] == str2[preflen] : 
            preflen += 1
        return str1[:preflen]
    