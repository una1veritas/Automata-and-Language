'''
Created on 2024/06/01

@author: Sin Shimozono
'''
import itertools
from btreeset import BTreeSet
from pickle import TRUE
from numpy import True_

class ObservationTable(object):
    EMPTYSTRING = ''
    LABEL_POSITIVE = '+'
    LABEL_NEGATIVE = '-'
    LABEL_ASSUMED_POSITIVE = '#'
    LABEL_ASSUMED_NEGATIVE = '='
    LABEL_UNKNOWN = '.'
    
    '''空の observation table を作る．有限アルファベットは与える．'''
    def __init__(self, f_alphabet : str = 'ab') :
        self.alphabet = set(f_alphabet)
        self.rows = dict()
        self.prefixes = BTreeSet(key=lambda x: (len(x), x))
        self.suffixes = BTreeSet(key=lambda x: (len(x), x))
        self.auxiliary = BTreeSet(key=lambda x: (len(x), x))
        '''
        BTreeSet/OrderedSet   --- 順序による集合．要素がソート済みになっている．
        self.alphabet --- 有限アルファベット．'' から 1 文字拡張する際に既知である必要がある. 
        self.rows     --- 行辞書の集まり，表（の中身，ます）
        self.prefixes --- 接頭辞の集合 S. なお S の要素と文字を連結した拡張接頭辞は，
        self.row （の見出し self.row.keys() ）には含まれるが，self.prefixes には含まれない．
        self.suffixes   --- 接尾辞の集合 E.
        self.auxiliary ---  接尾辞の集合 E にはふくめないが，すでに既知となった（ますが埋まった）
                            列の見出しの接尾辞の集合．self.suffixes には含まれないが，
                            self.row[s][x] が登録ずみの文字列 x. Angluin '87 にはない
        '''
        self.prefixes.add(self.EMPTYSTRING)
        self.rows[self.EMPTYSTRING] = dict()
        self.auxiliary.add(self.EMPTYSTRING)
        self.suffixes.add(self.EMPTYSTRING)
    
    def __str__(self) -> str:
        pfx_maxlen = max([len(pfx)+1 if pfx != '' else 2 for pfx in self.prefixes])
        sfx_totallen = sum([len(sfx)+1 if sfx != '' else 3 for sfx in self.suffixes])
        spc = ' '
        result =  "ObservationTable(" + "'" + ''.join(sorted(self.alphabet)) + "', \n" 
        result += f" {spc:<{pfx_maxlen}}| " + ','.join([sfx if len(sfx) > 0 else '\'\'' for sfx in self.suffixes]) \
        + "\n"
        #+ "  " + ','.join([e for e in self.auxiliary if not e in self.suffixes]) \
        result += f" {('-'*pfx_maxlen)}+{('-'*sfx_totallen)} \n"
        printedpfx = set()
        for pfx in self.prefixes :
            pfxstr = pfx if pfx != '' else '\'\''
            result += f" {pfxstr:<{pfx_maxlen}}| "
            result += self.row_string(pfx, ' ') + '\n'
            printedpfx.add(pfx)
        result += f" {('-'*pfx_maxlen)}+{('-'*sfx_totallen)} \n"
        for pfx, a in itertools.product(self.prefixes, self.alphabet) :
            if pfx+a not in self.prefixes :
                result += f" {pfx+a:<{pfx_maxlen}}| "
                result += self.row_string(pfx+a, ' ') + '\n'
            printedpfx.add(pfx+a)
        result += f" {('-'*pfx_maxlen)}+{('-'*sfx_totallen)} \n"
        # for pfx in self.rows :
        #     if pfx in printedpfx :
        #         continue
        #     result += " {0:8}| ".format(pfx)
        #     result += self.row_string_extended(pfx) + '\n'
        result += "])"
        return result
    
    def add_suffix(self, sfx):
        self.reset_assumptions()
        if sfx in self.auxiliary :
            self.auxiliary.remove(sfx)
        self.suffixes.add(sfx)
    
    def add_auxiliary(self, sfx):
        if sfx not in self.suffixes :
            self.auxiliary.add(sfx)
    
    def add_prefix(self,pfx):
        self.reset_assumptions()
        self.prefixes.add(pfx)
        if pfx not in self.rows:
            self.rows[pfx] = dict()
    
    def add_row(self,pfx):
        #self.reset_assumptions()
        if pfx not in self.rows :
            self.rows[pfx] = dict()
    
    def row(self,pfx):
        return self.rows.get(pfx, dict())
    
    def reset_assumptions(self):
        for pfx in self.rows:
            for key in self.rows[pfx]:
                if self.rows[pfx][key] in (self.LABEL_ASSUMED_NEGATIVE, self.LABEL_ASSUMED_POSITIVE) :
                    self.rows[pfx][key]= self.LABEL_UNKNOWN
                        
    '''例を使って表の空欄を埋める. '''
    '''addprefixes == True ならば，例から生じる接頭辞すべてを prefixes に登録する'''
    def fill_by_membership(self, an_example : tuple, add_prefixes = False):
        exstr, exclass = an_example
        if exclass not in (self.LABEL_POSITIVE, self.LABEL_NEGATIVE) :
            print(f"label error. reject given example {exstr}, {exclass}.")
            return 
        for i in range(0, len(exstr)+1):
            pfx = exstr[:i]
            sfx = exstr[i:]
            if add_prefixes:
                self.add_prefix(pfx)
            elif pfx not in self.rows:
                self.add_row(pfx)
                #print("added to rows", pfx,self.rows.keys())
            self.add_auxiliary(sfx)
            self.rows[pfx][sfx] = exclass
    
    def row_string(self, pfx, separator = ''):
        return separator.join([str(self.rows[pfx][s]) if pfx in self.rows and s in self.rows[pfx] else self.LABEL_UNKNOWN for s in self.suffixes])

    def extended_row_string(self, pfx):
        result = self.row_string(pfx) + " "
        if pfx in self.rows :
            result += "".join([str(self.rows[pfx].get(s, '.')) for s in self.auxiliary if not s in self.suffixes])
        else:
            result += ''.join(['.' for i in self.auxiliary if not i in self.suffixes])    
        return result

    def is_closed(self):
        return self.find_open_end_prefix() == None        
        
    def is_consistent(self):
        return self.find_inconsistent_extension() == None 
    
    def find_open_end_prefix(self):
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
                        print("find_inconsistent_extension", s1,s2,a+ext)
                        return (s1,s2,a+ext)
        return None 
    
    def rows_contradict(self, pfx1, pfx2):
        return self.find_rows_contradiction(pfx1, pfx2) != None
    
    '''returns a suffix with which transitions from the given prefixes 
    reach to both accepting and non-accepting states (prefixes).'''
    def find_rows_contradiction(self, pfx1, pfx2):
        for sfx in self.suffixes :
            if pfx1 in self.rows and sfx in self.rows[pfx1] \
            and pfx2 in self.rows and sfx in self.rows[pfx2] \
            and self.labels_contradict(self.rows[pfx1][sfx], self.rows[pfx2][sfx]) :
                return sfx
        return None
    
    def labels_contradict(self, label1, label2):
        if label1 == self.LABEL_UNKNOWN or label2 == self.LABEL_UNKNOWN :
            return False
        if label1 in (self.LABEL_ASSUMED_POSITIVE, self.LABEL_POSITIVE) \
        and label2 in ( self.LABEL_ASSUMED_NEGATIVE, self.LABEL_NEGATIVE) :
                return True
        elif label1 in (self.LABEL_ASSUMED_NEGATIVE, self.LABEL_NEGATIVE) \
        and label2 in ( self.LABEL_ASSUMED_POSITIVE, self.LABEL_POSITIVE) :
            return True
        return False
    
    def rows_agreeable(self,pfx1, pfx2):
        for suf in self.suffixes:
            c1, c2 = self.row(pfx1).get(suf,self.LABEL_UNKNOWN), self.row(pfx2).get(suf,self.LABEL_UNKNOWN)
            if c1 == c2 or c1 == self.LABEL_UNKNOWN or c2 == self.LABEL_UNKNOWN :
                continue
            if c1 in ( self.LABEL_POSITIVE, self.LABEL_ASSUMED_POSITIVE ) \
            and c2 in ( self.LABEL_POSITIVE, self.LABEL_ASSUMED_POSITIVE ) : 
                continue
            if c1 in ( self.LABEL_NEGATIVE, self.LABEL_ASSUMED_NEGATIVE ) \
            and c2 in ( self.LABEL_NEGATIVE, self.LABEL_ASSUMED_NEGATIVE ) : 
                continue
            break
        else:
            return True
        return False
    
    def find_unspecified(self):
        for pfx in sorted( set(list(self.prefixes) 
                               + [px + a for px, a in itertools.product(self.prefixes, self.alphabet)]) \
                          , key = lambda x : (len(x), x)) :
            for e in self.suffixes:
                if pfx not in self.rows or e not in self.rows[pfx] or self.rows[pfx][e] in (self.LABEL_ASSUMED_NEGATIVE, self.LABEL_ASSUMED_POSITIVE, self.LABEL_UNKNOWN):
                    #print("as px + a + e", px)
                    return pfx + e
        return None
    
class DFA(object):
    '''
    classdocs
    '''
    INITIAL_STATE = ''

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
        print(f'{q}, {c} undefined ')
        return self.UNDEFINED
    
    def accept(self, s):
        self.initiate()
        for c in s:
            self.current = self.transfer(self.current, c)
        return self.is_accept(self.current)
    
    def define_machine(self, obtable):
        '''とりあえず初期化'''
        self.states.clear()
        self.transfunc.clear()
        self.acceptingStates.clear()
        
        '''初期状態（空文字列）を登録．'''
        if obtable.EMPTYSTRING not in obtable.prefixes :
            raise ValueError("Error: Obtable has no initial empty-string prefix: " + str(obtable))
        
        '''空記号列は明らかに最も短い辞書式順序で最初の文字列であるから'''
        self.states.add(self.initialState)
        '''row_string(接頭辞) から代表元の接頭辞への写像'''
        row_dict = dict()
        row_dict[obtable.row_string(self.initialState)] = self.initialState
        for pfx in obtable.prefixes :
            rowstring = obtable.row_string(pfx)
            #print(pfx, rowstring)
            '''rowstring が完全な一致をした場合にのみ同一視し continue'''
            if rowstring not in row_dict :
                '''consistent であることを保証しつつ既存の状態 self.states 
                に同一視するか，または新規に状態として登録するか'''
                agreeable_state = None
                for s in self.states:
                    if obtable.rows_agreeable(s, pfx) :
                        agreeable_state = s
                        break
                
                self.states.add(pfx)
                row_dict[rowstring] = pfx
            else:
                continue
        
        #print(f'states = {self.states}, accepting states = {self.acceptingStates}, row_dict = {row_dict}')
        '''　Open end prefix, S.E の要素で S に等価な接頭辞を持たない、テーブルが閉じていない原因になるものへの対応'''
        for pfx, a in itertools.product(obtable.prefixes, self.alphabet) :
            pfx_a_rowstr = obtable.row_string(pfx+a) 
            if pfx_a_rowstr in row_dict :
                continue
            agreeable_state = None
            for s in self.states :
                if obtable.rows_agreeable(s, pfx+a):
                    agreeable_state = s
                    break
            if agreeable_state != None:
                '''fill by assumption'''
                for suf in obtable.suffixes:
                    #print(f'suf = "{suf}"', obtable.row(pfx+a), obtable.row(agreeable_state))
                    if obtable.row(pfx+a).get(suf,obtable.LABEL_UNKNOWN) == obtable.row(agreeable_state).get(suf,obtable.LABEL_UNKNOWN) :
                        continue
                    if obtable.row(pfx+a).get(suf,obtable.LABEL_UNKNOWN) == obtable.LABEL_UNKNOWN:
                        if obtable.row(agreeable_state)[suf] == obtable.LABEL_POSITIVE :
                            obtable.row(pfx+a)[suf] = obtable.LABEL_ASSUMED_POSITIVE 
                        elif obtable.row(agreeable_state)[suf] == obtable.LABEL_NEGATIVE :
                            obtable.row(pfx+a)[suf] = obtable.LABEL_ASSUMED_NEGATIVE 
                    elif obtable.row(agreeable_state).get(suf,obtable.LABEL_UNKNOWN) == obtable.LABEL_UNKNOWN :
                        if obtable.row(pfx+a)[suf] == obtable.LABEL_POSITIVE :
                            obtable.row(agreeable_state)[suf] = obtable.LABEL_ASSUMED_POSITIVE 
                        elif obtable.row(pfx+a)[suf] == obtable.LABEL_NEGATIVE :
                            obtable.row(agreeable_state)[suf] = obtable.LABEL_ASSUMED_NEGATIVE 
                print(f'agreeable "{pfx+a}" "{obtable.row_string(pfx+a)}" "{agreeable_state}" "{obtable.row_string(agreeable_state)}"')                
            else:
                self.states.add(pfx+a)
                row_dict[obtable.row_string(pfx+a)] = pfx+a
        #print(obtable)
        
        '''遷移関数を定義'''
        for st, a in itertools.product(self.states, self.alphabet) :
            #print(f'{st},{a}')
            rowstr = obtable.row_string(st + a)
            if rowstr in row_dict :
                self.transfunc[(st, a)] = row_dict[rowstr]
            else:
                for dst in self.states :
                    if obtable.rows_agreeable(st+a, dst) :
                        self.transfunc[(st, a)] = dst
                        break
                else:
                    raise ValueError(f'no agreeable states in self.state with transition destination {st+a}.')
        
        '''受理状態を定義'''
        for st in self.states:
            rowstr = obtable.row_string(st)
            #print(rowstr)
            if rowstr[0] in ( obtable.LABEL_POSITIVE, obtable.LABEL_ASSUMED_POSITIVE ) :
                self.acceptingStates.add(st)
        return 
    
    def learn_by_mat(self):
        obtable = ObservationTable(self.alphabet)
        cx_count = 0
        ex_count = 0
        while True:
            while (ext := obtable.find_inconsistent_extension()) != None \
            or (pfx := obtable.find_open_end_prefix()) != None \
            or (unspec := obtable.find_unspecified()) != None :
                
                if ext != None :
                    obtable.add_suffix(ext[2])
                    print("obtable is not consistent between {} and {}. adding suffix '{}'".format(ext[0], ext[1],ext[2]))
                    continue
                else:
                    print("obtable is consistent.")
                
                if pfx != None :
                    obtable.add_prefix(pfx)
                    print("obtable is not closed. adding prefix '{}'".format(pfx) )
                    continue
                else:
                    print("obtable is closed.")
                
                if unspec != None :
                    xclass = input(f"mq unspecified: Is '{unspec}' {obtable.LABEL_POSITIVE} or {obtable.LABEL_NEGATIVE} ? ")
                    ex_count += 1
                    obtable.fill_by_membership( (unspec, xclass) )
                    print(obtable)
                    self.define_machine(obtable)
                    print(self)
                    continue

            print("The target machine to our knowledge:")
            self.define_machine(obtable)
            print(self)
            cxpair = input("eq: is there a counter-example? ") 
            if not cxpair :
                break
            else:
                cxpair = cxpair.split(',')
            if len(cxpair) == 1 :
                cxpair.append(obtable.LABEL_NEGATIVE if self.accept(cxpair[0]) else obtable.LABEL_POSITIVE)
            print("counter example: {}, {}".format(cxpair[0],cxpair[1]))
            cx_count += 1
            print(cxpair)
            obtable.fill_by_membership(cxpair, add_prefixes=True)
            # while (unspec := obtable.find_unspecified()) != None :
            #     xclass = input("mq unspecified: Is '{}' 1 or 0 ? ".format(unspec))
            #     obtable.fill_by_membership(unspec, xclass)
            print(obtable)
        print("MQ: {}, EQ: {}".format(ex_count, cx_count))
        return 

    