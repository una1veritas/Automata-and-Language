'''
Created on 2024/06/01

@author: Sin Shimozono
'''
import itertools
from orderedset import OrderedSet

class ObservationTable(object):
    EMPTYSTRING = ''
    EXAMPLE_LABEL = 1
    COUNTEREXAMPLE_LABEL = 0
    
    def __init__(self, finitealphabet):
        self.alphabet = set(finitealphabet)
        self.prefixes = OrderedSet(key=lambda x: (len(x), x))
        self.prefixes.insert(self.EMPTYSTRING)
        self.row = dict()
        self.row[self.EMPTYSTRING] = dict()
        self.suffixes = OrderedSet(key=lambda x: (len(x), x))
        self.suffixes.insert(self.EMPTYSTRING)
    
    def __str__(self)->str:
        result =  "ObservationTable(" \
        + "'" + ''.join(sorted(self.alphabet)) + "', " \
        + "\n" + str(self.suffixes) 
        result += ", [\n"
        for pfx in sorted(self.prefixes) :
            result += " {0:8}| ".format(pfx)
            result += self.row_string(pfx) + '\n'
        result += "--------\n"
        for pfx in sorted(set(self.row.keys()) - set(self.prefixes)) :
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
            self.suffixes.insert(sfx)  # duplicate addition will be ignored. 
            if pfx not in self.row :
                self.row[pfx] = dict()
            self.row[pfx][sfx] = xclass
            
            if pfx not in self.prefixes :
                for pref in self.prefixes:
                    if self.rows_agree(pref, pfx) :
                        break
                else:
                    self.prefixes.insert(pfx)
    
    def row_string(self, pfx):
        if pfx in self.row :
            result = "".join([str(self.row[pfx].get(s, '?')) for s in self.suffixes])
            return result
        return ''.join(['?' for i in range(len(self.suffixes))])
    
    def rows_agree(self, pfx1, pfx2):
        for e in self.suffixes :
            if pfx1 not in self.row or pfx2 not in self.row :
                continue
            if e not in self.row[pfx1] or e not in self.row[pfx2] :
                continue
            if self.row[pfx1][e] != self.row[pfx2][e] :
                return False
        return True
        
    def closed(self):
        for p, a in itertools.product(self.prefixes, self.alphabet) :
            if self.EMPTYSTRING not in self.row[p] :
                return False
            t = p + a
            if t not in self.row :
                return False
            for pref in self.prefixes:
                if self.rows_agree(pref, t) :
                    break
            else:
                return False
        return True
    
    def collect_open_prefixes(self):
        result = set()
        for p, a in itertools.product(self.prefixes, self.alphabet) :
            if self.EMPTYSTRING not in self.row[p] :
                print("add {} since not in self.row".format(self.EMPTYSTRING))
                result.add(self.EMPTYSTRING)
            t = p + a
            if t not in self.row :
                print("add {} since not in self.row".format(t))
                result.add(t)
            # for pref in self.prefixes:
            #     if self.rows_agree(pref, t) :
            #         break
            # else:
            #     print("add {} since no agreeing row".format(t))
            #     self.prefixes.insert(t)
                #result.add(t)
        return result
        
        
    def consistent(self):
        if len(self.prefixes) == 0 :
            return False
        for s1, s2 in itertools.product(self.prefixes, self.prefixes) :
            if s1 >= s2:
                continue
            row1 = self.row_string(s1)
            row2 = self.row_string(s2)
            if row1 == row2:
                #print("consistency chk:")
                for a in self.alphabet :
                    if self.row_string(s1+a) != self.row_string(s2+a) :
                        return False
                #print("passed", s1, s2)
        return True

    def unspecified_pairs(self):
        res = set()
        for p in self.prefixes:
            for s in self.suffixes:
                if s not in self.row[p]:
                    res.add( (p, s) )
        # for p in self.prefixes:
        #     for a in self.alphabet:
        #         if p+a not in self.row :
        #             res.add(p+a)
        return res
    
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
        
        for pfx in sorted(sorted(obtable.prefixes), key = lambda x : (len(x), x) ) :
            if pfx not in self.states: 
                eqvpfx = obtable.non_contradicting_prefix(pfx) 
                if eqvpfx == None :
                    self.states.add(pfx)
                else:
                    self.states.add(eqvpfx)
                    pfx = eqvpfx

            for a in self.alphabet :
                #print(pfx, a, obtable.non_contradicting_prefix(pfx + a))
                dst = obtable.non_contradicting_prefix(pfx + a)
                if dst == None :
                    dst = pfx+a
                self.transfunc[(pfx,a)] = dst
        #print(self.states, self.transfunc)
        for st in self.states :
            if obtable.row[st][''] == self.POSITIVE :
                self.acceptingStates.add(st)
        
    
    def get_example(self):
        exs = ''
        exc = ''
        while True:
            ex = input("例をください")
            arr = ex.split(",")
            if len(arr) == 2 :
                exs = arr[0]
                exc = arr[1]
                exs = exs.strip()
                exc = exc.strip()
            if exc not in ["+", "-"] :
                print("例は文字列と正負のラベルを , で区切ってください．")
                print("正負のラベルは + か - でお願いします．")
            else:
                break
        return exs, exc
        
    def learn_by_mat(self):
        obtable = ObservationTable(self.alphabet)
        while True:
            while not obtable.consistent() or not obtable.closed() :
                # unspairs = obtable.unspecified_pairs()
                # print(unspairs)
                # while unspairs :
                #     pref, suf = unspairs.pop()
                #     xc = input("uns mq: '{}' ? ".format(pref+suf))
                #     obtable.extend(pref+suf, xc)
                #     print(obtable)
                openprefs = obtable.collect_open_prefixes()
                while openprefs :
                    print(openprefs)
                    pref = openprefs.pop()
                    xc = input("open mq: '{}' ? ".format(pref))
                    obtable.extend(pref, xc)
                    print(obtable)
            break
        print(obtable)
        return 

    