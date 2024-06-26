'''
Created on 2024/06/01

@author: Sin Shimozono
'''


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
        definitions
        '''
        self.alphabet = set()
        if len(falphabet) > 0 :
            for c in str(falphabet) :
                self.alphabet.add(c)
        self.initialState = self.INITIAL_STATE
        self.states = set()
        self.states.add(self.initialState)
        self.transfunc = dict()
        '''
        computing mechanizm
        '''
        self.current = self.initialState
        
    def __str__(self):
        return "DFA('" + ''.join(sorted(self.alphabet)) + "', {" \
            + ', '.join(sorted(self.states)) + "}, initial = '" + str(self.initialState) + "', \n" \
            + "transition = {" + ', '.join(sorted(["{} -> {}".format(k, v) for k, v in self.transfunc.items() if k[1] != ''])) \
            + "}, \n" + "finals = " + str(set([s for s in self.states if self.isAccept(s)])) + ")"
        
    def initiate(self):
        self.current = self.initialState
    
    def isAccept(self, q) -> bool:
        return self.transfer(q, '') == True
    
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
    
    def specificThan(self, left, right):
        if len(left) != len(right) :
            return False
        for i in range(len(left)) :
            if right[i] == '*' :
                continue
            else:
                if left[i] == right[i] :
                    continue
                else:
                    return False
        return True
    
    def learn(self, exs):
        for xm, cl in exs:
            for c in xm:
                self.alphabet.add(c)
        ot = self.observationTable(exs)
        for k in ot[0]:
            print(self.row_string(ot, k))
        return ot
    
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
    
    def minimize(self):
        print("debug: minimize")
        ovtable = list()
        alphindex = [''] + sorted(self.alphabet)
        for q in self.states :
            t = list()
            for c in alphindex :
                t.append(self.transfer(q, c))
            ovtable.append((q, t))
        for e in sorted(ovtable, key=lambda x: x[1]): print(e)
        
    def commonPrefix(self, str1, str2):
        preflen = 0
        while preflen < min(len(str1), len(str2)) and str1[preflen] == str2[preflen] : 
            preflen += 1
        return str1[:preflen]
    