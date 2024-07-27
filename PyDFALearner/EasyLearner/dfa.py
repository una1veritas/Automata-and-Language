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
        self.stateprefixes = OrderedSet(key=lambda x: (len(x), x))
        self.stateprefixes.insert(self.EMPTYSTRING)
        self.row = dict()
        self.row[self.EMPTYSTRING] = dict()
        self.extensions = OrderedSet(key=lambda x: (len(x), x))
        self.extensions.insert(self.EMPTYSTRING)
    
    def __str__(self)->str:
        result =  "ObservationTable(" \
        + "'" + ''.join(sorted(self.alphabet)) + "', " \
        + "\n" + str(self.extensions) 
        result += ", [\n"
        for pfx in sorted(self.stateprefixes) :
            result += " {0:8}| ".format(pfx)
            result += self.row_string(pfx) + '\n'
        result += "--------\n"
        for pfx in sorted(set(self.row.keys()) - set(self.stateprefixes)) :
            result += " {0:8}| ".format(pfx)
            result += self.row_string(pfx) + '\n'
        result += "])"
        return result
    
    def extend(self, xstr, xclass):
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
            self.extensions.insert(sfx)  # duplicate addition will be ignored. 
            if pfx not in self.row :
                self.row[pfx] = dict()
            self.row[pfx][sfx] = xclass
            #
            # if pfx not in self.stateprefixes :
            #     for pref in self.stateprefixes:
            #         if self.rows_agree(pref, pfx) :
            #             break
            #     else:
            #         self.stateprefixes.insert(pfx)
    
    def row_string(self, pfx):
        if pfx in self.row :
            result = "".join([str(self.row[pfx].get(s, '?')) for s in self.extensions])
            return result
        return ''.join(['?' for i in range(len(self.extensions))])
    
    def rows_disagree(self, pfx1, pfx2):
        for e in self.extensions :
            if pfx1 not in self.row or pfx2 not in self.row :
                continue
            if e not in self.row[pfx1] or e not in self.row[pfx2] :
                continue
            if self.row[pfx1][e] != self.row[pfx2][e] :
                return e
        return None 
    
    def rows_agree(self, pfx1, pfx2):
        return self.rows_disagree(pfx1, pfx2) == None 
     
    def find_stray_prefix(self):
        for p, a in itertools.product(self.stateprefixes, self.alphabet) :
            t = p + a
            if t not in self.row :
                #print("not in row")
                return t
            for pfx in self.stateprefixes:
                if self.rows_agree(pfx, t) :
                    break
            else:
                #print("has no agreeing prefix")
                return t
        return None
        
    def find_inconsistent_extension(self):
        for s1, s2 in itertools.product(self.stateprefixes, self.stateprefixes) :
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
        for p in self.stateprefixes:
            for e in self.extensions:
                if p not in self.row or e not in self.row[p]:
                    res.add( (p, e) )
        # for p in self.stateprefixes:
        #     for a in self.alphabet:
        #         if p+a not in self.row :
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
        
        for pfx in obtable.stateprefixes :
            if pfx not in self.states: 
                self.states.add(pfx)
                for a in self.alphabet :
                    self.transfunc[(pfx,a)] = pfx + a
                    for s in obtable.stateprefixes:
                        if obtable.rows_agree(s, pfx+a) :
                            self.transfunc[(pfx,a)] = s
                            break
        for s in self.states :
            if obtable.row[s][''] == obtable.EXAMPLE_LABEL :
                self.acceptingStates.add(s)
        
    def learn_by_mat(self):
        obtable = ObservationTable(self.alphabet)
        while True:
            print(obtable)
            while True :
                print(obtable)
                if not obtable.fullyspecified() :
                    for s, e in obtable.unspecified_pairs() :
                        xclass = input("mq: Is '{}' 1 or 0 ? ".format(s+e))
                        obtable.extend(s+e, xclass)
                    continue
                else:
                    print("obtable is fully specified.")
                    print(obtable)
                
                if not obtable.consistent() :
                    ext = obtable.find_inconsistent_extension()
                    if ext not in obtable.extensions :
                        obtable.extensions.insert(ext)
                    continue
                else:
                    print("obtable is consistent.")
                
                if not obtable.closed() :
                    pfx = obtable.find_stray_prefix()
                    print("not closed. stray pfx = ", pfx)
                    if pfx not in obtable.stateprefixes :
                        obtable.stateprefixes.insert(pfx)
                    continue
                else:
                    print("obtable is closed.")
                break
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
            obtable.extend(cxpair[0], cxpair[1])
                
            print(obtable)
        return 

    