'''
Created on 2024/06/01

@author: Sin Shimozono
'''

import sys
from dfa import DFA

if __name__ == '__main__':
    '''有限アルファベットのみを定義'''
    falphabet = "ab"
    if len(sys.argv) >= 2 :
        falphabet = sys.argv[1]
    dfa1 = DFA(falphabet)

    dfa1.learn_by_mat()
    print(dfa1)
    
    print('finished.')