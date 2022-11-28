//============================================================================
// Name        : StringSearchNFA.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <iomanip>
#include <set>
#include <map>

#include <cstdint>

using namespace std;


struct NFA {
private:
	constexpr static unsigned int ALPHABET_LIMIT = 128;
	constexpr static unsigned int STATE_LIMIT = 64;

	uint64_t delta[STATE_LIMIT][ALPHABET_LIMIT];
	unsigned int initial; // the initial state.
	uint64_t finals;      // set of the final states.
	uint64_t state;   // the current state.

public:
	NFA() : initial(0), finals(0), state(0) {
		for(int s = 0; s < STATE_LIMIT; ++s) {
			for(int c = 0; c < ALPHABET_LIMIT; ++c)
				delta[s][c] = 0;
		}
	}

	void define_transfer(const int curr, const char ch, const int nx) {
		if (curr < STATE_LIMIT and ch < ALPHABET_LIMIT and nx < STATE_LIMIT)
			delta[curr][int(ch)] |= uint64_t(1)<<nx;
	}

	void define_final(const int state) {
		if (state < STATE_LIMIT)
			finals |= uint64_t(1)<<state;
	}

	uint64_t transfer(uint64_t current, const char c) {
		uint64_t nextstate = 0;
		unsigned int s;
		while (current) {
			s = __builtin_ctzll(current);
			nextstate |= delta[s][int(c)];
			current &= current - 1;
		}
		state = nextstate;
		return nextstate;
	}

	friend ostream & operator<<(ostream & out, const NFA & nfa) {
		set<char> alphabet;
		out << "NFA(";
		uint64_t states = 0;
		for(int s = 0; s < STATE_LIMIT; ++s) {
			for(int c = 0; c < ALPHABET_LIMIT; ++c) {
				if ( nfa.delta[s][c] != 0 ) {
					states |= uint64_t(1)<<s;
					states |= nfa.delta[s][c];
					alphabet.insert(char(c));
				}
			}
		}
		out << "alphabet = {";
		for(auto & c : alphabet) {
			out << c << ", ";
		}
		out << "}, ";
		out << "states = {";
		for(int s = 0; s < STATE_LIMIT; ++s) {
			if ( (states & (1LL<<s)) != 0 ) {
				out << dec << s << ", ";
			}
		}
		out << "}, ";
		out << "initial state = " << nfa.initial << ", ";
		out << "final states = {";
		for(int s = 0; s < STATE_LIMIT; ++s) {
			if ( (nfa.finals & (1LL<<s)) != 0 ) {
				out << dec << s << ", ";
			}
		}
		out << "}, ";
		out << endl;
		for(int s = 0; s < STATE_LIMIT; ++s) {
			for(int c = 0; c < ALPHABET_LIMIT; ++c) {
				if ( nfa.delta[s][c] != 0 ) {
					out << "(" << s << ", " << char(c) << ") -> {";
					for(int t = 0; t < STATE_LIMIT; ++t) {
						if ( nfa.delta[s][c] & (1LL<<t) ) {
							out << t << ", ";
						}
					}
					out << "}" << endl;
				}
			}
		}
		out << ") ";
		return out;
	}
};

int main(int argc, char * argv[]) {
	for(int i = 0; i < argc; ++i) {
		cout << argv[i] << ", ";
	}
	cout << endl;

	NFA nfa;
	nfa.define_transfer(0,'=',0);
	nfa.define_transfer(0,'+',0);
	nfa.define_transfer(0,'-',0);
	nfa.define_transfer(0,'b',0);
	nfa.define_transfer(0,'#',0);
	nfa.define_final(0);
	cout << nfa << endl;
	return 0;
}
