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
            
    def transfer(self,state,symbol):
        if not isinstance(state,set):
            state = set([state])
        nextstate = set()
        for each in state:
            left = 0
            right = len(self.transition)
            counter = 0
            while right != left :
                ix = left + ((right - left)>>1)
                #print(left,right,ix)
                t = self.transition[ix]
                if t[:2] >= (each, symbol) :
                    right = ix
                elif t[:2] < (each, symbol) :
                    left = ix + 1
                # if counter > 10:
                #     break
                # else:
                #     counter += 1
            if left >= len(self.transition):
                #print(left)
                continue
            #print('left',left, self.transition[left])
            if (each, symbol) == self.transition[left][:2] :
                for ix in range(left,len(self.transition)):
                    if (each, symbol) == self.transition[ix][:2] :
                        nextstate.add(self.transition[ix][2])
            #print('nextstate=',nextstate)
        if len(nextstate) == 1:
            nextstate = nextstate.pop()
        return nextstate
    
    def run(self,inputstr):
        self.reset()
        print('{}'.format(self.currentstate),end='')
        for symb in inputstr:
            self.currentstate = self.transfer(self.currentstate, symb)
            print(' -{}-> {} '.format(symb, self.currentstate),end='')
        if isinstance(self.currentstate, set) :
            return bool(self.currentstate.intersection(self.finals))
        else:
            return self.currentstate in self.finals
        
if __name__ == '__main__':
    fa = FiniteAutomata('0123', 'ab', [('0','a','0'),('0','b','0'),('0','a','1'),('1','a','2'),('2','b','3'),('3','a','3'),('3','b','3')],'0','3')
    print(fa)
    print(fa.run('aababba'))