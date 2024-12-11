'''
Created on 2021/11/05

@author: Sin Shimozono
'''

import itertools

class FormalGrammer():
    def __init__(self, nonterminals,terminals,rules,start):
        self.nonterminals = set(nonterminals)
        self.terminals = set(terminals)
        self.prodrules = dict()
        if isinstance(rules,str):
            for each in rules.split(',') :
                if '→' in each :
                    (lhs, rhs) = each.strip().split('→') 
                else:
                    (lhs, rhs) = each.strip().split('->') 
                lhs = lhs.strip()
                rhs = rhs.strip().split('|')
                if lhs not in self.prodrules :
                    self.prodrules[lhs] = set()
                for e in rhs:
                    self.prodrules[lhs].add(e)
            #print(self.prodrules)
        else:
            raise TypeError('illegal type for production rules.')
        self.start = start

    def __repr__(self):
        tmp = 'FormalGrammer({},{},{},{})'.format(self.nonterminals,self.terminals,self.prodrules,self.start)
        return tmp

    def __str__(self):
        rulesstr = '{' + ', '.join([str(key)+'->'+'|'.join([val for val in sorted(self.prodrules[key])]) for key in self.prodrules]) + '}'
        nonterminalsstr = '{'
        nonterminalsstr += self.start
        for e in sorted(list(self.nonterminals)):
            if e == self.start : continue
            nonterminalsstr += ', ' + e
        nonterminalsstr += '}'
        alphabetstr = '{'+(', '.join(sorted(list(self.terminals))))+'}'        
        tmp = 'FormalGrammer({}, {}, {}, {})'.format(nonterminalsstr,alphabetstr,rulesstr,self.start)
        return tmp
    
    def fromed_from_terminals(self, seq):
        for c in seq :
            if c not in self.terminals :
                return False
        return True 
        
    def generate(self, limit=10):
        derived = list()
        derived.append(self.start)
        result = list()
#       cnt = 0
        while len(derived) > 0:
#            if cnt > 100 :
#                break
#            else:
#                cnt += 1
            t = derived.pop(0)
            if self.fromed_from_terminals(t) :
                result.append(t)
                continue
            expanded = list()
            ''' t 中の非終端記号の出現位置を記号毎にすべて確認 '''
            NTs = dict()
            for i in range(len(t)) :
                if t[i] in self.nonterminals :
                    if t[i] not in NTs :
                        NTs[t[i]] = list()
                    NTs[t[i]].append(i)
            #print(t, NTs)
            ''' 出現する非終端記号ごとにすべての可能なルール適用パターンを枚挙した代入を適用 '''
            for nt in NTs:
                for tup in itertools.product(self.prodrules[nt], repeat=len(NTs[nt])) :
                    '''「同時に代入」をどう実現するか。
                    まず t を NTs[nt] の各要素で区切るか。。'''
                    elems = t.split(nt)
                    res = ''
                    for i in range(len(tup)) :
                        res += elems[i] + tup[i]
                    res += elems[-1]
                    if len(res) <= limit :
                        expanded.append(res)
            #print("extended = ",expanded)
            derived.extend(expanded)
            #print(result, derived)
        result = list(set(result))
        result = sorted(result, key = lambda x: len(x))
        return result

if __name__ == '__main__':
    import sys
    #print(sys.argv)
    g = FormalGrammer(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    print('G='+str(g))
    print("The final result = "+str(g.generate(int(sys.argv[5]))))
