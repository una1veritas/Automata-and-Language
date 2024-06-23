'''
Created on 2024/06/01

@author: Sin Shimozono
'''
from pandas.io.formats.info import _DataFrameInfoPrinter

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

    def learn(self, exs):
        for x in exs:
            for c in x[0]:
                self.alphabet.add(c)
                
        self.observe(exs)
        return 
    
    def observe(self, exs):
        ovtbl = dict()
        prfxes = set()
        extnds = set()
        for exstr, exclass in exs :
            for i in range(0, len(exstr)+1):
                # s 
                prefx = exstr[:i]
                sufx = exstr[i:]
                if not prefx in ovtbl :
                    ovtbl[prefx] = dict()
                    prfxes.add(prefx)
                if prefx in extnds:
                    extnds.remove(prefx)
                    prfxes.add(prefx)
                if sufx in ovtbl[prefx] and ovtbl[prefx] != exclass:
                    print("error: a contradicting example, ", exstr, exclass)
                    return 
                ovtbl[prefx][sufx] = exclass
                # s.a
                for a in self.alphabet :
                    if prefx + a not in ovtbl :
                        extnds.add(prefx + a)
                        ovtbl[prefx + a] = dict()
                    
        print("ovtbl = ")
        #print(prfxes)
        #print(extnds)
        sufexs = sorted([k for k in ovtbl.keys()], key = lambda x: x[::-1] )
        print(sufexs)
        for key in sorted(prfxes):
            print(" {0:8} ".format(key), end="")
            for s in sufexs:
                if s in ovtbl[key]:
                    print(ovtbl[key][s],end="")
                else:
                    print("*",end="")
            print()
        print("-----")
        for key in sorted(extnds):
            print(" {0:>8} ".format(key), end="")
            for s in sufexs:
                if s in ovtbl[key]:
                    print(ovtbl[key][s],end="")
                else:
                    print("*",end="")
            print()
        print()
        return
    
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
    