/*
 * ACMachine.h
 *
 *  Created on: 2017/02/27
 *      Author: sin
 */

#ifndef ACMACHINE_ARRAY_H_
#define ACMACHINE_ARRAY_H_

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

#include <cinttypes>
#include <cstring>

typedef size_t position;

class ACMachine {
public:
	typedef int32_t state_index;
	typedef uint8_t alphabet;

private:
	struct aspair {
		alphabet label;
		state_index state;

		aspair(const alphabet c) : label(c), state(State::undefined) {}
		aspair(const alphabet c, const state_index nstate) : label(c), state(nstate) {}
	};

	struct ascompare {
		bool operator() (const aspair & left, const aspair & right) {
			return left.label < right.label;
		}
	};

	struct State {
		std::vector<aspair> trans;
		state_index failure;
		std::vector<position> output;

		enum {
			initial = 0,
			undefined = (state_index) -1,
		};

		State() {
			trans.clear();
			failure = initial;
			output.clear();
		}

		uint32_t byteSize() const {
			return sizeof(State) + trans.size() * sizeof(aspair) + output.size() * sizeof(position);
		}

		state_index transition(const alphabet c) const {
			ascompare comp;
			aspair a_pair(c);
			std::vector<aspair>::const_iterator itr = std::lower_bound(trans.begin(), trans.end(), a_pair, comp);
			if ( itr == trans.end() || itr->label != c )
				return State::undefined;
			return itr->state;
		}

		state_index transition(const alphabet c, state_index state) {
			ascompare comp;
			aspair a_pair(c);
			std::vector<aspair>::iterator itr = std::lower_bound(trans.begin(), trans.end(), a_pair, comp);
			if ( itr == trans.end() || itr->label != c ) {
				trans.insert(itr, aspair(c,state));
			} else {
				itr->state = state;
			}
			return state;
		}

		std::vector<aspair>::const_iterator nextTransition(const alphabet c) const {
			ascompare comp;
			aspair a_pair(c);
			std::vector<aspair>::const_iterator itr = std::lower_bound(trans.begin(), trans.end(), a_pair, comp);
			return itr;
		}

	};
	std::vector<State> states;
	state_index current;

private:
	std::ostream & printStateOn(std::ostream & out, state_index i, const std::string & pathstr) const;

	void setupInitialState(void);
	state_index initialState() const { return State::initial; }
	bool transfer(const alphabet & c, const bool ignore_case = false);

	state_index transition(const state_index s, const alphabet c) const;

public:
	ACMachine(void);

	uint32_t stateCount() const { return states.size(); }
	uint32_t byteSize() const {
		uint32_t sum = sizeof(ACMachine);
		for (auto itr = states.begin(); itr != states.end(); ++itr)
			sum += itr->byteSize();
		return sum;
	}

	state_index resetState() { return current = State::initial; }
	state_index currentState() const { return current; }

	bool atInitialState() const { return current == State::initial; }

	const std::vector<position> & currentOutput() const { return states[current].output; }

	// add patt to the trie and output of the destination state.
	template <typename T>
		state_index addPath(const T & patt, const position & length);
	template <typename T>
		state_index addPath(const T patt[]);
	template <typename T>
		state_index addPath(const T & patt);

	bool addOutput(const std::string & patt);
	bool addOutput(const char patt[]);

	void addFailures();

	template <typename C>
	void addPatterns(const C & strset) {
		for(auto str : strset ) {
			resetState();
			addPath(str);
			addOutput(str);
		}
		addFailures();
	}

	std::vector<std::pair<position,const std::string>> search(const std::string & text);
	bool read(const alphabet & c, const bool ignore_case = false);

	std::ostream & printOn(std::ostream & out) const;

	friend std::ostream & operator<<(std::ostream & out, const ACMachine & acm) {
		return acm.printOn(out);
	}

};

#endif /* ACMACHINE_ARRAY_H_ */
