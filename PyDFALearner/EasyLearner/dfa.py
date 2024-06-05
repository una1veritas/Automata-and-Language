'''
Created on 2024/06/01

@author: Sin Shimozono
'''
from pickle import TRUE
from numpy.core.numeric import False_

class DFA(object):
    '''
    classdocs
    '''
    INITIAL_STATE_NAME = ''
    POSITIVE_LABEL = '+'
    NEGATIVE_LABEL = '-'
    UNDEFINED_LABEL = '0'

    def __init__(self, falphabet = ''):
        '''
        definitions
        '''
        self.alphabet = set()
        if falphabet != self.INITIAL_STATE_NAME :
            for c in str(falphabet) :
                self.alphabet.add(c)
        self.initialState = ''
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
        return self.UNDEFINED_LABEL

    def learn(self, exs : dict()):
        for exstr, exclass in exs.items() :
            self.initiate()
            print(exstr, exclass)
            if not (exclass == self.POSITIVE_LABEL or exclass == self.NEGATIVE_LABEL) :
                print("Error: invalid class label for an example: "+exstr +", " +exclass)
                print("Skip this example.")
                continue 
            for pos in range(len(exstr)) :
                c = exstr[pos]
                if c not in self.alphabet :
                    self.alphabet.add(c)
                if not self.defined(self.current, c) :
                    newstate = self.current + c
                    self.transfunc[(self.current, c)] = newstate
                    self.states.add(newstate)
                    self.transfunc[(newstate, "")] = self.UNDEFINED_LABEL
                self.current = self.transfunc[(self.current, c)]
            if self.transfer(self.current, "") == self.UNDEFINED_LABEL :
                if exclass == self.POSITIVE_LABEL :
                    self.transfunc[(self.current, "")] = self.POSITIVE_LABEL
                else:
                    self.transfunc[(self.current, "")] = self.NEGATIVE_LABEL
            else:
                print(self.current, c, self.transfer(self.current, c))
                if self.transfer(self.current, "") != (exclass == self.POSITIVE_LABEL) :
                    print("Error: a contradicting example: " + exstr + ", " +exclass)
                    return 
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
    