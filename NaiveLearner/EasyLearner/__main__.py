'''
Created on 2024/06/01

@author: Sin Shimozono
'''

import sys
from EasyLearner.dfa import DFA

if __name__ == '__main__':
    examples = dict()
    print(sys.argv)
    if len(sys.argv) == 1 :
        examples['aa'] = DFA.POSITIVE_LABEL
        examples['a'] = DFA.NEGATIVE_LABEL
        examples['aaaaaa'] = DFA.POSITIVE_LABEL
        examples['aaaaa'] = DFA.NEGATIVE_LABEL
    elif len(sys.argv) == 2 :
        for pair in sys.argv[1].split(' ') :
            exstr, exclass = pair.split(',')
            examples[exstr] = exclass[1]
    else:
        for pair in sys.argv[1:] :
            exstr, exclass = pair.split(',')
            examples[exstr] = exclass[1]
    print(examples)
    
    fsm1 = DFA()
    fsm1.learn(examples)
    
    print(fsm1)
    
    fsm1.minimize()
    print('finished.')