'''
Created on 2024/06/01

@author: Sin Shimozono
'''

import sys
from dfa import DFA

if __name__ == '__main__':
    examples = list()
    #print(sys.argv)
    # if len(sys.argv) == 1 :
    #     print('examples requested.')
    #     exit(1)
    # elif len(sys.argv) == 2 :
    #     for pair in sys.argv[1].split(' ') :
    #         exstr, exclass = pair.split(',')
    #         examples.append( (exstr, exclass) )
    # else:
    #     for pair in sys.argv[1:] :
    #         exstr, exclass = pair.split(',')
    #         examples.append( (exstr, exclass) )
    # print("Given examples: ", examples)
    
    dfa1 = DFA()

    dfa1.learn()
    print(dfa1)
    
    print('finished.')