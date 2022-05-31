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
	inv_failure.clear();
	inv_failure.push_back(std::set<state>());
	inv_failure[initialState()].clear();
	// failure to initial state from initial state eats up one symbol at transition.
	output.clear();
	output.push_back(std::set<position>());
	output[initialState()].clear();
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


// trace or create the path on trie from the current state
template <typename T>
ACMachine::state ACMachine::addPath(const T patt[]) {
	uint32 len;
	for (len = 0; patt[len] != 0; len++) {}
	return addPath(patt, len);
}

template <typename T>
ACMachine::state ACMachine::addPath(const T & patt) {
	return addPath(patt, patt.length());
}

template <>
ACMachine::state ACMachine::addPath<char>(const char & patt) {
	std::string p{ patt };
	return addPath(p, 1);
}

template <typename T>
ACMachine::state ACMachine::addPath(const T & patt, const uint32 & length) {
	uint32 pos;
	state newstate;

	for (pos = 0; pos < length; ++pos) {
		if (!transfer(patt[pos])) {
			newstate = transitions.size(); //the next state of the existing last state
			transitions.push_back(std::map<alphabet, state>());
			(transitions[current])[patt[pos]] = newstate;
			failure.push_back(initialState());
			inv_failure.push_back(std::set<state>());
			output.push_back(std::set<position>());
			current = newstate;
		}
	}
	return current;
}

template ACMachine::state ACMachine::addPath<char>(const char patt[]);
template ACMachine::state ACMachine::addPath<ACMachine::alphabet>(const ACMachine::alphabet patt[]);
template ACMachine::state ACMachine::addPath<std::string>(const std::string & patt);


//template void ACMachine::addfailurestates<char>(failurestates fst, const char patt[]);
//template void ACMachine::addfailurestates<ACMachine::alphabet>(failurestates fst, const ACMachine::alphabet patt[]);
//template void ACMachine::addfailurestates<std::string>(failurestates fst, const std::string & patt);


template <typename T>
bool ACMachine::addOutput(const T & patt) {
	std::pair<std::set<position>::iterator, bool> res = output[current].insert(patt.length());
	return res.second;
}

template <typename T>
bool ACMachine::addOutput(const T patt[]) {
	const std::string p(patt);
	return addOutput(p);
}

template <>
bool ACMachine::addOutput<char>(const char & patt) {
	const std::string p{ patt };
	return addOutput(p);
}

template bool ACMachine::addOutput<char>(const char patt[]);
template bool ACMachine::addOutput<std::string>(const std::string & patt);

void ACMachine::addFailures() {
	std::deque<state> q;

	// for states whose distance from the initial state is one.
	//	std::cout << "states within distance one: ";
	for (auto const & assoc : transitions[initial_state]) {
		//const alphabet c = assoc.first;
		const state nxstate = assoc.second;
		// if is neither an explicit failure, nor go-root-failure
		failure[nxstate] = initial_state;
		inv_failure[initial_state].insert(nxstate);
		q.push_back(nxstate);
		//		std::cout << nxstate << ", ";
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
				inv_failure[initial_state].insert(nxstate);
			}
			else {
				failure[nxstate] = itp->second;
				inv_failure[itp->second].insert(nxstate);
				output[nxstate].insert(output[failure[nxstate]].begin(), output[failure[nxstate]].end());
			}
			//			std::cout << std::endl << "set "<< nxstate << " ~~> " <<  failure[nxstate];
			//			std::cout << std::endl;
		}
	}
}

template<>
int ACMachine::searchstateposition<char>(const char & patt) {
	const std::string p{ patt };
	return searchstateposition(p);
}

template <typename T>
int ACMachine::searchstateposition(const T patt[]){
  const std::string p(patt);
  return searchstateposition(p);
}

template <typename T>
int ACMachine::searchstateposition(const T & patt){
  int position;

  resetState();
  
  for(position = 0; position < patt.size() ; position++){
    if(!transfer(patt[position]))
      break;
  }

  resetState();

  return position;
}

template int ACMachine::searchstateposition<char>(const char patt[]);
template int ACMachine::searchstateposition<std::string>(const std::string & patt);

template <typename T>
void ACMachine::addFailure(const int position, const T patt[]) {
  const std::string p(patt);
  return addFailure(position, p);
}

template <>
void ACMachine::addFailure<char>(const int position, const char & patt) {
	const std::string p{ patt };
	//std::cout << "char " << p << std::endl;
	return addFailure(position, p);
}


template <typename T>
void ACMachine::addFailure(const int position, const T & patt) {

  //std::cout << "addFailure check" << std::endl;
  //std::cout << "position " << position << std::endl;

  state s;

  std::map<alphabet, state>::iterator itp;

  resetState();
  for(int p = 0; p < position; p++){
    transfer(patt[p]);
  }
  //std::cout << "check a" << std::endl;

  state cstate = currentState();

  state nxstate, fstate;
  for(int p = position; p < patt.size(); p++){
	//std::cout << "check a" << std::endl;
    itp = transitions[cstate].find(patt[p]);
    nxstate = itp->second;
    fstate = failure[cstate];
    
    if(cstate == initial_state){
      failure[nxstate] = initial_state;
      inv_failure[initial_state].insert(nxstate);
    }
    else{
      while (1) {
		itp = transitions[fstate].find(patt[p]);
		if (itp == transitions[fstate].end() && fstate != initial_state) {
			fstate = failure[fstate];
		}
		else {
			break;
		}
      }
      if (itp == transitions[fstate].end()) {
		failure[nxstate] = initial_state;
		inv_failure[initial_state].insert(nxstate);
      }
      else {
		failure[nxstate] = itp->second;
		inv_failure[itp->second].insert(nxstate);
		output[nxstate].insert(output[failure[nxstate]].begin(), output[failure[nxstate]].end());
      }
    }
    cstate = nxstate;
	//std::cout << "check b" << std::endl;
  
  } 

    

	
}

template void ACMachine::addFailure<char>(int i, const char patt[]);
template void ACMachine::addFailure<std::string>(int i, const std::string & patt);

template <typename T>
void ACMachine::renewfunction(int position, const T patt[]) {
  const std::string p(patt);
  return renewfunction(position, p);
}

template <typename T>
void ACMachine::renewfunction(int position, const T & patt) {
  
  resetState();
  for(int p = 0; p < position; p++){
    transfer(patt[p]);
  }

  state s = currentState();

  std::deque<state> st_que;
  std::deque<int> pos_que;

  std::map<alphabet, state>::iterator itp;
  std::vector<state>::iterator itp_fail;
  /*
  for(int i = 1; i < (int)failure.size(); i++)
    if(failure[i] == s){
      st_que.push_back(i);
      pos_que.push_back(position);
    }
  */
  for(auto inf : inv_failure[s]){
    st_que.push_back(inf);
    pos_que.push_back(position);
  }
  
  state cstate;

  state nxstate;
  state fstate;
  state fnxstate;
  int pos;
  int count = 1;
  while(!st_que.empty()){

    fstate = st_que.front();
    st_que.pop_front();
    pos = pos_que.front();
    pos_que.pop_front();

	cstate = s;

	for (int i = position; i < pos; i++) {
		itp = transitions[cstate].find(patt[i]);
		cstate = itp->second;
	}
	itp = transitions[cstate].find(patt[pos]);
	nxstate = itp->second;

    itp = transitions[fstate].find(patt[pos]);
    while(itp != transitions[fstate].end()){
      fnxstate = itp->second;
      //itp_fail = std::find(inv_failure[failure[fnxstate]].begin(), inv_failure[failure[fnxstate]].end(), fnxstate);
      //inv_failure[failure[fnxstate]].erase(itp_fail);
      inv_failure[failure[fnxstate]].erase(fnxstate);
      failure[fnxstate] = nxstate;
      inv_failure[nxstate].insert(fnxstate);

      pos++;
      cstate = nxstate;
      itp = transitions[nxstate].find(patt[pos]);
      nxstate = itp->second;
      fstate = fnxstate;
      itp = transitions[fstate].find(patt[pos]);
    }

    if(pos == patt.size())
      output[fstate].insert(patt.length());
    
    /*
    for(int i = 1; i < (int)failure.size(); i++)
      if(fstate == failure[i]){
		st_que.push_back(i);
		pos_que.push_back(pos);
      }
    */
    for(auto inf : inv_failure[fstate]){
      st_que.push_back(inf);
      pos_que.push_back(pos);
    }
    
  }
  
}


template void ACMachine::renewfunction<char>(int position, const char patt[]);
template void ACMachine::renewfunction<std::string>(int position, const std::string & patt);


template <typename T>
void ACMachine::addfailurestates(ACMachine::failurestates & fst, const T patt[]){
  const std::string s(patt);
  return addfailurestates(fst, s);
}

template <>
void ACMachine::addfailurestates<char>(ACMachine::failurestates & fst, const char & patt) {
	const std::string s{ patt };
	return addfailurestates(fst, s);
}

	
template <typename T>
void ACMachine::addfailurestates(ACMachine::failurestates & fst, const T & patt){
  //sleep(3);
  std::vector<state> tmp;
  resetState();
  //std::vector<state>::iterator itp_fail;
  tmp.push_back(current);
  if (!fst.empty()){
    for (int i = 0; i < patt.length(); i++){
      transfer(patt[i]);
      tmp.push_back(current);
    }
    for (auto st : fst) {
      //sleep(3);
      //itp_fail = std::find(inv_failure[failure[st.first]].begin(), inv_failure[failure[st.first]].end(), failure[st.first]);
      //inv_failure[failure[st.first]].erase(itp_fail);
      inv_failure[failure[st.first]].erase(st.first);
      //std::cout << "failure[st.first] " << failure[st.first] << std::endl;
      //sleep(3);
      failure[st.first] = tmp[st.second];
      inv_failure[tmp[st.second]].insert(st.first);
    }
  }
		
}

template void ACMachine::addfailurestates<char>(ACMachine::failurestates & fst, const char patt[]);
template void ACMachine::addfailurestates<std::string>(ACMachine::failurestates & fst, const std::string & patt);

template <typename T>
void ACMachine::addoutstates(ACMachine::outstates & ost, const T patt[]){
  const std::string p(patt);
  return addoutstates(ost, p);
}

template <>
void ACMachine::addoutstates<char>(ACMachine::outstates & ost, const char & patt) {
	const std::string p{ patt };
	return addoutstates(ost, p);
}

template <typename T>
void ACMachine::addoutstates(ACMachine::outstates & ost, const T & patt){
  if (!ost.empty()){
    for (auto st : ost){
      output[st].insert(patt.size());
    }
  }
}

template void ACMachine::addoutstates<char>(ACMachine::outstates & ost, const char patt[]);
template void ACMachine::addoutstates<std::string>(ACMachine::outstates & ost, const std::string & patt);

std::vector<std::pair<position, const std::string> >
ACMachine::search(const std::string & text) {
	std::vector<std::pair<position, const std::string> > occurrs;
	std::deque<alphabet> uring;

	uint32 pos = 0;
	resetState();
	uring.clear();
	while (pos < text.size()) {
		if (transfer(text[pos])) {
			uring.push_back(text[pos]);
			if (!output[current].empty()) {
				for (std::set<position>::iterator it = output[current].begin();
					it != output[current].end(); it++) {
					const position patlen = *it;
					std::string patt(patlen, ' ');
					for (position i = 0; i < patlen; i++) {
						patt[i] = uring.at(uring.size() - patlen + i);
					}
					occurrs.push_back(std::pair<position, const std::string>(pos + *it + 1, patt));
				}
			}
			pos++;
		}
		else {
			// failure loop
			current = failure[current];
			if (current == initialState()) {
				pos++;
				//uring.push_back(text[pos]);
				uring.clear();
			}
			else {
				uring.pop_front();
			}
		}
	}
	return occurrs;
}

bool ACMachine::read(const alphabet & c, const bool ignore_case) {
	do {
		if (transfer(c, ignore_case))
			return true;
		current = failure[current];
		std::cout << "failure" << std::endl;
		std::cout << "current state " << current  << std::endl;
	} while (current != initialState());
	return false;
}



std::ostream & ACMachine::printStateOn(std::ostream & out, state i, const std::string & pathstr) const {
	if (i == current) {
		out << "<" << i << ">";
	}
	else {
		out << i;
	}
	if (output[i].size() > 0) {
		out << "{";
		for (std::set<position>::iterator it = output[i].begin();
			it != output[i].end(); ) {
			out << pathstr.substr(pathstr.length() - *it, *it);
			if (++it != output[i].end())
				out << ", ";
		}
		out << "}";
	}
	out << "[";
	for (std::map<alphabet, state>::const_iterator it = transitions[i].begin();
		it != transitions[i].end(); it++) {
		out << "'" << (char)it->first << "'-> " << it->second << ", ";
	}
	out << "~> " << failure[i];
	out << "], ";

	return out;
}



std::ostream & ACMachine::printOn(std::ostream & out) const {
	std::deque<std::map<alphabet, state>::const_iterator> path;
	state curr;
	std::string str;

	std::map<alphabet, state> dummy;
	dummy[0] = initialState(); // dummy arc to the initial state.

	out << "ACMachine(";
	path.push_back(dummy.begin());
	curr = initialState();
	str = "";
	printStateOn(out, curr, str);

	std::map<alphabet, state>::const_iterator itr;
	itr = transitions[curr].begin();
	if (itr != transitions[curr].end()) {
		path.push_back(itr);
		curr = itr->second;
	}

	while (!path.empty()) {
		if (curr == path.back()->second) {
			// I'm on top.
			// print curr, then go to the first child if exist
			str.resize(path.size());
			for (position i = 0; i < path.size(); i++) {
				str[i] = path[i]->first;
			}
			printStateOn(out, curr, str);
			itr = transitions[curr].begin(); // the first transition arc
		}
		else {
			// returned from the child that still on path top.
			// find next to path.back()
			itr = path.back();
			path.pop_back(); // remove last edge
			++itr; // the next transition arc
		}
		if (itr != transitions[curr].end()) {
			path.push_back(itr); // replace with new edge
			curr = itr->second;
			continue;
		}
		else {
			itr = path.back();
			path.pop_back();
			if (path.empty()) // popped the dummy path to the initial state.
				continue;
			curr = path.back()->second;
			path.push_back(itr);
			continue;
		}
	}

	out << ") ";
	return out;
}


