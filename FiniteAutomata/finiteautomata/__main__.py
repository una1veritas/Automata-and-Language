'''
Created on 2021/11/06

@author: Sin Shimozono
'''
from _tracemalloc import start
from numpy import ix_

class FiniteAutomata:
    def __init__(self, states, alphabet, transition, start, finals):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transition = list()
        if isinstance(transition,dict):
            for k in transition:
                self.transition.append(k, transition[k])
        elif isinstance(transition,(list,set)):
            for ea in transition:
                self.transition.append(tuple(ea))
        else:
            raise TypeError('process for this type still undefined')
        self.transition = sorted(self.transition)
        if start in self.states :
            self.start = start
        else:
            raise RuntimeError('start state is not in states')
        finals = set(finals)
        if finals <= self.states :
            self.finals = finals
        else:
            raise RuntimeError('final states includes one not in states')
        self.reset()
        
    def reset(self):
        self.currentstate = self.start
    
    def __str__(self):
        t= 'FiniteAutomata('
        t += str(self.states)
        t += ', '
        t += str(self.alphabet)
        t += ', '
        t += str(self.transition)
        t += ', '
        t += str(self.start)
        t += ', '
        t += str(self.finals)
        t += ')'
        return t

    def trans(self,state,symbol):
        left = 0
        right = len(self.transition)
        while right - left > 0 :
            ix = left + (right - left)>>1
            #print(left,right,ix)
            t = self.transition[ix]
            if (state, symbol) < t[:2] :
                right = ix
            elif (state, symbol) > t[:2] :
                left = ix + 1
            else:
                return t[2]
        return None
            
        
if __name__ == '__main__':
    fa = FiniteAutomata('01', 'ab', [('0','a','0'), ('0','b','1'),('1','a','0'),('1','b','1')],'0','1')
    print(fa)
    print(fa.trans('0', 'c'))