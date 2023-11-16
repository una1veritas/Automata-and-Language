'''
Created on 2023/11/16

@author: Sin Shimozono
'''

import sys
if __name__ == '__main__':
    print(sys.argv)
    n = int(sys.argv[1])
    f_0 = '0'
    f_1 = '1'
    if n >= 0 :
        print(0, f_0)
    if n >= 1:
        print(1, f_1)
    for i in range(2, n) :
        f_n = f_0 + f_1
        f_0 = f_1
        f_1 = f_n
        print(i, f_n)
    exit(0)