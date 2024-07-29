'''
Created on 2024/06/01

@author: Sin Shimozono
'''
import itertools
from orderedset import OrderedSet
from pickle import NONE
from xlwt.BIFFRecords import ContinueRecord

class ObservationTable(object):
    EMPTYSTRING = ''
    EXAMPLE_LABEL = 1
    COUNTEREXAMPLE_LABEL = 0
    
    def __init__(self, finitealphabet):
        self.alphabet = set(finitealphabet)
        self.rows = dict()
        self.prefixes = OrderedSet(key=lambda x: (len(x), x))
        self.suffixes = OrderedSet(key=lambda x: (len(x), x))
        self.extensions = set()
        
        self.prefixes.insert(self.EMPTYSTRING)
        self.rows[self.EMPTYSTRING] = dict()
        self.extensions.add(self.EMPTYSTRING)
        self.suffixes.insert(self.EMPTYSTRING)
    
    def __str__(self)->str:
        result =  "ObservationTable(" + "'" + ''.join(sorted(self.alphabet)) + "', " 
        result += ", \n"  + str(self.suffixes) + str(sorted(self.extensions - set(self.suffixes), key=lambda x: (len(x),x))) + ",\n"
        for pfx in self.prefixes :
            result += " {0:8}| ".format(pfx)
            result += self.extension_string(pfx) + '\n'
        result += "--------\n"
        for pfx, a in itertools.product(self.prefixes, self.alphabet) :
            if pfx+a not in self.prefixes :
                result += " {0:8}| ".format(pfx+a)
                result += self.extension_string(pfx+a) + '\n'
        result += "])"
        return result
    
    def add_suffix(self, sfx):
        self.extensions.add(sfx)
        self.suffixes.insert(sfx)
    
    def add_extension(self, sfx):
        self.extensions.add(sfx)
    
    def add_prefix(self,pfx):
        self.prefixes.insert(pfx)
        if pfx not in self.rows:
            self.rows[pfx] = dict()
    
    def add_row(self,pfx):
        if pfx not in self.rows :
            self.rows[pfx] = dict()
    
    def row(self,pfx):
        return self.rows[pfx]

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
            if sfx not in self.extensions:
                self.extensions.add(sfx)
            self.rows[pfx][sfx] = xclass

    
    def row_string(self, pfx):
        if pfx in self.rows :
            result = "".join([str(self.rows[pfx].get(s, '.')) for s in self.suffixes])
            return result
        return ''.join(['.' for i in self.suffixes])

    def extension_string(self, pfx):
        result = self.row_string(pfx) + " "
        if pfx in self.rows :
            result += "".join([str(self.rows[pfx].get(s, '.')) for s in sorted(self.extensions -set(self.suffixes), key=lambda x: (len(x), x))])
        else:
            result += ''.join(['.' for i in sorted(self.extensions -set(self.suffixes), key=lambda x: (len(x), x))])    
        return result

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
        alphexts = sorted(self.alphabet.union(self.suffixes), key = lambda x: (len(x), x))
        print(self.prefixes, alphexts)
        for p in self.prefixes:
            for e in alphexts:
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
        rowstrings = dict()
        for pfx in obtable.prefixes :
            rowstr = obtable.row_string(pfx)
            if rowstr not in rowstrings :
                self.states.add(pfx)
                rowstrings[rowstr] = pfx
        #print(rowstrings)
        for s, a in itertools.product(self.states, self.alphabet) :
            for p in self.states :
                if obtable.rows_agree(s+a, p) :
                    #print("agree '{}.{}' with '{}'".format(s,a, p))
                    self.transfunc[(s,a)] = p
                    break
            
        for s in self.states :
            if obtable.rows[s][''] == obtable.EXAMPLE_LABEL :
                self.acceptingStates.add(s)
        
    def learn_by_mat(self):
        obtable = ObservationTable(self.alphabet)
        while True:
            while True :
                for s, e in obtable.unspecified_pairs() :
                    xclass = input("mq: Is '{}' 1 or 0 ? ".format(s+e))
                    obtable.extend(s+e, xclass)
                print(obtable)
                
                if not obtable.consistent() :
                    ext = obtable.find_inconsistent_extension()
                    print("obtable is not consistent with "+ext)
                    obtable.add_suffix(ext)
                    continue
                else:
                    print("obtable is consistent.")
                
                if not obtable.closed() :
                    pfx = obtable.find_stray_prefix()
                    print("obtabler is not closed with "+ pfx)
                    obtable.add_prefix(pfx)
                    continue
                else:
                    print("obtable is closed.")
                break
            self.define_machine(obtable)
            print(self)
            cxpair = input("eq: is there a counter-example? ") 
            if not cxpair :
                break
            else:
                cxpair = cxpair.split(',')
            if len(cxpair) == 1 :
                cxpair.append('0' if self.accept(cxpair[0]) else '1')
            print("counter example: {}, {}".format(cxpair[0],cxpair[1]))
            obtable.extend(cxpair[0], cxpair[1],addprefixes=True)

        return 

    