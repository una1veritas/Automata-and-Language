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
#include <cinttypes>

typedef uint8_t uint8;
typedef uint32_t uint32;
typedef uint64_t uint64;

struct NFA32 {
private:
	typedef uint32 bitset32;
	bitset32 stateset; 	// bitset of states
	std::string pattern;
	std::map<uint64, uint32> delta; // transfer function

	static constexpr uint8 initial_state = 0;

	static bitset32 singleton32(uint8 i) { return uint32(1)<<i; }
	static uint64 state_alpha(const uint8 & s, const char & c) {
		return uint64(1)<<(s+8) | c;
	}

public:
	NFA32(const std::string & patstr) :
		stateset(singleton32(initial_state)), pattern(patstr), delta() { }

	void define(const int & src, const char & c, const int & dst) {
		if ( delta.contains(state_alpha(src,c) ) ) {
			delta[state_alpha(src,c)] |= singleton32(dst);
		} else {
			delta[src] = singleton32(dst);
		}
	}

	uint64 transfer(const bitset32 & states, const char & c) {
		uint32 a_state, dststates = 0;
		for(int bitpos = 0; bitpos < 32; ++bitpos) {
			a_state = states & singleton32(bitpos);
			if ( delta.contains(state_alpha(a_state, c)) ) {
				dststates |= delta[state_alpha(a_state, c)];
			} else {
				dststates |= initial_state;
			}
		}
		return dststates;
	}

	uint64 transfer(const char & c) {
		return stateset = transfer(stateset, c);
	}

};

int main() {
	std::cout << "!!!Hello World!!!" << std::endl; // prints !!!Hello World!!!
	return 0;
}
