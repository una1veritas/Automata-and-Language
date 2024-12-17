実行例）
% python3 fgrammer.py "SA" "ab" "S->|b|aA, S->bS, A-> a, A->aS, A -> bA " "S" 4
G=FormalGrammer({S, A}, {a, b}, {S->|aA|b|bS, A->a|aS|bA}, S)
result = ['', 'b', 'aa', 'bb', 'aab', 'aba', 'baa', 'bbb', 'aaaa', 'aabb', 'abab', 'abba', 'baab', 'baba', 'bbaa', 'bbbb']

第１引数：　非終端記号を列挙した文字列
第２引数；　終端記号（アルファベット，アスキーコードで１文字）を列挙した文字列
第３引数：　生成規則を列挙した文字列，左辺 -> 右辺 の形式で，左辺は非終端記号一文字，
右辺は非終端記号と終端記号からなる文字列，ただし | で右辺のみ異なる複数のルールを記述できる．
左辺が同じ（右辺がことなる）ルールを複数記述することもできる．
第４引数：　開始記号．
第５引数：　生成する文字列の長さ上限


"SAB" "ab" "S→aAbB,A→|aA,B→|bB" "S" 7
result = ['ab', 'aab', 'abb', 'aaab', 'aabb', 'abbb', 'aaaab', 'aaabb', 'aabbb', 'abbbb', 'aaaaab', 'aaaabb', 'aaabbb', 'aabbbb', 'abbbbb']

"SAB" "ab" "S→aAb|bAa|bBb,A→|aAb|bAa,B→bBa" "S" 7
result = ['ab', 'ba', 'aabb', 'abab', 'baba', 'bbaa', 'aaabbb', 'aababb', 'ababab', 'abbaab', 'baabba', 'bababa', 'bbabaa', 'bbbaaa']

"SAB" "ab" "S→A|B,A→|aaAa|bBbb,B→|bBbb|aaAa" "S" 7
result = ['', 'aaa', 'bbb', 'aaaaaa', 'aabbba', 'baaabb', 'bbbbbb']

"SABCD" "ab" "S→AB|BA|AC|BD,A→a,B→b,C→SB,D→SA" "S" 7
result = ['ab', 'ba', 'abab', 'aabb', 'bbaa', 'baba', 'bbabaa', 'baabba', 'bababa', 'aababb', 'abbaab', 'aaabbb', 'ababab', 'bbbaaa']

"SABCD" "ab" "S->AB|AC|BD|BC, A->a, B->b, C->SB, D->SB" "S" 6
result = ['ab', 'babb', 'aabb', 'aaabbb', 'baabbb', 'bbabbb', 'ababbb']
