'''
Created on 2025/01/28

@author: sin
'''

if __name__ == '__main__':
    while True:
        cxpair = input("eq: is there a counter-example? ")
        print('cxpair = ', cxpair)
        if not cxpair :
            print('cxpair is empty')
            exit(1)
        else:
            sep = ''
            if ',' in cxpair :
                sep = ','
            else:
                sep = ' '
            if sep != '' :
                cxpair = cxpair.split(sep)
                cxpair = (cxpair[0].strip(), cxpair[1].strip())
        if len(cxpair) == 1 :
            cxpair = (cxpair[0].strip(), '0' if True else '1')
        print("counter example: '{}', '{}'".format(cxpair[0],cxpair[1]))
    
    exit(0)
