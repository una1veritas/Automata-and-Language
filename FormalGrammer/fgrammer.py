'''
Created on 2021/11/05

@author: Sin Shimozono
'''

class FormalGrammer():
    def __init__(self, nonterminals,terminals,rules,start):
        self.nonterminals = set(nonterminals)
        self.terminals = set(terminals)
        self.prodrules = dict()
        if isinstance(rules,str):
            for each in rules.split(',') :
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
    
    def generate(self, limit=10):
        derived = list()
        derived.append(self.start)
        result = list()
        while len(derived):
            #print(derived, result)
            t = derived.pop(0)
            if all([ea in self.terminals for ea in t]) or not len(t) <= limit :
                result.append(t)
                continue
            expanded = list()
            for i in range(len(t)):
                s = t[i]
                if s in self.prodrules:
                    for each in self.prodrules[s]:
                        r = t[:i]+each+t[i+1:]
                        if len(r) <= limit :
                            expanded.append(r)
            print(expanded)
            derived.extend(expanded)
        result = list(set(result))
        result = sorted(result)
        result = sorted(result, key = lambda x: len(x))
        return result

if __name__ == '__main__':
    import sys
    g = FormalGrammer(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    print('G='+str(g))
    print("result = "+str(g.generate(int(sys.argv[5]))))
