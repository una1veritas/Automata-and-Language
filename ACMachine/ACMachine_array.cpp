/*
 * ACMachine.cpp
 *
 *  Created on: 2017/02/27
 *      Author: sin
 */

#include "ACMachine_array.h"
#include <deque>

#include <cctype>

/*
	std::set<std::string> patterns;
	std::vector<std::map<alphabet,state>> transitions;
	std::vector<state> failures;
	std::vector<std::set<const std::string *> > output;

	state current;
 *
 */

ACMachine::ACMachine(void) {
	setupInitialState();
	resetState();
}

void ACMachine::setupInitialState(void) {
	states.push_back(State());
}

/*
ACMachine::state ACMachine::transition(const state src, const alphabet c) {
	state dst = failure[src];
	const std::map<alphabet,state>::iterator & itr = transitions[src].find(c);
	if ( itr != transitions[src].end() )
		dst = itr->second;
	return dst;
}
*/

ACMachine::state_index ACMachine::transition(const ACMachine::state_index s, const ACMachine::alphabet c) const {
	return states[s].trans[c];
}

bool ACMachine::transfer(const alphabet & c, const bool ignore_case) {
	state_index nexstate;
	nexstate = transition(current, (ignore_case ? toupper(c) : c));
	if ( nexstate == State::undefined ) {
		return false;
	}
	current = nexstate;
	return true;
}

// trace or create the path on trie from the current state
template <typename T>
ACMachine::state_index ACMachine::addPath(const T patt[]) {
	uint32 len;
	for(len = 0; patt[len] != 0; len++) {}
	return addPath(patt, len);
}

template <typename T>
ACMachine::state_index ACMachine::addPath(const T & patt) {
	return addPath(patt, patt.length());
}

template <typename T>
ACMachine::state_index ACMachine::addPath(const T & patt, const uint32 & length) {
	uint32 pos;
	state_index newstate;

	for(pos = 0; pos < length; ++pos) {
		if ( !transfer(patt[pos]) ) {
			newstate = stateCount(); //the next state of the existing last state
			states.push_back(State());
			states[current].trans[(uint16) patt[pos]] = newstate;
			//transitions[current].define(patt[pos],newstate);
			states[current].failure = initialState();
			states[current].output.clear();
			current = newstate;
		}
	}
	return current;
}

template ACMachine::state_index ACMachine::addPath<char>(const char patt[]);
template ACMachine::state_index ACMachine::addPath<ACMachine::alphabet>(const ACMachine::alphabet patt[]);
template ACMachine::state_index ACMachine::addPath<std::string>(const std::string & patt);

template <typename T>
bool ACMachine::addOutput(const T & patt) {
	states[current].output.push_back( patt.length() );
	return true;
}

template <typename T>
	bool ACMachine::addOutput(const T patt[]) {
	const std::string p(patt);
	return addOutput(p);
}

template bool ACMachine::addOutput<char>(const char patt[]);
template bool ACMachine::addOutput<std::string>(const std::string & patt);

void ACMachine::addFailures() {
	std::deque<state_index> q;

	// for states whose distance from the initial state is one.
	for(uint16 c = 0; (c = states[State::initial].firstTrans(c)) < alphabet_size; ++c) {
		const state_index & nxstate = states[State::initial].trans[c];
		// if it is neither an explicit failure, nor go-root-failure
		states[nxstate].failure  = State::initial;
		q.push_back(nxstate);
	}

	// for states whose distance from the initial state is more than one.
	while ( !q.empty() ) {
		const state_index cstate = q.front();
		q.pop_front();
		//std::cout << std::endl << "cstate " << cstate << std::endl;

		// skips if == NULL
		for (uint16 c = 0; (c = states[cstate].firstTrans((const alphabet) c)) < alphabet_size; ++c) {
		//for (uint16 c = 0; c < alphabet_size; ++c) {
			const state_index & nxstate = states[cstate].trans[c];
			//const alphabet c  = assoc.first;
			//const state nxstate = assoc.second;
			//if ( nxstate == State::undefined ) continue;
			q.push_back(nxstate);

			//std::cout << cstate << " -" << (char) c << "-> " << nxstate << std::endl;
			state_index fstate = states[cstate].failure;
			//std::cout << cstate << " ~~> " << fstate << " " << std::endl;
			state_index tsta;
			while (1) {
				tsta = transition(fstate, c);
				//std::cout << " tsta = " << tsta << std::flush;
				if ( tsta == State::undefined && fstate != State::initial ) {
					fstate = states[fstate].failure;
					//std::cout << " ~~> " << fstate << " " << std::flush;
					continue;
				}
				break;
			}
			if ( tsta == State::undefined ) {
				states[nxstate].failure = State::initial;
			} else {
				//std::cout << " add output " << states[states[nxstate].failure].output.size() << std::endl;
				states[nxstate].failure = tsta;
				states[nxstate].output.insert(states[nxstate].output.end(),
						states[states[nxstate].failure].output.begin(),
						states[states[nxstate].failure].output.end());
			}
			//std::cout << std::endl << "set "<< nxstate << " ~~> " <<  states[nxstate].failure;
			//std::cout << std::endl;
		}
	}
}

std::vector<std::pair<position, const std::string> >
	ACMachine::search(const std::string & text) {
	std::vector<std::pair<position, const std::string> > occurrs;
	std::deque<alphabet> uring;

	uint32 pos = 0;
	resetState();
	uring.clear();
	while ( pos < text.size() ) {
		if ( transfer(text[pos]) ) {
			uring.push_back(text[pos]);
			if ( !states[current].output.empty() ) {
				for(std::vector<position>::iterator it = states[current].output.begin();
						it != states[current].output.end(); it++) {
					const position patlen = *it;
					std::string patt(patlen, ' ');
					for(position i = 0; i < patlen; i++) {
						patt[i] = uring.at(uring.size() - patlen + i);
					}
					occurrs.push_back(std::pair<position,const std::string>(pos + *it + 1, patt));
				}
			}
			pos++;
		} else {
			// failure loop
			current = states[current].failure;
			if ( current == initialState() ) {
				pos++;
				//uring.push_back(text[pos]);
				uring.clear();
			} else {
				uring.pop_front();
			}
		}
	}
	return occurrs;
}

bool ACMachine::read(const alphabet & c, const bool ignore_case) {
	do {
		if ( transfer(c, ignore_case) )
			return true;
		current = states[current].failure;
	} while ( current != initialState() );
	return false;
}

std::ostream & ACMachine::printStateOn(std::ostream & out, state_index i, const std::string & pathstr) const {
	if ( i == current ) {
		out << "<" << i << ">";
	} else {
		out << i;
	}
	if ( states[i].output.size() > 0 ) {
		out << "{";
		for(std::vector<position>::const_iterator it = states[i].output.begin();
				it != states[i].output.end(); ) {
			out << pathstr.substr(pathstr.length() - *it, *it);
			if ( ++it != states[i].output.end() )
				out << ", ";
		}
		out << "}";
	}
	out << "[";
	for (uint16 c = 0; (c = states[i].firstTrans((const alphabet) c)) != alphabet_size; ++c) {
//	for(uint16 c = 0; c < alphabet_size; ++c) {
		out << "'" << (char) c << "'-> " << states[i].trans[c] << ", ";
	}
	out << "~> " << states[i].failure;
	out << "], ";

	return out;
}


std::ostream & ACMachine::printOn(std::ostream & out) const {
	std::deque<std::pair<alphabet,state_index> > path;
	state_index curr;
	std::string str;

	// dummy arc to the initial state (from nothing).
	std::pair<alphabet,state_index> dummy((alphabet) -1, State::initial);
	out << "ACMachine(";
	path.push_back(dummy);
	curr = State::initial;
	str = "";

	uint16 nextlabel;
	while ( !path.empty() ) {
		if ( curr == path.back().second ) {
			// I'm on top.
			// print curr, then go to the first child if exist
			str.resize(path.size());
			for(position i = 0; i < path.size(); i++) {
				str[i] = path[i].first;
			}
			printStateOn(out,curr, str);
			// the first transition arc
			nextlabel = states[curr].firstTrans();
		} else {
			// returned from the child that still on path top.
			// find next to path.back()
			nextlabel = path.back().first;
			path.pop_back(); // remove last edge
			curr = path.back().second;
			nextlabel = states[curr].nextTrans((const alphabet) nextlabel);
		}
		if ( nextlabel != alphabet_size ) {
			state_index nexstate = states[curr].trans[nextlabel];
			path.push_back(std::pair<alphabet,state_index>(nextlabel,nexstate)); // replace with new edge
			curr = nexstate;
		} else {
			std::pair<alphabet,state_index> aspair = path.back();
			path.pop_back();
			if ( path.empty() ) // popped the dummy path to the initial state.
				break;
			curr = path.back().second;
			path.push_back(aspair);
		}
	}

	out << ") ";
	return out;
}
