'''
Created on 2021/11/05

@author: Sin Shimozono
'''

class GenerativeGrammer():
    def __init__(self, nonterminals,terminals,rules,start):
        self.nonterminals = set(nonterminals)
        self.terminals = set(terminals)
        self.prodrules = dict()
        if isinstance(rules,str):
            rules = eval(rules)
        if isinstance(rules,(list,tuple)) and all([isinstance(elem,(list,tuple)) for elem in rules]):
            for src, dst in rules:
                if src in self.terminals and src not in self.nonterminals: continue
                if src not in self.prodrules:
                    self.prodrules[src] = set()
                self.prodrules[src].add(dst)
        elif isinstance(rules,dict) and all([isinstance(val,(set,list,tuple)) for key, val in rules]):
            for k, v in rules:
                if k in self.terminals and k not in self.nonterminals : continue
                self.prodrules[k] = set(v)        
        else:
            raise TypeError('illegal type for production rules.')
        self.startsym = start

    def __repr__(self):
        tmp = 'GenerativeGrammer({},{},{},{})'.format(self.nonterminals,self.terminals,self.prodrules,self.startsym)
        return tmp

    def __str__(self):
        rulesstr = '{'
        rulesstr += ', '.join([str(key)+'->'+str(val) for key in self.prodrules for val in self.prodrules[key]])
        rulesstr += '}'
        tmp = 'GenerativeGrammer({}, {}, {}, {})'.format(self.nonterminals,self.terminals,rulesstr,self.startsym)
        return tmp
    
    def generate(self, limit=10):
        derived = list()
        derived.append(self.startsym)
        result = list()
        while len(derived):
            print(derived, result)
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
        return result

if __name__ == '__main__':
    import sys
    g = GenerativeGrammer(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    print('G='+str(g))
    print("result = "+str(g.generate(int(sys.argv[5]))))
