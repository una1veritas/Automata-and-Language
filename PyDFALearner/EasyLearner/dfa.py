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
    
    '''空の observation table を作る．有限アルファベットは与える．'''
    def __init__(self, finitealphabet):
        self.alphabet = set(finitealphabet)
        self.rows = dict()
        self.prefixes = OrderedSet(key=lambda x: (len(x), x))
        self.suffixes = OrderedSet(key=lambda x: (len(x), x))
        self.extensions = set()
        '''
        OrderedSet   --- 自作の，二分探索法を使った集合．要素がソート済みになっている．
        self.alphabet --- 有限アルファベット．'' から 1 文字拡張する際に既知である必要がある. 
        self.rows     --- 行辞書の集まり，表（の中身，ます）
        self.prefixes --- 接頭辞の集合 S. なお S の要素と文字を連結した拡張接頭辞は，
        self.row （の見出し self.row.keys() ）には含まれるが，self.prefixes には含まれない．
        self.suffixes   --- 接尾辞の集合 E.
        self.extensions --- 接尾辞の集合 E にはふくめないが，ある行についてすでに既知となった
        （ますが埋まった）接尾辞の集合．self.suffixes には含まれないが，
        self.row[s][x] が登録ずみの文字列 x. Angluin '87 にはないもの．
        '''
        self.prefixes.insert(self.EMPTYSTRING)
        self.rows[self.EMPTYSTRING] = dict()
        self.extensions.add(self.EMPTYSTRING)
        self.suffixes.insert(self.EMPTYSTRING)
    
    def __str__(self)->str:
        result =  "ObservationTable(" + "'" + ''.join(sorted(self.alphabet)) + "', \n" 
        ext_suffixes = [sfx for sfx in sorted(self.extensions, key=lambda x: (len(x),x)) if sfx not in self.suffixes] 
        result += str(self.suffixes) + ",\n"
        printedpfx = set()
        for pfx in self.prefixes :
            result += " {0:8}| ".format(pfx)
            result += self.row_string(pfx) + '\n'
            printedpfx.add(pfx)
        result += "--------\n"
        for pfx, a in itertools.product(self.prefixes, self.alphabet) :
            if pfx+a not in self.prefixes :
                result += " {0:8}| ".format(pfx+a)
                result += self.row_string(pfx+a) + '\n'
            printedpfx.add(pfx+a)
        # result += "========\n"
        # for pfx in self.rows :
        #     if pfx in printedpfx :
        #         continue
        #     result += " {0:8}| ".format(pfx)
        #     result += self.extension_string(pfx) + '\n'
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
        return self.rows.get(pfx, dict())
    
    # def table(self, xs):
    #     return self.rows[self.EMPTYSTRING].get(xs,None)
    
    '''例を使って表の空欄を埋める. '''
    '''addprefixes == True ならば，例から生じる接頭辞すべてを prefixes に登録する'''
    def fill(self, xstr, xclass, addprefixes=False):
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
            if addprefixes:
                self.add_prefix(pfx)
            elif pfx not in self.rows:
                self.add_row(pfx)
                #print("added to rows", pfx,self.rows.keys())
            self.add_extension(sfx)
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
     
    def find_open_prefix(self):
        for p, a in itertools.product(self.prefixes, self.alphabet) :
            t = p + a
            if t not in self.rows :
                self.rows[t] = dict()
            for pfx in self.prefixes:
                if self.rows_agree(pfx, t) :
                    break
            else:
                print("has no agreeing prefix", pfx, t)
                return t
        return None
        
    def find_inconsistent_extension(self):
        for s1, s2 in itertools.product(self.prefixes, self.prefixes) :
            if s1 >= s2:
                continue
            #print(s1,s2,self.row_string(s1), self.row_string(s2))
            if self.rows_agree(s1, s2) :
               #print("consistency chk:")
                for a in self.alphabet :
                    #print("{}, {}, +{}; {}/{} -> {},{}".format(s1,s2,a,self.row_string(s1), self.row_string(s2),self.row_string(s1+a), self.row_string(s2+a)))
                    ext = self.rows_disagree(s1+a, s2+a)
                    if ext != None :
                        return a + ext
        return None 
    
    def find_transition_gap(self):
        prefs = OrderedSet(self.prefixes)
        prefs.pop() # pop ''
        while len(prefs) > 0 : 
            first = prefs.pop()
            src = self.representative_prefix(first[:-1])
            dst = self.representative_prefix(src + first[-1:])
            if dst != self.representative_prefix(first) :
                return (first[:-1], first)            
        return None
    
    def representative_prefix(self, pfx):
        for s in self.prefixes:
            if self.rows_agree(s, pfx):
                return s
        return pfx
        
    def closed(self):
        # print("find_stray", self.find_open_prefix() == None)
        return self.find_open_prefix() == None        
        
    def consistent(self):
        return self.find_inconsistent_extension() == None 
    #
    # def unspecified_pairs(self):
    #     res = set()
    #     alphexts = sorted(self.alphabet.union(self.suffixes), key = lambda x: (len(x), x))
    #     #print(self.prefixes, alphexts)
    #     for p in self.prefixes:
    #         for e in alphexts:
    #             if p not in self.rows or e not in self.rows[p]:
    #                 res.add( (p, e) )
    #     return res
    
    def find_unspecified(self):
        for pfx in sorted( set(list(self.prefixes) 
                               + [px + a for px, a in itertools.product(self.prefixes, self.alphabet)]) \
                          , key = lambda x : (len(x), x)) :
            for e in self.suffixes:
                if pfx not in self.rows or e not in self.rows[pfx]:
                    #print("as px + a + e", px)
                    return pfx + e
    
        # for px, e in itertools.product(self.prefixes, self.suffixes) :
        #     if px not in self.rows or e not in self.rows[px]:
        #         #print("as px + e", px)
        #         return px + e
        # for px, a in itertools.product(self.prefixes, self.alphabet):
        #     if px + a not in self.prefixes:
        #         for e in self.suffixes:
        #             if px + a not in self.rows or e not in self.rows[px+a]:
        #                 #print("as px + a + e", px)
        #                 return px + a + e
                    
        return None
    #
    # def find_undecided(self):
    #     for px in self.prefixes:
    #         if self.EMPTYSTRING not in self.rows[px] :
    #             return px
    #     return None
    #
    # def fullyspecified(self):
    #     return self.find_unspecified == None
    
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
        maxlen = max([len(s) for s in self.states])
        return "DFA(alphabet = {" + ', '.join(sorted(self.alphabet)) + "}, \n states = {" \
            + ', '.join([ s if len(s) > 0 else "'"+s+"'" for s in sorted(self.states)]) + "}, \n initial = '" + str(self.initialState) + "', \n" \
            + " transition = {\n" + "\n".join(["{0:{wdth}} | {1} | {2}".format(k[0] if len(k[0]) else "''", k[1], self.transfunc[k] if len(self.transfunc[k]) else "''", wdth=maxlen) for k in sorted(self.transfunc.keys())]) \
            + "\n}, \n finals = {" + ", ".join(["'"+s+"'" for s in self.acceptingStates]) + "}" +  ")"
        
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
        self.transfunc.clear()
        self.acceptingStates.clear()
        
        for pfx in obtable.prefixes :
            if len(self.states) == 0 :
                self.states.add(pfx)
                continue
            for s in self.states :
                if obtable.rows_agree(pfx, s) :
                    break
            else: 
                self.states.add(pfx)
        for s, a in itertools.product(self.states, self.alphabet) :
            for p in self.states :
                if obtable.rows_agree(s+a, p) :
                    self.transfunc[(s,a)] = p
                    break
            else:
                raise ValueError("no dest state "+str((s,a)))
            
        for s in self.states :
            if obtable.EMPTYSTRING in obtable.rows[s] and obtable.rows[s][obtable.EMPTYSTRING] == obtable.EXAMPLE_LABEL :
                #print("add final ", s)
                self.acceptingStates.add(s)
        
    def learn_by_mat(self):
        obtable = ObservationTable(self.alphabet)
        cx_count = 0
        ex_count = 0
        while True:
            while (ext := obtable.find_inconsistent_extension()) != None \
            or (pfx := obtable.find_open_prefix()) != None \
            or (unspec := obtable.find_unspecified()) != None :                
                if  ext != None :
                    obtable.add_suffix(ext)
                    print("obtable is not consistent. adding suffix '{}'".format(ext))
                    continue
                else:
                    print("obtable is consistent.")
                
                if pfx != None :
                    obtable.add_prefix(pfx)
                    print("obtable is not closed. adding prefix '{}'".format(pfx) )
                    continue
                else:
                    print("obtable is closed.")
                
                print("current ", end="")
                print(obtable)
                print()

                if ext == None and pfx == None :
                    if (gap := obtable.find_transition_gap()) == None:
                        print("Tentative machine: ")
                        self.define_machine(obtable)
                        print(self)
                    else:
                        print("Table has a transition gap between {} and {}.".format(gap[0], gap[1]))
                
                if unspec != None :
                    xclass = input("mq unspecified: Is '{}' 1 or 0 ? ".format(unspec))
                    ex_count += 1
                    obtable.fill(unspec, xclass)
                    print()

            print("The target machine to our knowledge:")
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
            cx_count += 1
            obtable.fill(cxpair[0], cxpair[1],addprefixes=True)
            # while (unspec := obtable.find_unspecified()) != None :
            #     xclass = input("mq unspecified: Is '{}' 1 or 0 ? ".format(unspec))
            #     obtable.fill(unspec, xclass)
            print(obtable)
        print("MQ: {}, EQ: {}".format(ex_count, cx_count))
        return 

    