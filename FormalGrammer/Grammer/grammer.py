'''
Created on 2021/11/05

@author: Sin Shimozono
'''

class Grammer():
    # class for representing generative formal grammer
    def __init__(self, nonterminals,terminals,rules,start):
        self.nonterminals = set(nonterminals)
        self.terminals = set(terminals)
        self.prodrules = dict()
        if isinstance(rules,str):
            try:
                rules = eval(rules)
            except SyntaxError:
                ruledict = dict()
                for each in rules.split(','):
                    lhs, rhs = each.split('->')
                    if lhs not in ruledict:
                        ruledict[lhs] = list()
                    ruledict[lhs].append(rhs)
                rules = ruledict
        print(rules)
        print()
        if isinstance(rules,(list,tuple)) and all([isinstance(elem,(list,tuple)) for elem in rules]):
            for src, dst in rules:
                if src in self.terminals and src not in self.nonterminals: continue
                if src not in self.prodrules:
                    self.prodrules[src] = set()
                self.prodrules[src].add(dst)
        elif isinstance(rules,dict) and all([isinstance(val,(set,list,tuple)) for key, val in rules.items()]):
            for k in rules:
                if k in self.terminals and k not in self.nonterminals : continue
                self.prodrules[k] = set(rules[k])        
        else:
            raise TypeError('illegal type for production rules.')
        self.startsym = start

    def __repr__(self):
        tmp = 'Grammer({},{},{},{})'.format(self.nonterminals,self.terminals,self.prodrules,self.startsym)
        return tmp

    def __str__(self):
        rulesstr = '{'
        rulesstr += ', '.join([str(key)+'->'+str(val) for key in self.prodrules for val in self.prodrules[key]])
        rulesstr += '}'
        tmp = 'Grammer({}, {}, {}, {})'.format(self.nonterminals,self.terminals,rulesstr,self.startsym)
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
    
    def ischomskynormalform(self):
        for lhs in self.prodrules:
            for rhs in self.prodrules[lhs]:
                if len(rhs) == 2 and all([sym in self.nonterminals for sym in rhs]) :
                    continue
                if len(rhs) == 1 and rhs in self.terminals :
                    continue
                return False
        return True

    def isregular(self):
        for lhs in self.prodrules:
            for rhs in self.prodrules[lhs]:
                if len(rhs) == 0 :
                    continue
                if len(rhs) == 1 and rhs in self.terminals :
                    continue
                if len(rhs) == 2 and rhs[0] in self.terminals and rhs[1] in self.nonterminals :
                    continue
                return False
        return True       
    
if __name__ == '__main__':
    import sys
    g = Grammer(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    print('G='+str(g))
    lim = 7
    if len(sys.argv) == 6 :
        lim = int(sys.argv[5])
    print("result = "+str(g.generate(lim)))
    print(g.ischomskynormalform())
    print(g.isregular())
