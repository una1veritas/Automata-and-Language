'''
Created on 2024/06/01

@author: Sin Shimozono
'''

import sys
from EasyLearner.dfa import DFA

if __name__ == '__main__':
    examples = list()
    print(sys.argv)
    if len(sys.argv) == 1 :
        print('examples requested.')
        exit(1)
    elif len(sys.argv) == 2 :
        for pair in sys.argv[1].split(' ') :
            exstr, exclass = pair.split(',')
            examples.append( (exstr, exclass) )
    else:
        for pair in sys.argv[1:] :
            exstr, exclass = pair.split(',')
            examples.append( (exstr, exclass) )
    print("Given examples: ", examples)
    
    dfa1 = DFA()
    print(dfa1)

    dfa1.learn(examples)
    print(dfa1)
    
    
    dfa1.minimize()
    print('finished.')