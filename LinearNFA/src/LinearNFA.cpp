//============================================================================
// Name        : LinearNFA.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <string>
#include <map>
#include <set>
#include <cinttypes>

typedef uint8_t uint8;
typedef uint32_t uint32;
typedef uint64_t uint64;

struct NFA32 {
private:
	uint32 stateset; 	// bitset of states
	std::string pattern;
	std::map<uint64, uint32> delta; // transfer function
	uint32 finalset;

public:
	static constexpr uint8 initial_state = 0;

private:
	static constexpr uint8 initial_statebit = uint32(1)<<initial_state;
	static uint32 statebit32(uint8 i) { return uint32(1)<<i; }

public:
	NFA32(const std::string & patstr) :
		stateset(initial_statebit),
		pattern(patstr),
		delta(), finalset(0) { }

	void final(uint8 i) {
		finalset |= uint32(1)<<i;
	}

	void define(const int & srcid, const char & c, const int & dstid) {
		uint32 srcbit = statebit32(srcid);
		uint32 dstbit = statebit32(dstid);
		if ( delta.contains(srcbit<<8 | c) ) {
			delta[(srcbit<<8 | c)] |= dstbit;
		} else {
			delta[(srcbit<<8 | c)] = dstbit;
		}
	}

	uint64 transfer(const uint32 & statebits, const char & c) {
		uint32 a_state, dststates = 0;
		for(int bitpos = 0; bitpos < 32; ++bitpos) {
			a_state = statebits & statebit32(bitpos);
			if ( a_state == 0 )
				continue;
			if ( delta.contains(a_state<<8 | c) ) {
				dststates |= delta[(a_state<<8 | c)];
			} else {
				dststates |= initial_statebit;
			}
		}
		return dststates;
	}

	uint64 transfer(const char & c) {
		return stateset = transfer(stateset, c);
	}

	friend std::ostream & operator<<(std::ostream & out, const NFA32 & nfa) {
		out << "NFA(";
		out << "{";
		for(int i = 0; i < 32; ++i) {
			if ( nfa.stateset & (uint32(1)<<i) ) {
				out << i << ", ";
			}
		}
		out << "}, ";
		for(auto & keyvalue : nfa.delta) {
			out << "(" << uint32(keyvalue.first>>8) << ", " << char(keyvalue.first & 0xff) << ")-> " << keyvalue.second << ", ";
		}
		out << " final = {";
		for(int i = 0; i < 32; ++i) {
			if ( nfa.finalset & (uint32(1)<<i) ) {
				out << i << ", ";
			}
		}
		out << "} ";
		out << ") ";
		return out;
	}
};

int main() {
	std::cout << "!!!Hello World!!!" << std::endl; // prints !!!Hello World!!!

	NFA32 nfa("abcabcd");
	nfa.define(nfa.initial_state,'a',1);
	nfa.define(1,'b',2);
	nfa.define(2,'c',3);
	nfa.define(3,'a',4);
	nfa.define(4,'b',5);
	nfa.define(5,'c',6);
	nfa.define(6,'d',7);
	nfa.final(7);
	std::cout << nfa << std::endl;

	return 0;
}
