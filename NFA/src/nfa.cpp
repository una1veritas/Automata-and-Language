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

	explicit operator bool() const { return bits != 0; }
	explicit operator uint64() const { return bits; }

	bool operator[](const uint & i) const { return (bits>>i) & 1; }
	bitset64 & set(const uint & i) { bits |= 1LL<<i; return *this; }
	bitset64 & clear(const uint & i) { bits &= ~(1LL<<i); return *this; }
	bool operator==(const bitset64 & b) const { return bits == b.bits; }
	bool operator==(const uint64 & intval) const { return bits == intval; }
	bool operator!=(const bitset64 & b) const { return bits != b.bits; }
	bool operator!=(const uint64 & intval) const { return bits != intval; }

	bitset64 & operator|=(const uint64 & intval) { bits |= intval; return *this; }
	bitset64 & operator|=(const bitset64 & b) { bits |= b.bits; return *this; }

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
	NFA(const string &transdef, const string &initialstate, const string &finalstates) {
		define(transdef, initialstate, finalstates);
	}

	void define(const string &transdef, const string &initialstate, const string &finalstates) {
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
		char delim = ',';
		vector<string> items;
		while ( getline(stream, item, delim)) {
			items.push_back(item);
		}
		for (const auto & item : items) {
			int stat = std::stol(item.substr(0,1));
			int symb = uint(item[1]);
			for (uint i = 2; i < item.length() ; ++i) { /* 遷移先は複数記述可能 */
				delta[stat][symb] |= 1LL << std::stol(item.substr(i,1));
			}
		}
		initial = std::stol(initialstate); /* 初期状態は１つ */
		for (uint i = 0; i < finalstates.length(); ++i) {
			finals.set(std::stol(finalstates.substr(i,1)));
		}
	}

	void reset() {
		current = 1LL << initial;
	}

	bitset64& transfer(char a) {
		bitset64 next = 0;
		for (uint i = 0; i < bitset64::limit; ++i) {
			if ( current[i] ) {
				if ( !bool(delta[i][uint(a)]) ) /* defined */
					next |= delta[i][uint(a)];
				//else /* if omitted, go to and self-loop in the ghost state. */
			}
		}
		return current = next;
	}

	bool accepting() {
		return (finals & current) == 0;
	}

	friend ostream& operator<<(ostream &out, const NFA & nfa) {
		bitset64 states;
		set<char> alphabet;

		states = 0;
		for (uint i = 0; i < bitset64::limit; ++i) {
			for (uint a = 0; a < ALPHABET_LIMIT; ++a) {
				if ( bool(nfa.delta[i][a]) ) {
					states |= (1LL << i);
					states |= uint64(nfa.delta[i][a]);
					alphabet.insert(char(a));
				}
			}
		}
		out << "nfa(" << endl;
		out << "states = " << states << endl;
		out << "alphabet = {";
		int the1st = 1;
		for (uint i = 0; i < ALPHABET_LIMIT; ++i) {
			if (alphabet.contains(char(i))) {
				if (!the1st) {
					out << ", ";
				}
				out << char(i);
				the1st = 0;
			}
		}
		out << "}," << endl;

		out << "delta = " << endl;
		out << "state symbol| next" << endl;
		out << "------------+------" << endl;
		for (uint i = 0; i < bitset64::limit; ++i) {
			for (uint a = 0; a < ALPHABET_LIMIT; ++a) {
				if ( bool(nfa.delta[i][a]) ) {
					out << "  " << i << "  ,  "<< char(a) << "   | " << nfa.delta[i][a] << endl;
				}
			}
		}
		out << "------------+------" << endl;
		out << "initial state = " << nfa.initial << endl;
		out << "accepting states = " << nfa.finals << endl;
		out << ")" << endl;
		return out;
	}

	int run(const string & inputstr) {
		uint pos;
		cout << "run on '<< inputstr << ' :" << endl;
		reset();
		cout << "     -> " << current;
		for (pos = 0; pos < inputstr.length(); ++pos) {
			transfer(inputstr[pos]);
			cout << ", -" << inputstr[pos] << "-> " << current;
		}
		if (accepting()) {
			cout << ", " << endl << "accepted." << endl;
			return STATE_IS_FINAL;
		} else {
			cout << ", "<< endl << "rejected." << endl;
			return STATE_IS_NOT_FINAL;
		}
	}
};

int command_arguments(const int , const char ** , string &, string &, string &, string &);

int main(const int argc, const char **argv) {
	string delta = "0a01,0b0,0c0,1a0,1b02,1c0,2a0,2b03,2c0,3a3,3b3,3c3", initial = "0", finals = "3";
	string input_buff = "acabaccababbacbbac";
	if ( command_arguments(argc, argv, delta, initial, finals, input_buff) )
		return 1;

	NFA M(delta, initial, finals);
	//printf("M is using %0.2f Kbytes.\n\n", (double)(sizeof(M)/1024) );
	cout << M << endl;
	if ( input_buff.length() )
		M.run(input_buff);
	else {
		cout << "Type an input as a line, or quit by the empty line." << endl;
		/* 標準入力から一行ずつ，入力文字列として走らせる */
		while( std::getline(cin, input_buff, '\n') ) {
			if (! input_buff.length() )
				break;
			M.run(input_buff);
		}
	}
	printf("bye.\n");
	return 0;
}

int command_arguments(const int argc, const char * argv[], string & delta, string & initial, string & finals, string & input) {
	if (argc > 1) {
		if ((string)argv[1] == (string)"-h") {
			cout << "usage: command \"transition triples\" \"initial state\" \"final states\" (\"input string\")" << endl;
			cout << "example: dfa.exe \"" << delta << "\" \"" << initial <<  "\" \"" << finals << "\"" << endl << endl;
			return 1;
		} else if (argc == 4 || argc == 5 ) {
			delta = argv[1]; initial = argv[2][0]; finals = argv[3];
			if (argc == 5 )
				input = argv[4];
			else
				input = "";
		} else {
			cout << "Illegal number of arguments." << endl;
			return 1;
		}
	} else {
		cout << "define M by built-in example: dfa.exe \"" << delta << "\" \"" << initial <<  "\" \"" << finals << "\"" << endl << endl;
		cout << "(Use 'command -h' to get a help message.)" << endl << endl;
	}
	return 0;
}
