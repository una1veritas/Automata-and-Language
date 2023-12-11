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
            rules = eval(rules)
        # if isinstance(rules,(list,tuple)) and all([isinstance(elem,(list,tuple)) for elem in rules]):
        #     for src, dst in rules:
        #         if src in self.terminals and src not in self.nonterminals: 
        #             continue
        #         if src not in self.prodrules:
        #             self.prodrules[src] = set([dst])
        #         else:
        #             self.prodrules[src].add(dst)
        if isinstance(rules,dict) :
            print("rules = ", rules)
            for k in rules:
                rhs = rules[k]
                if k in self.terminals and k not in self.nonterminals :
                    print('error')
                    continue
                if k not in self.prodrules :
                    self.prodrules[k] = set() 
                else:
                    print(k, rhs)
                if isinstance(rhs, (list,tuple,set)) :
                    for e in rules[k]:
                        self.prodrules[k].add(e)
                else:
                    self.prodrules[k].add(rhs)
            print(self.prodrules)
        else:
            raise TypeError('illegal type for production rules.')
        self.start = start

    def __repr__(self):
        tmp = 'FormalGrammer({},{},{},{})'.format(self.nonterminals,self.terminals,self.prodrules,self.start)
        return tmp

    def __str__(self):
        rulesstr = '{'
        rulesstr += ', '.join([str(key)+'->'+str(val) for key in self.prodrules for val in self.prodrules[key]])
        rulesstr += '}'
        tmp = 'FormalGrammer({}, {}, {}, {})'.format(self.nonterminals,self.terminals,rulesstr,self.start)
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
            #print(expanded)
            derived.extend(expanded)
        return set(result)

if __name__ == '__main__':
    import sys
    g = FormalGrammer(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    print('G='+str(g))
    print("result = "+str(g.generate(int(sys.argv[5]))))
