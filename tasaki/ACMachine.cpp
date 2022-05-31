//=======================================
// ACMachine.cpp
//=======================================

#include "ACMachine.h"
#include <deque>
#include <algorithm>
#include <cctype>
#include <unistd.h>



ACMachine::ACMachine(void) {
	setupInitialState();
	resetState();
}

void ACMachine::setupInitialState(void) {
	transitions.clear();
	transitions.push_back(std::map<alphabet, state>());
	failure.clear();
	failure.push_back(initialState());
	// failure to initial state from initial state eats up one symbol at transition.
	output.clear();
	output.push_back(std::list<position>());
	//output[initialState()].clear();
}


bool ACMachine::transfer(const alphabet & c, const bool ignore_case) {
	std::map<alphabet, state>::iterator itr;
	if (ignore_case) {
		itr = transitions[current].find(toupper(c));
		if (itr == transitions[current].end())
			itr = transitions[current].find(tolower(c));
	}
	else {
		itr = transitions[current].find(c);
	}
	if (itr == transitions[current].end()) {
		return false;
	}
	current = itr->second;
	return true;
}


template <typename T>
ACMachine::state ACMachine::addPath(const T & patt) {
	return addPath(patt, patt.length());
}

template <typename T>
ACMachine::state ACMachine::addPath(const T & patt, const uint32 & length) {
	uint32 pos;
	state newstate;

	for (pos = 0; pos < length; ++pos) {
	  if (!transfer((unsigned char)patt[pos])) {
			newstate = transitions.size(); //the next state of the existing last state
			transitions.push_back(std::map<alphabet, state>());
			(transitions[current])[(unsigned char)patt[pos]] = newstate;

			failure.push_back(initialState());
			output.push_back(std::list<position>());
			//count++;
			current = newstate;
		}
	}
	return current;
}

//template ACMachine::state ACMachine::addPath<char>(const char patt[]);
//template ACMachine::state ACMachine::addPath<ACMachine::alphabet>(const ACMachine::alphabet patt[]);
template ACMachine::state ACMachine::addPath<std::string>(const std::string & patt);


template <typename T>
bool ACMachine::addOutput(const T & patt) {
	output[current].push_back(patt.length());
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

	//int addcount = 0;

	// for states whose distance from the initial state is one.
	//	std::cout << "states within distance one: ";
	for (auto const & assoc : transitions[initial_state]) {
		//const alphabet c = assoc.first;
		const state nxstate = assoc.second;
		// if is neither an explicit failure, nor go-root-failure
		failure[nxstate] = initial_state;
		q.push_back(nxstate);
		//std::cout <<"nxstate " << nxstate << std::endl;
	}
	//std::cout << std::endl;

	// for states whose distance from the initial state is more than one.
	while (!q.empty()) {
		const state cstate = q.front();
		q.pop_front();
		//		std::cout << std::endl << "cstate " << cstate << std::endl;

		// skips if == NULL
		for (auto const & assoc : transitions[cstate]) {
			const alphabet c = assoc.first;
			const state nxstate = assoc.second;
			q.push_back(nxstate);

			//			std::cout << cstate << " -" << (char) c << "-> " << nxstate << std::endl;

			state fstate = failure[cstate];
			//			std::cout << cstate << " ~~> " << fstate << " ";
			std::map<alphabet, state>::iterator itp;
			while (1) {
				itp = transitions[fstate].find(c);
				if (itp == transitions[fstate].end() && fstate != initial_state) {
					fstate = failure[fstate];
					//					std::cout << " ~~> " << fstate << " ";
				}
				else {
					break;
				}
			}
			if (itp == transitions[fstate].end()) {
				failure[nxstate] = initial_state;
			}
			else {
				failure[nxstate] = itp->second;
				if (!output[itp->second].empty()){

					if(output[nxstate].empty()){
						for(auto itp_fs = output[itp->second].begin(); itp_fs != output[itp->second].end(); itp_fs++){
							output[nxstate].push_back(*itp_fs);
						}
					}
					else{
						auto itp_ns = output[nxstate].begin();
						for(auto itp_fs = output[itp->second].begin(); itp_fs != output[itp->second].end(); ){
							if(*itp_fs < *itp_ns){
								output[nxstate].insert(itp_ns, *itp_fs);
								itp_fs++;
							}
							else if(*itp_fs == *itp_ns){
								itp_fs++;
								itp_ns++;
							}
							else{
								itp_ns++;
							}
						}
					}
				}

			}
			//			std::cout << std::endl << "set "<< nxstate << " ~~> " <<  failure[nxstate];
			//			std::cout << std::endl;
		}
	}

}



bool ACMachine::read(const alphabet & c, const bool ignore_case) {
	//std::cout << "current state " << current  << std::endl;
	do {
		if (transfer(c, ignore_case)){
			//std::cout << "transfer success" << std::endl;
			//std::cout << "current state " << current << std::endl;
			return true;
		}
		//std::cout << "transfer fail" << std::endl;
		current = failure_array[current];
		//std::cout << "failure" << std::endl;
		//std::cout << "current state " << current  << std::endl;
	} while (current != initialState());
	return false;
}



