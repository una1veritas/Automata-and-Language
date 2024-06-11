#!/usr/local/bin/python2.7
# encoding: utf-8
'''
SimpleLearner.__main__ -- shortdesc

SimpleLearner.__main__ is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2024 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys

class DFA():
    # DFA class constant
    initial_state = ''
    
    def __init__(self):
        self.falphabet = set()
        self.states = set()
        self.transfunc = dict() # a key is a pair (tuple) of strings, which can be hashed
        self.finals = set()
        self.rejects = set() #
        
        self.states.add(DFA.initial_state)
        self.current = DFA.initial_state
#

    def state_initialize(self):
        self.current = DFA.initial_state
#
    def transfer(self, st, ch):
        if (st, ch) in self.transfunc :
            return self.transfunc[(st,ch)]
        return NONE
#
    def learn(self, anex :str, exclass : bool):
        self.state_initialize()
        for i in range(len(anex)) :
            c = anex[i]
            if c not in self.falphabet:
                self.falphabet.add(c)
            if (self.current, c) in self.transfunc :
                self.current = self.transfer(self.current, c)
            else:
                newstate = anex[:i+1]
                self.transfunc[(self.current,c)] = newstate
                self.states.add(newstate)
                self.current = newstate
                #print(self)
        if exclass :
            if self.current in self.rejects :
                print("Error: supersade by contradicting example " + anex + ", " + bool)
                self.rejects.delete(self.current)
            self.finals.add(self.current)
        else:
            if self.current in self.finals :
                print("Error:  supersade by contradicting example " + anex + ", " + bool)
                self.finals.delete(self.current)
            self.rejects.add(self.current)
#    def __repr__(self):
#        return reprstr

    def __str__(self):
        outstr = "DFA("+str(sorted(self.states)) + ", \n"
        for a,v in self.transfunc.items() :
            outstr += str(a) + " -> " + str(v) + "\n"
        outstr += "finals = " + str(sorted(self.finals)) + " "
        outstr += "rejects = " + str(sorted(self.rejects)) + ") "
        return outstr
#    

def DFA_learn(exs):
    fsm = DFA()
    #print(fsm)
    for ex, exclass in exs.items():
        #print(ex, exclass)
        fsm.learn(ex, exclass == '+')
        #print()
    print(fsm)

if __name__ == '__main__' :
    examples = dict()
    for ex in sys.argv[1:] :
        exstr, exclass = ex.split(',')
        if exclass == '+' :
            examples[exstr] = '+'
        elif exclass == '-' :
            examples[exstr] = '-'
    print(examples)
    DFA_learn(examples)