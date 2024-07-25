'''
Created on 2024/06/01

@author: Sin Shimozono
'''
import itertools
from orderedset import OrderedSet

class ObservationTable(object):
    EMPTYSTRING = ''
    
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
        for i in range(0, len(xstr)+1):
            pfx = xstr[:i]
            sfx = xstr[i:]
            self.suffixes.insert(sfx)  # duplicate addition will be ignored. 
            if pfx not in self.row :
                self.row[pfx] = dict()
            self.row[pfx][sfx] = xclass
            
            if len(pfx) > 0 and '' in self.row[pfx[:-1]]:
                for a in self.alphabet :
                    if pfx[:-1] + a not in self.row :
                        break
                else:
                    #print("move ", pfx[:-1])
                    self.prefixes.insert(pfx[:-1])
    
    
    def row_string(self, pfx):
        if pfx in self.row :
            result = "".join([self.row[pfx].get(s, '*') for s in self.suffixes])
            return result
        return ''.join(['*' for i in range(len(self.suffixes))])
    
    def non_contradiction(self, p1, p2):
        row1 = self.row.get(p1, None)
        row2 = self.row.get(p2, None)
        if row1 is None or row2 is None :
            return True
        #print("prefix {}, {}".format(row1, row2))
        for e in self.suffixes:
            if (e in row1 and e in row2) and row1[e] != row2[e] :
                return False
        return True
    
    def first_contradictiing_suffix(self, p1, p2):
        row1 = self.row.get(p1, None)
        row2 = self.row.get(p2, None)
        if row1 is None or row2 is None :
            return None
        #print("prefix {}, {}".format(row1, row2))
        for e in self.suffixes:
            if (e in row1 and e in row2) and row1[e] != row2[e] :
                return e
        return None
    
    def non_contradicting_prefix(self, pfx):
        for p in sorted(self.prefixes, key=lambda x: (len(x), x)) :
            if self.non_contradiction(pfx, p) :
                return p
        return None
    
    def closed(self):
        if self.first_open_prefix() == None :
            return True
        return False
    
    def open_prefixes(self):
        res = set()
        for p, a in itertools.product(self.prefixes, self.alphabet) :
            t = p + a
            if t not in self.row :
                res.add(t)
            for s in self.prefixes :
                if self.non_contradiction(t, s) :
                    equiv_t = s
            if equiv_t == None :
                res.add(t)
        return res
    
    def consistent(self):
        if len(self.prefixes) == 0 :
            return False
        for s1, s2 in itertools.product(self.prefixes, self.prefixes) :
            if s1 >= s2:
                continue
            if self.non_contradiction(s1, s2):
                #print("consistency chk:")
                for a in self.alphabet :
                    if not self.non_contradiction(s1+a, s2+a) :
                        return False
                #print("passed", s1, s2)
        return True
    
    def inconsistent_quadruple(self):
        if len(self.prefixes) <= 1 :
            return None
        for s1, s2 in itertools.product(self.prefixes, self.prefixes) :
            if s1 >= s2:
                continue
            if self.non_contradiction(s1, s2):
                #print("consistency chk:")
                for a in self.alphabet :
                    sfx = self.first_contradicting_suffix(s1+a, s2+a) 
                    if sfx != None :
                        return (s1, s2, a, sfx)
                #print("passed", s1, s2)
        return True
    
    def unspecified_pairs(self):
        res = set()
        for p in self.prefixes:
            for s in self.suffixes:
                if s not in self.row[p]:
                    res.add( (p, s) )
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
            print(obtable)
            unspairs = obtable.unspecified_pairs()
            while unspairs :
                print(unspairs)
                pfx, sfx = unspairs.pop()
                xc = input("Wether '{}' is + or - ? ".format(pfx+sfx))
                obtable.extend(pfx+sfx,xc)
                print(obtable)
            print("unspairs cleared.")
            q = obtable.inconsistent_quadruple()
            print("inconsistent quadruple = ", q)
            if q != None :
                '''issue membership query'''
                (s1, s2, a, e) = q
                for p in obtable.prefixes:
                    if p+a+e not in obtable.row : 
                        xc = input(p+a+e)
                        obtable.extend(p+a+e, xc)
                        print(obtable)
            q = obtable.open_prefixes()
            while q :
                print("open prefixes = ", q)
                '''issue membership query'''
                p = q.pop()
                xc = input("Wether '{}' is + or - ? ".format(p))
                obtable.extend(p,xc)
                print(obtable)
            '''issue equivalence query'''
            self.define_machine(obtable)
            print(self)
            print("判例があればください")
            
            print("なければおわります．")
            break
        return 

    