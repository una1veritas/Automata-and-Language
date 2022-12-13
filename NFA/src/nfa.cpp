/*
 ============================================================================
 Name        : nfa.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <iostream>
#include <string>
#include <sstream>

#include <cinttypes>
#include <cctype>

#include <vector>
#include <set>

using namespace std;

using uint64 = uint64_t;
using uint = unsigned int;

struct bitset64 {
private:
	uint64 bits;

public:
	bitset64(void) : bits(0) { }
	bitset64(uint64 intval) : bits(intval) { }

	constexpr static uint limit = 64;

	bitset64 & operator=(const uint64 & intval) { bits = intval; return *this; }

	bool operator[](const uint & i) const { return (bits>>i) & 1; }
	bitset64 & set(const uint & i) { bits |= 1LL<<i; return *this; }
	bitset64 & clear(const uint & i) { bits &= ~(1LL<<i); return *this; }
	bool operator==(const bitset64 & b) const { return bits == b.bits; }
	bool operator==(const uint64 & intval) const { return bits == intval; }
	bool operator!=(const bitset64 & b) const { return bits != b.bits; }
	bool operator!=(const uint64 & intval) const { return bits != intval; }

	bitset64 & operator|=(const uint64 & intval) { bits |= intval; return *this; }

	explicit operator uint64() const { return bits; }
	bitset64 operator&(const bitset64 & b) const { return bitset64(bits & b.bits); }

	friend ostream & operator<<(ostream & out, const bitset64 & bset) {
		out << "{";
		uint bitpos = 0;
		uint cnt = 0;
		uint64 mask = 1;
		for(; mask != 0; ++bitpos, mask <<= 1) {
			if ( mask & bset.bits ) {
				if ( cnt ) out << ", ";
				out << std::dec << bitpos;
				++cnt;
			}
		}
		out << "}";
		return out;
	}

};

struct NFA {
private:
	/* 整数のビット長により設定する上限 */
	constexpr static unsigned int ALPHABET_LIMIT = 128;

	/* 状態は 数字，英大文字を含む空白 (0x20) から _ (0x5f) までの一文字 */
	/* に対応させる正の整数 {0,...,63} の要素に限定. */
	/* 文字は ASCII 文字, char 型の {0,...,127} の要素に限定. */
	bitset64 delta[bitset64::limit][ALPHABET_LIMIT]; /* 遷移関数 : Q x Σ -> 2^Q*/
	uint initial; /* 初期状態 */
	bitset64 finals; /* 最終状態を表すフラグの表 */

	bitset64 current;

// ユーティリティ
	/*
	 #define char2state(x)  (tolower(x) - 0x30)
	 #define state2char(x)  ((x) + 0x30)
	 */

	/* 定数 */
	constexpr static uint TRANSITION_NOT_DEFINED = 0;
	constexpr static uint STATE_IS_NOT_FINAL = 0;
	constexpr static uint STATE_IS_FINAL = 1;

	/* 定義文字列から nfa を初期化 */
public:
	void define(string &transdef, string &initialstate, string &finalstates) {
		//char triplex[72];
		//char buf[72];
		//char * ptr = trans;

		/* データ構造の初期化 */
		for (uint i = 0; i < bitset64::limit; ++i) {
			for (uint a = 0; a < ALPHABET_LIMIT; ++a) { /* = 1 からでもよいが */
				delta[i][a] = 0; /* 空集合に初期化 */
			}
		}
		finals = 0;

		istringstream stream(transdef);
		/* 定義の三つ組みを読み取る */
		string item;
		string delim = ",";
		vector<string> items;
		while (std::getline(stream, item, delim)) {
			items.push_back(item);
		}
		for (const auto & item : items) {
			int stat = std::stol(item.substr(0,1));
			int symb = uint(item[1]);
			for (uint i = 2; i < item.length() ; ++i) { /* 遷移先は複数記述可能 */
				delta[stat][symb] |= 1LL << std::stol(item.substr(i,1));
			}
		}
		initial.set(std::stol(initialstate)); /* 初期状態は１つ */
		for (uint i = 0; i < finals.length(); ++i) {
			finals.set(std::stol(finals.substr(i,1)));
		}
	}

	void reset() {
		current = 1LL << initial;
	}

	bitset64& transfer(char a) {
		bitset64 next = 0;
		for (uint i = 0; i < bitset64::limit; ++i) {
			if (current[i]) {
				if (delta[i][(int) a] != 0) /* defined */
					next |= mp->delta[i][(int) a];
				//else /* if omitted, go to and self-loop in the ghost state. */
			}
		}
		return current = next;
	}

	bool accepting() {
		return (finals & current) == 0;
	}

	friend ostream& operator<<(ostream &out, const NFA & nfa) {
		bset64 states;
		set<char> alphabet;
		char buf[160];

		states = 0;
		for (int a = 0; a < ALPHABET_LIMIT; ++a) {
			alphabet[a] = 0;
		}
		for (int i = 0; i < STATE_LIMIT; ++i) {
			for (int a = 0; a < ALPHABET_LIMIT; ++a) {
				if (mp->delta[i][a]) {
					states |= 1 << i;
					states |= (int) mp->delta[i][a];
					alphabet[a] = 1;
				}
			}
		}
		printf("nfa(\n");
		printf("states = %s\n", bset64_str(states, buf));
		printf("alphabet = {");
		int the1st = 1;
		for (int i = 0; i < ALPHABET_LIMIT; ++i) {
			if (alphabet[i]) {
				if (!the1st) {
					printf(", ");
				}
				printf("%c", (char) i);
				the1st = 0;
			}
		}
		printf("},\n");

		printf("delta = \n");
		printf("state symbol| next\n");
		printf("------------+------\n");
		for (int i = 0; i < STATE_LIMIT; ++i) {
			for (int a = 0; a < ALPHABET_LIMIT; ++a) {
				if (mp->delta[i][a]) {
					printf("  %c  ,  %c   | %s \n", state2char(i), a,
							bset64_str(mp->delta[i][a], buf));
				}
			}
		}
		printf("------------+------\n");
		printf("initial state = %x\n", mp->initial);
		printf("accepting states = %s\n", bset64_str(mp->finals, buf));
		printf(")\n");
		fflush(stdout);
	}

	int run(char *inputstr) {
		char *ptr = inputstr;
		char buf[128];
		printf("run on '%s' :\n", ptr);
		nfa_reset(mp);
		printf("     -> %s", bset64_str(mp->current, buf));
		for (; *ptr; ++ptr) {
			nfa_transfer(mp, *ptr);
			printf(", -%c-> %s", *ptr, bset64_str(mp->current, buf));
		}
		if (nfa_accepting(mp)) {
			printf(", \naccepted.\n");
			fflush(stdout);
			return STATE_IS_FINAL;
		} else {
			printf(", \nrejected.\n");
			fflush(stdout);
			return STATE_IS_NOT_FINAL;
		}
	}
};

int command_arguments(int , char ** , char ** , char * , char ** , char *);

int main(int argc, char **argv) {
	char * delta = "0a01,0b0,0c0,1a0,1b02,1c0,2a0,2b03,2c0,3a3,3b3,3c3", initial = '0', *finals = "3";
	char input_buff[1024] = "acabaccababbacbbac";
	if ( command_arguments(argc, argv, &delta, &initial, &finals, input_buff) )
		return 1;

	nfa M;
	//printf("M is using %0.2f Kbytes.\n\n", (double)(sizeof(M)/1024) );
	nfa_define(&M, delta, initial, finals);
	nfa_print(&M);
	if (strlen(input_buff))
		nfa_run(&M, input_buff);
	else {
		printf("Type an input as a line, or quit by the empty line.\n");
		fflush(stdout);
		/* 標準入力から一行ずつ，入力文字列として走らせる */
		while( fgets(input_buff, 1023, stdin) ) {
			char * p;
			for(p = input_buff; *p != '\n' && *p != '\r' && *p != 0; ++p) ;
			*p = '\0'; /* 行末の改行は消す */
			if (!strlen(input_buff))
				break;
			nfa_run(&M, input_buff);
		}
	}
	printf("bye.\n");
	return 0;
}

int command_arguments(int argc, char * argv[], char ** delta, char * initial, char ** finals, char * input) {
	if (argc > 1) {
		if (strcmp(argv[1], "-h") == 0 ) {
			printf("usage: command \"transition triples\" \"initial state\" \"final states\" (\"input string\")\n");
			printf("example: dfa.exe \"%s\" \"%c\" \"%s\"\n\n", *delta, *initial, *finals);
			return 1;
		} else if (argc == 4 || argc == 5 ) {
			*delta = argv[1]; *initial = argv[2][0]; *finals = argv[3];
			if (argc == 5 )
				strcpy(input, argv[4]);
			else
				input[0] = '\0';
		} else {
			printf("Illegal number of arguments.\n");
			return 1;
		}
	} else {
		printf("define M by built-in example: \"%s\" \"%c\" \"%s\"\n", *delta, *initial, *finals);
		printf("(Use 'command -h' to get a help message.)\n\n");
	}
	return 0;
}
