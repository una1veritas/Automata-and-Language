'''
Created on 2024/06/01

@author: Sin Shimozono
'''
import itertools
from orderedset import OrderedSet
from pickle import NONE

class ObservationTable(object):
    EMPTYSTRING = ''
    EXAMPLE_LABEL = 1
    COUNTEREXAMPLE_LABEL = 0
    
    def __init__(self, finitealphabet):
        self.alphabet = set(finitealphabet)
        self.rows = dict()
        self.prefixes = OrderedSet(key=lambda x: (len(x), x))
        self.suffixes = OrderedSet(key=lambda x: (len(x), x))
        self.auxextensions = set()
        
        self.prefixes.insert(self.EMPTYSTRING)
        self.rows[self.EMPTYSTRING] = dict()
        self.suffixes.insert(self.EMPTYSTRING)
    
    def __str__(self)->str:
        result =  "ObservationTable(" + "'" + ''.join(sorted(self.alphabet)) + "', " 
        result += ", \n"  + str(self.suffixes) + ",\n"
        for pfx in self.prefixes :
            result += " {0:8}| ".format(pfx)
            result += self.row_string(pfx) + '\n'
        result += "--------\n"
        for pfx, a in itertools.product(self.prefixes, self.alphabet) :
            if pfx+a not in self.prefixes :
                result += " {0:8}| ".format(pfx+a)
                result += self.row_string(pfx+a) + '\n'
        result += "])"
        return result
    
    def extend(self, xstr, xclass, addprefixes=False):
        if xclass not in ('+', '-','0', '1', 0, 1) :
            print("label error", xclass)
            return 
        if xclass in ('+', '1'):
            xclass = 1
        elif xclass in ('-', '0'):
            xclass = 0
        for i in range(0, len(xstr)+1):
            pfx = xstr[:i]
            sfx = xstr[i:]
            if pfx not in self.rows:
                self.rows[pfx] = dict()
            if pfx not in self.prefixes and addprefixes:
                self.prefixes.insert(pfx)
            self.rows[pfx][sfx] = xclass

    
    def row_string(self, pfx):
        if pfx in self.rows :
            result = "".join([str(self.rows[pfx].get(s, ' ')) for s in self.suffixes])
            return result
        return ''.join([' ' for i in self.suffixes])
    
    def rows_disagree(self, pfx1, pfx2):
        for e in self.suffixes :
            if pfx1 not in self.rows or pfx2 not in self.rows :
                continue
            if e not in self.rows[pfx1] or e not in self.rows[pfx2] :
                continue
            if self.rows[pfx1][e] != self.rows[pfx2][e] :
                return e
        return None 
    
    def rows_agree(self, pfx1, pfx2):
        return self.rows_disagree(pfx1, pfx2) == None
     
    def find_stray_prefix(self):
        # for x in self.extensions:
        #     print("ext", x)
        #     for pfx in self.prefixes:
        #         if self.rows_agree(pfx, x) :
        #             break
        #     else:
        #         #print("has no agreeing prefix")
        #         return x
        for p, a in itertools.product(self.prefixes, self.alphabet) :
            t = p + a
            if t not in self.rows :
                self.rows[t] = dict()
            for pfx in self.prefixes:
                if self.rows_agree(pfx, t) :
                    break
            else:
                #print("has no agreeing prefix")
                return t
        return None
        
    def find_inconsistent_extension(self):
        for s1, s2 in itertools.product(self.prefixes, self.prefixes) :
            if s1 >= s2:
                continue
            if self.rows_agree(s1, s2) :
               #print("consistency chk:")
                for a in self.alphabet :
                    ext = self.rows_disagree(s1+a, s2+a)
                    if ext != None :
                        return a + ext
        return None 
    
    def closed(self):
        # print("find_stray", self.find_stray_prefix() == None)
        return self.find_stray_prefix() == None        
        
    def consistent(self):
        return self.find_inconsistent_extension() == None 

    def unspecified_pairs(self):
        res = set()
        for p in self.rows:
            for e in self.suffixes:
                if p not in self.rows or e not in self.rows[p]:
                    res.add( (p, e) )
        # for p in self.prefixes:
        #     for a in self.alphabet:
        #         if p+a not in self.rows :
        #             res.add(p+a)
        print(res)
        return res
    
    def fullyspecified(self):
        return not self.unspecified_pairs()
    
class DFA(object):
    '''
    classdocs
    '''
    INITIAL_STATE = ''
    POSITIVE = '+'
    NEGATIVE = '0'
    UNDEFINED = '-'

    def __init__(self, falphabet = ''):
        '''
        the definitions of the initial empty automata 
        accepts no strings
        '''
        self.alphabet = set()
        if len(falphabet) > 0 :
            for c in str(falphabet) :
                self.alphabet.add(c)
        self.initialState = self.INITIAL_STATE
        self.states = set()
        self.states.add(self.initialState)
        self.transfunc = dict()
        self.acceptingStates = set()
        '''
        computing mechanizm
        '''
        self.current = self.initialState
        
    def __str__(self):
        return "DFA(alphabet = {" + ', '.join(sorted(self.alphabet)) + "}, \n states = {" \
            + ', '.join([ s if len(s) > 0 else "'"+s+"'" for s in sorted(self.states)]) + "}, \n initial = '" + str(self.initialState) + "', \n" \
            + " transition = {" + ", ".join(["{} -> '{}'".format(k, v) for k, v in self.transfunc.items()]) \
            + "}, \n finals = " + str(self.acceptingStates) + ")"
        
    def initiate(self):
        self.current = self.initialState
    
    def is_accept(self, q) -> bool:
        return (q in self.acceptingStates)
    
    def defined(self, q, c):
        if (q, c) in self.transfunc :
            return True
        return False
    
    def transfer(self, q, c):
        if (q,c) in self.transfunc :
            return self.transfunc[(q, c)]
        return self.UNDEFINED
    
    def accept(self, s):
        self.initiate()
        for c in s:
            self.current = self.transfer(self.current, c)
        return self.is_accept(self.current)
        
    def define_machine(self, obtable):
        self.states.clear()
        self.acceptingStates.clear()
        eqvgroups = dict()
        for pfx in obtable.prefixes :
            row = obtable.row_string(pfx)
            if row not in eqvgroups :
                eqvgroups[row] = list()
                eqvgroups[row].append(pfx)
                self.states.add(pfx)
                for a in self.alphabet :
                    self.transfunc[(pfx,a)] = pfx + a
                    if pfx+a in eqvgroups :
                        self.transfunc[(pfx,a)] = eqvgroups[pfx+a][0]
                    else:
                        eqvgroups[pfx+a] = list()
                        eqvgroups[pfx+a].append(pfx+a)
                        
        for s in self.states :
            if obtable.rows[s][''] == obtable.EXAMPLE_LABEL :
                self.acceptingStates.add(s)
        
    def learn_by_mat(self):
        obtable = ObservationTable(self.alphabet)
        while True:
            while True :
                print(obtable)
                for s, e in obtable.unspecified_pairs() :
                    xclass = input("mq: Is '{}' 1 or 0 ? ".format(s+e))
                    obtable.extend(s+e, xclass)
                
                if not obtable.consistent() :
                    ext = obtable.find_inconsistent_extension()
                    print("obtable is not consistent for "+ext)
                    if ext not in obtable.suffixes :
                        obtable.suffixes.insert(ext)
                    for s, e in obtable.unspecified_pairs() :
                        xclass = input("mq: Is '{}' 1 or 0 ? ".format(s+e))
                        obtable.extend(s+e, xclass)
                    continue
                else:
                    print("obtable is consistent.")
                
                if not obtable.closed() :
                    pfx = obtable.find_stray_prefix()
                    print("obtabler is not closed with "+ pfx)
                    if pfx not in obtable.rows :
                        obtable.rows[pfx] = dict()
                    obtable.prefixes.insert(pfx)
                    for s, e in obtable.unspecified_pairs() :
                        xclass = input("mq: Is '{}' 1 or 0 ? ".format(s+e))
                        obtable.extend(s+e, xclass)
                    continue
                else:
                    print("obtable is closed.")
                break
            print(obtable)
            self.define_machine(obtable)
            print(self)
            cxpair = input("eq: is there a counter-example? ")
            if not cxpair :
                break
            cxpair = cxpair.split(',')
            if self.accept(cxpair[0]) :
                if len(cxpair) < 2 :
                    cxpair.append('0') 
                if cxpair[1] in ('+', '1') :
                    continue
            else:
                if len(cxpair) < 2 :
                    cxpair.append('1') 
                if cxpair[1] in ('-', '0') :
                    continue
            obtable.extend(cxpair[0], cxpair[1],addprefixes=True)

        return 

    