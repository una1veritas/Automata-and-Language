'''
Created on 2024/06/01

@author: Sin Shimozono
'''
import itertools
from btreeset import BTreeSet

class ObservationTable(object):
    EMPTYSTRING = ''
    EXAMPLE_LABEL = 1
    COUNTEREXAMPLE_LABEL = 0
    
    '''空の observation table を作る．有限アルファベットは与える．'''
    def __init__(self, finitealphabet):
        self.alphabet = set(finitealphabet)
        self.rows = dict()
        self.prefixes = BTreeSet(key=lambda x: (len(x), x))
        self.suffixes = BTreeSet(key=lambda x: (len(x), x))
        self.extensions = BTreeSet(key=lambda x: (len(x), x))
        '''
        BTreeSet/OrderedSet   --- 自作の集合．要素がソート済みになっている．
        self.alphabet --- 有限アルファベット．'' から 1 文字拡張する際に既知である必要がある. 
        self.rows     --- 行辞書の集まり，表（の中身，ます）
        self.prefixes --- 接頭辞の集合 S. なお S の要素と文字を連結した拡張接頭辞は，
        self.row （の見出し self.row.keys() ）には含まれるが，self.prefixes には含まれない．
        self.suffixes   --- 接尾辞の集合 E.
        self.extensions --- 接尾辞の集合 E にはふくめないが，ある行についてすでに既知となった
        （ますが埋まった）接尾辞の集合．self.suffixes には含まれないが，
        self.row[s][x] が登録ずみの文字列 x. Angluin '87 にはないもの．
        '''
        self.prefixes.add(self.EMPTYSTRING)
        self.rows[self.EMPTYSTRING] = dict()
        self.extensions.add(self.EMPTYSTRING)
        self.suffixes.add(self.EMPTYSTRING)
    
    def __str__(self) -> str:
        result =  "ObservationTable(" + "'" + ''.join(sorted(self.alphabet)) + "', \n" 
        result += str(list(self.suffixes)) + "," + str([e for e in self.extensions if not e in self.suffixes]) + "\n"
        printedpfx = set()
        for pfx in self.prefixes :
            result += " {0:8}| ".format(pfx)
            result += self.row_string_extended(pfx) + '\n'
            printedpfx.add(pfx)
        result += "--------\n"
        for pfx, a in itertools.product(self.prefixes, self.alphabet) :
            if pfx+a not in self.prefixes :
                result += " {0:8}| ".format(pfx+a)
                result += self.row_string_extended(pfx+a) + '\n'
            printedpfx.add(pfx+a)
        # result += "========\n"
        # for pfx in self.rows :
        #     if pfx in printedpfx :
        #         continue
        #     result += " {0:8}| ".format(pfx)
        #     result += self.row_string_extended(pfx) + '\n'
        result += "])"
        return result
    
    def add_suffix(self, sfx):
        self.extensions.add(sfx)
        self.suffixes.add(sfx)
    
    def add_extension(self, sfx):
        self.extensions.add(sfx)
    
    def add_prefix(self,pfx):
        self.prefixes.add(pfx)
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
        # if pfx in self.rows :
        #     result = "".join([str(self.rows[pfx].get(s, '.')) for s in self.suffixes])
        #     return result
        return ''.join([str(self.rows[pfx][s]) if pfx in self.rows and s in self.rows[pfx] else '.' for s in self.suffixes])

    def row_string_extended(self, pfx):
        result = self.row_string(pfx) + " "
        if pfx in self.rows :
            result += "".join([str(self.rows[pfx].get(s, '.')) for s in self.extensions if not s in self.suffixes])
        else:
            result += ''.join(['.' for i in self.extensions if not i in self.suffixes])    
        return result

    def rows_contradict(self, pfx1, pfx2):
        return self.find_rows_contradiction(pfx1, pfx2) != None
    
    def find_rows_contradiction(self, pfx1, pfx2):
        for sfx in self.suffixes :
            if pfx1 in self.rows and sfx in self.rows[pfx1] \
            and pfx2 in self.rows and sfx in self.rows[pfx2] \
            and self.rows[pfx1][sfx] != self.rows[pfx2][sfx] :
                return sfx
        return None
    
    # def rows_agree(self, pfx1, pfx2):
    #     return self.rows_disagree(pfx1, pfx2) == None
    
    def rows_identical(self, pfx1, pfx2):
        for e in self.suffixes :
            if e not in self.rows[pfx1] or e not in self.rows[pfx2] :
                break
            if self.rows[pfx1][e] != self.rows[pfx2][e] :
                break
        else:
            return True
        return False
    
    def find_open_prefix(self):
        for p, a in itertools.product(self.prefixes, self.alphabet) :
            t = p + a
            if t not in self.rows :
                self.rows[t] = dict()
            for pfx in self.prefixes:
                if not self.rows_contradict(pfx, t) :
                    break
            else:
                print("has no agreeing prefix", pfx, t)
                return t
        return None
        
    def find_inconsistent_extension(self):
        for s1, s2 in itertools.product(self.prefixes, self.prefixes) :
            if s1 < s2 and not self.rows_contradict(s1, s2):
                #print("consistency chk:")
                for a in self.alphabet :
                    #print("{}, {}, +{}; {}/{} -> {},{}".format(s1,s2,a,self.row_string(s1), self.row_string(s2),self.row_string(s1+a), self.row_string(s2+a))) 
                    if (ext := self.find_rows_contradiction(s1+a, s2+a)) != None :
                        return (s1,s2,a+ext)
        return None 
    
    def find_transition_gap(self):
        for pfx in self.prefixes :
            if len(pfx) == 0 :
                continue
            for src in self.prefixes:
                if src == pfx[:-1] or self.rows_contradict(src, pfx[:-1]) :
                    continue
                dst = self.agreeing_prefix(src + pfx[-1:])
                if dst == self.agreeing_prefix(pfx) :
                    break
            else:
                return (pfx[:-1], pfx)
        return None
    
    def list_transition_gaps(self):
        reslist = list()
        for pfx in self.prefixes :
            if len(pfx) == 0 :
                continue
            for src in self.prefixes:
                if src == pfx[:-1] or self.rows_contradict(src, pfx[:-1]) :
                    continue
                dst = self.agreeing_prefix(src + pfx[-1:])
                if dst == self.agreeing_prefix(pfx) :
                    break
            else:
                reslist.append(pfx)
        return reslist
    
    def agreeing_prefix(self, pfx):
        choice = None
        for s in self.prefixes:
            if self.rows_identical(s, pfx) :
                return s
            if choice == None and not self.rows_contradict(s, pfx):
                choice = s # a candidate
        if choice != None :
            return choice
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
        maxlen = 0 if len(self.states) == 0 else max([len(s) for s in self.states])
        #print(self.transfunc)
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
        '''基本となる，完成した観察テーブル obtable から自明な有限オートマトンを
        実際に構築する関数．D. Angluin '87 で照明されている構築方法に沿ってつくる。'''

        '''とりあえず初期化'''
        self.states.clear()
        self.transfunc.clear()
        self.acceptingStates.clear()

        '''状態の集合　を row() 文字列の集合として管理する。
        Angluin の論文の方法そのままで row() 文字列を状態として
        扱うための辞書。
        self.states には、Angluin の論文の方法そのままではなく、
        row() 文字列が同じになる接頭辞のうち、最も短く辞書式順序となるものを
        self.states に登録して状態とする。'''     
        rowstates = dict()
        
        '''初期状態（空文字列）を登録．'''
        if obtable.EMPTYSTRING not in obtable.prefixes :
            raise ValueError("Error: Obtable has no initial state: " + str(obtable))
        rowstr = obtable.row_string(obtable.EMPTYSTRING)
        '''空記号列は明らかに最も短い辞書式順序で最初の文字列であるから'''
        rowstates[rowstr] = self.initialState
        self.states.add(self.initialState) 
        
        ''' 状態の同値類（row string が同じ状態の集合）の代表元を引く辞書 '''
        for pfx in obtable.prefixes :
            rowstr = obtable.row_string(pfx)
            if '.' in rowstr :
                ''' . があったら obtable に未定義箇所がのこっているのでエラー '''
                raise ValueError('Error: Observation table has undetermined cell. ' + pfx + ', ' + rowstr) 
            
            ''' row() 文字列を状態として追加し、接頭辞を同値類の代表元とする '''
            if rowstr in rowstates :
                if len(pfx) < len(rowstates[rowstr]) or pfx < rowstates[rowstr] :
                    rowstates[rowstr] = pfx
                continue
            rowstates[rowstr] = pfx
        
        '''状態として row() 文字列から対応する接頭辞（最も短く先のもの）を
        とりだし、遷移先を定義する。DFA クラスの状態を接頭辞としているため。'''
        for rowstate, pfx in rowstates.items() :
            self.states.add(pfx)
            if obtable.row(pfx)[obtable.EMPTYSTRING] == 1 :
                self.acceptingStates.add(pfx)
            for a in self.alphabet :
                self.transfunc[(pfx, a)] = rowstates[obtable.row_string(pfx+a)]
            
        ''' 遷移関数を定義 '''
        return 
    
    def define_machine_naive(self, obtable):
        '''とりあえず初期化'''
        self.states.clear()
        self.transfunc.clear()
        self.acceptingStates.clear()
        
        '''初期状態（空文字列）を登録．'''
        if obtable.EMPTYSTRING not in obtable.prefixes :
            raise ValueError("Error: Obtable has no initial empty-string prefix: " + str(obtable))
        '''空記号列は明らかに最も短い辞書式順序で最初の文字列であるから'''
        self.states.add(self.initialState) 
        
        reprdict = dict()        
        for pfx in obtable.prefixes :
            if pfx not in self.states : 
                if '.' in obtable.row_string(pfx) :
                    '''行文字列が不完全な接頭辞は他の接頭辞と同一視せず状態に追加'''
                    self.states.add(pfx)
                    reprdict[pfx] = pfx
                    continue
            '''同一視できる状態を探す'''
            for s in self.states:
                if obtable.rows_identical(pfx, s) :
                    '''すでに同一視できる状態が self.states にある'''
                    reprdict[pfx] = s
                    continue
            '''pfx は長さの昇順、同じ長さなら辞書式順序で枚挙されるので、同一視できる
            状態の中の代表元として使用、状態の集合に追加する'''
            self.states.add(pfx)
        
        print(self.states, reprdict)
        '''遷移関数を定義'''
        for s in self.states:
            print("s = ", s)
            if obtable.EMPTYSTRING in obtable.row(s) and obtable.row(s)[obtable.EMPTYSTRING] == 1 :
                self.acceptingStates.add(s)
            for a in self.alphabet:
                if s+a in self.states:
                    self.transfunc[(s, a)] = s+a
                elif s+a in reprdict :
                    '''同一視する状態が登録済み'''
                    self.transfunc[(s,a)] = reprdict[s+a]
                else:
                    '''obtable が open, s+a が prefixes にない'''
                    dstpfx = obtable.agreeing_prefix(s+a)
                    if dstpfx in reprdict :
                        dstpfx = reprdict[dstpfx]
                    self.transfunc[(s,a)] = dstpfx
        return 
    
    def learn_by_mat(self):
        obtable = ObservationTable(self.alphabet)
        cx_count = 0
        ex_count = 0
        while True:
            while (ext := obtable.find_inconsistent_extension()) != None \
            or (pfx := obtable.find_open_prefix()) != None \
            or (unspec := obtable.find_unspecified()) != None :
                
                if ext != None :
                    obtable.add_suffix(ext[2])
                    print("obtable is not consistent between {} and {}. adding suffix '{}'".format(ext[0], ext[1],ext[2]))
                    print(obtable)
                    continue
                else:
                    print("obtable is consistent.")
                
                if pfx != None :
                    obtable.add_prefix(pfx)
                    print("obtable is not closed. adding prefix '{}'".format(pfx) )
                    print(obtable)
                    continue
                else:
                    print("obtable is closed.")
                
                if unspec != None :
                    xclass = input("mq unspecified: Is '{}' 1 or 0 ? ".format(unspec))
                    ex_count += 1
                    obtable.fill(unspec, xclass)
                    print(obtable)
                    self.define_machine_naive(obtable)
                    print(self)
                    continue

            print("The target machine to our knowledge:")
            self.define_machine_naive(obtable)
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

    