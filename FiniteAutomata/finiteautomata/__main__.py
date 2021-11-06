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

    def searchtuple(self, singlestate, symbol):
        left = 0
        right = len(self.transition)
        counter = 0
        while right != left :
            ix = left + ((right - left)>>1)
            print(left,right,ix)
            t = self.transition[ix]
            if t[:2] >= (state, symbol) :
                right = ix
            elif t[:2] < (state, symbol) :
                left = ix + 1
            # if counter > 10:
            #     break
            # else:
            #     counter += 1
        if (state, symbol) == self.transition[left][:2] :
            collection = set()
            for i in range(left,len(self.transition)):
                collection.add(self.transition[i][2])
        return collection
            
    def transfer(self,state,symbol):
        if not isinstance(state,set) :
            state = set([state])
            if len(collection) == 1 :
                return collection.pop()
            elif len(collection) > 1 :
                return collection
        return None
    
    def run(self,inputstr):
        self.reset()
        print('{}'.format(self.currentstate),end='')
        for symb in inputstr:
            if isinstance(self.currentstate,set):
                
            else:
                self.currentstate = self.transfer(self.currentstate, symb)
                print(' -{}-> {} '.format(symb, self.currentstate),end='')
        return self.currentstate in self.finals
        
if __name__ == '__main__':
    fa = FiniteAutomata('01', 'ab', [('0','a','0'),('0','a','1'),('0','a','2'),('0','b','1'),('0','b','2'),('1','a','0'),('1','a','1'),('1','a','2'),('1','b','0'),('1','b','1')],'0','1')
    print(fa)
    print(fa.run('aabab'))