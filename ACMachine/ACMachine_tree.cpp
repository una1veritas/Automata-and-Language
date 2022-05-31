/*
 * ACMachine.cpp
 *
 *  Created on: 2017/02/27
 *      Author: sin
 */

#include <deque>

#include <cctype>
#include "ACMachine_tree.h"

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
	states.clear();
	states.push_back(TransitionTable());
	failure.clear();
	failure.push_back(initialState());
	// failure to initial state from initial state eats up one symbol at transition.
	output.clear();
	output.push_back(std::vector<position>());
	output[initialState()].clear();
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

ACMachine::state ACMachine::transition(const ACMachine::state s, const ACMachine::alphabet c) const {
	TransitionTable::const_iterator c_itr;
	if ( (c_itr = states[s].find(c)) == states[s].end() ) {
		return undef_state;
	}
	return c_itr->second;
}

bool ACMachine::transfer(const alphabet & c, const bool ignore_case) {
	state nexstate;
	nexstate = transition(current, (ignore_case ? toupper(c) : c));
	if ( nexstate == undef_state ) {
		return false;
	}
	current = nexstate;
	return true;
}



// trace or create the path on trie from the current state
template <typename T>
ACMachine::state ACMachine::addPath(const T patt[]) {
	uint32 len;
	for(len = 0; patt[len] != 0; len++) {}
	return addPath(patt, len);
}

template <typename T>
ACMachine::state ACMachine::addPath(const T & patt) {
	return addPath(patt, patt.length());
}

template <typename T>
ACMachine::state ACMachine::addPath(const T & patt, const uint32 & length) {
	uint32 pos;
	state newstate;

	for(pos = 0; pos < length; ++pos) {
		if ( !transfer(patt[pos]) ) {
			newstate = stateCount(); //the next state of the existing last state
			states.push_back(TransitionTable());
			(states[current])[patt[pos]] = newstate;
			//transitions[current].define(patt[pos],newstate);
			failure.push_back(initialState());
			output.push_back(std::vector<position>());
			current = newstate;
		}
	}
	return current;
}

template ACMachine::state ACMachine::addPath<char>(const char patt[]);
template ACMachine::state ACMachine::addPath<ACMachine::alphabet>(const ACMachine::alphabet patt[]);
template ACMachine::state ACMachine::addPath<std::string>(const std::string & patt);

template <typename T>
bool ACMachine::addOutput(const T & patt) {
	output[current].push_back( patt.length() );
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
	std::deque<state> q;

	// for states whose distance from the initial state is one.
//	std::cout << "states within distance one: ";
	for(std::pair<alphabet,state> const & nxpair : states[initial_state] ) {
		// if is neither an explicit failure, nor go-root-failure
		failure[nxpair.second]  = initial_state;
		q.push_back(nxpair.second);
//		std::cout << nxstate << ", ";
	}
//	std::cout << std::endl;

	// for states whose distance from the initial state is more than one.
	while ( !q.empty() ) {
		const state cstate = q.front();
		q.pop_front();
//		std::cout << std::endl << "cstate " << cstate << std::endl;

		// skips if == NULL
		for(auto const & nxpair : states[cstate] ) {
			//const alphabet c  = assoc.first;
			//const state nxstate = assoc.second;
			q.push_back(nxpair.second);

//			std::cout << cstate << " -" << (char) c << "-> " << nxstate << std::endl;

			state fstate = failure[cstate];
//			std::cout << cstate << " ~~> " << fstate << " ";
			state tsta;
			while (1) {
				tsta = transition(fstate, nxpair.first);
				if ( tsta == undef_state && fstate != initial_state ) {
					fstate = failure[fstate];
					continue;
//					std::cout << " ~~> " << fstate << " ";
				}
				break;
			}
			if ( tsta == undef_state ) {
				failure[nxpair.second] = initial_state;
			} else {
				failure[nxpair.second] = tsta;
				output[nxpair.second].insert(output[nxpair.second].end(),
						output[failure[nxpair.second]].begin(),output[failure[nxpair.second]].end());
			}
//			std::cout << std::endl << "set "<< nxstate << " ~~> " <<  failure[nxstate];
//			std::cout << std::endl;
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
			if ( !output[current].empty() ) {
				for(std::vector<position>::iterator it = output[current].begin();
						it != output[current].end(); it++) {
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
			current = failure[current];
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
		current = failure[current];
	} while ( current != initialState() );
	return false;
}



std::ostream & ACMachine::printStateOn(std::ostream & out, state i, const std::string & pathstr) const {
	if ( i == current ) {
		out << "<" << i << ">";
	} else {
		out << i;
	}
	if ( output[i].size() > 0 ) {
		out << "{";
		for(auto it = output[i].begin(); it != output[i].end(); ) {
			out << pathstr.substr(pathstr.length() - *it, *it);
			if ( ++it != output[i].end() )
				out << ", ";
		}
		out << "}";
	}
	out << "[";
	for(std::map<alphabet,state>::const_iterator it = states[i].begin();
			it != states[i].end(); it++) {
		out << "'" << (char)it->first << "'-> " << it->second << ", ";
	}
	out << "~> " << failure[i];
	out << "], ";

	return out;
}


std::ostream & ACMachine::printOn(std::ostream & out) const {
	std::deque<std::pair<alphabet,state> > path;
	state curr;
	std::string str;

	// dummy arc to the initial state (from nothing).
	std::pair<alphabet,state> dummy(alph_end,initial_state);
	out << "ACMachine(";
	path.push_back(dummy);
	curr = initial_state;
	str = "";
	//printStateOn(out,curr,str);

	alphabet nextlabel;
	while ( !path.empty() ) {
		if ( curr == path.back().second ) {
			// I'm on top.
			// print curr, then go to the first child if exist
			str.resize(path.size());
			for(position i = 0; i < path.size(); i++) {
				str[i] = path[i].first;
			}
			printStateOn(out,curr, str);
			; // the first transition arc
			if ( states[curr].begin() != states[curr].end() ) {
				nextlabel = states[curr].begin()->first;
			} else {
				nextlabel = alph_end;
			}
		} else {
			// returned from the child that still on path top.
			// find next to path.back()
			nextlabel = path.back().first;
			path.pop_back(); // remove last edge
			curr = path.back().second;
			TransitionTable::const_iterator it = states[curr].find(nextlabel);
			++it;
			// the next transition arc
			if ( it != states[curr].end() ) {
				nextlabel = it->first;
			} else {
				nextlabel = alph_end;
			}
		}
		if ( nextlabel != alph_end ) {
			state nexstate = states[curr].find(nextlabel)->second;
			path.push_back(std::pair<alphabet,state>(nextlabel,nexstate)); // replace with new edge
			curr = nexstate;
		} else {
			std::pair<alphabet,state> aspair = path.back();
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
