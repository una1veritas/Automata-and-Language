'''
Created on 2024/06/01

@author: Sin Shimozono
'''

import sys
from dfa import DFA

if __name__ == '__main__':
    '''有限アルファベットのみを定義'''
    dfa1 = DFA(sys.argv[1])

    dfa1.learn_by_mat()
    print(dfa1)
    
    print('finished.')