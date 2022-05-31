//====================================
// dawg.cpp
//====================================

#include "dawg.h"

#include <deque>
#include <algorithm>
#include <cctype>


DAWG::DAWG(void) {
	setupInitialState();
	resetState();
}

void DAWG::setupInitialState(void) {
	transitions.clear();
	transitions.push_back(std::map<alphabet, state_edgelabel>());
	spointer.clear();
	spointer.push_back(initialState());
	inv_sp.clear();
	inv_sp.push_back(std::set<state>());
	inv_sp[initialState()].clear();
	torb.clear();
	torb.push_back(true);
	datoac.clear();
	datoac.push_back(initialState());
}


int DAWG::transfer(const state current, const alphabet & c, const int pors, const bool ignore_case) {
  std::map<alphabet, state_edgelabel>::iterator itr;
  state newstate;
  
  if (ignore_case) {
    itr = transitions[current].find(toupper(c));
    if (itr == transitions[current].end())
      itr = transitions[current].find(tolower(c));
  }
  else {
    itr = transitions[current].find(c);
  }
  
  if (itr == transitions[current].end()) {
    return -1;
  }

  if (pors == -1) 
	  newstate = itr->second.first;
  else {
	  if (pors != itr->second.second) {
		  return -1;
	  }
	  newstate = itr->second.first;
  }

  return newstate;
}


DAWG::state DAWG::update(state sink, char c) {
    state currentsink = sink;
    state newsink;
    state_edgelabel tmp;

    if(transfer(currentsink, c) > 0){
      //std::cout << "not make primary" << std::endl;
      if(transfer(currentsink, c, true) > 0){
		newsink = transfer(currentsink, c, true);
		torb[newsink] = true;
		if(datoac[newsink] == -1)
		  dawgtoacm(true, newsink);
		return newsink;
	  }
      else{
		newsink = transfer(currentsink, c, false);
		torb.push_back(true);
		dawgtoacm(true);
		return split(currentsink, newsink, c);
	  }
    }
    else{
      //std::cout << "make primary" << std::endl;
      newsink = transitions.size();
      tmp.first = newsink; tmp.second = true;
      transitions.push_back(std::map<alphabet, state_edgelabel>());
      transitions[currentsink].insert(std::make_pair(c, tmp));
      torb.push_back(true);
      dawgtoacm(true);

      spointer.push_back(initialState());
      inv_sp.push_back(std::set<state>());

      state currentstate = currentsink;
      int sfstate = -1;

      while((currentstate != initialState()) && (sfstate == -1)){
		currentstate = spointer[currentstate];
		//std::cout << "current state: " << currentstate << std::endl;
		if((transfer(currentstate, c, true) == -1) && (transfer(currentstate, c, false) == -1)){
			//std::cout << "while: not edge" << std::endl;
			tmp.first = newsink; tmp.second = false;
			transitions[currentstate].insert(std::make_pair(c, tmp));
			//std::cout << "check" << std::endl;
		}
		else if(transfer(currentstate, c, true) > 0){
		  //std::cout << "while: primary" << std::endl;
		  sfstate = transfer(currentstate, c, true);
		}
		else if(transfer(currentstate, c, false) > 0){
		  //std::cout << "while: secondary" << std::endl;
		  state child = transfer(currentstate, c, false);
		  torb.push_back(false);
		  dawgtoacm(false);
		  sfstate = split(currentstate, child, c);
		  //std::cout << "while: secondary sfstate: " << sfstate << std::endl;
		}
      }

      if(sfstate == -1)
		sfstate = initialState();

      spointer[newsink] = sfstate;
	  inv_sp[sfstate].insert(newsink);
      return newsink;
    }
}

DAWG::state DAWG::split(state parentstate, state childstate, char c) {
  
  state newchildstate;
  std::map<alphabet, state_edgelabel>::iterator itr;
  std::vector<state>::iterator itr_sp;
  newchildstate = transitions.size();
  transitions.push_back(std::map<alphabet, state_edgelabel>());
  state_edgelabel  tmp;
  tmp.first = newchildstate; tmp.second = true;
  
  itr = transitions[parentstate].find(c);
  transitions[parentstate].erase(itr);
  transitions[parentstate].insert(std::make_pair(c, tmp));
  transitions[newchildstate].insert(transitions[childstate].begin(), transitions[childstate].end());
  for(auto & assoc:transitions[newchildstate]) 
    assoc.second.second = false;

  spointer.push_back(spointer[childstate]);
  inv_sp.push_back(std::set<state>());
  inv_sp[spointer[childstate]].insert((spointer.size() - 1));
  spointer[childstate] = newchildstate;
  inv_sp[newchildstate].insert(childstate);
  //itr_sp = std::find(inv_sp[spointer[childstate]].begin(), inv_sp[spointer[childstate]].end(), childstate);
  //inv_sp[spointer[childstate]].erase(itr_sp);
  inv_sp[spointer[newchildstate]].erase(childstate);


  state currentstate;
  currentstate = parentstate;
  tmp.first = newchildstate; tmp.second = false;

  while(currentstate != initialState()){
    currentstate = spointer[currentstate];
    itr = transitions[currentstate].find(c);
    if(itr->second.second == false){
      transitions[currentstate].erase(itr);
      transitions[currentstate].insert(std::make_pair(c, tmp));
      
    }
    else{
      break;
    }
    
  }

  return newchildstate;
  
}


template <typename T>
void DAWG::builddawg(const T str[]){
  const std::string s(str);
  int len;
  for(len = 0; str[len] != 0; len++){}
  builddawg(str, len);
}
	

template <typename T>
void DAWG::builddawg(const T & str){
  builddawg(str, str.length());
}

template <>
void DAWG::builddawg<char>(const char & str){
  std::string s{ str };
  builddawg(s, 1);
}


template <typename T>
void DAWG::builddawg(const T & str, const int length){
  state sink;
  sink = initialState();
  for(int i =0; i < length; i++) {
    sink = update(sink, str[i]);
  }
}


template <>
void DAWG::builddawg<char>(const char & str, const int length){
  state sink;
  sink = initialState();
  sink = update(sink, str);
}


template void DAWG::builddawg<char>(const char str[]);
template void DAWG::builddawg<std::string>(const std::string & str);
template void DAWG::builddawg<char>(const char & str);

/*
template <typename T>
void DAWG::buildingdawg(const T strset[]){
  const std::string s(strset);
  buildingdawg(s);
}

template <typename T>
void DAWG::buildingdawg(const T & strset){
  for (auto str : strset) {
    builddawg(str);
  }
}

template void DAWG::buildingdawg<std::string>(const std::string & strset);
template void DAWG::buildingdawg<char>(const char strset[]);
*/

template <typename T>
std::vector<DAWG::fstates> DAWG::getFailStates(int position, const T patt[]) {
  const std::string p(patt);
  return getFailStates(position, p);
}

template <>
std::vector<DAWG::fstates> DAWG::getFailStates<char>(int position, const char & patt) {
	const std::string p{ patt };
	return getFailStates(position, p);
}

//std::vector<DAWG::fstates> DAWG::getFailStates(int position, std::string patt) {
template <typename T>
std::vector<DAWG::fstates> DAWG::getFailStates(int position, const T & patt) {
  std::vector<fstates> failstates;
  state activestate = initialState();
  //state cstate;
  state currentstate;
  state pos;
  state state_tmp;
  fstates f_tmp;
  int pattsize = patt.length();
  std::deque<state> st;
  std::deque<int> st_pos;

  for (int i = 0; i <= pattsize; i++) {
    if (i > position) {
      st.push_front(activestate);
      st_pos.push_front(i);
    }


    if ((transfer(activestate, patt[i]) == -1))
      break;

    state_tmp = transfer(activestate, patt[i]);
    
    activestate = state_tmp;
  }

  std::deque<state> queue;
  std::deque<int> queue_pos;
  std::vector<state> mark;


  while (!st.empty()) {
    state_tmp = st.front();
    pos = st_pos.front();
    st.pop_front();
    st_pos.pop_front();
    queue.push_back(state_tmp);

    while (!queue.empty()) {
      currentstate = queue.front();
      queue.pop_front();

	  auto itr = std::find(mark.begin(), mark.end(), currentstate);
	  if (itr == mark.end()) {
		mark.push_back(currentstate);
		if ((torb[currentstate] == true)) {
			f_tmp.first = datoac[currentstate];
			f_tmp.second = pos;
			failstates.push_back(f_tmp);
	    }
	    else {
	      /*
			for (state s = 0; s < spointer.size(); s++) {
				if(spointer[s] == currentstate)
					queue.push_back(s);
			}
	      */
	      for(auto inf : inv_sp[currentstate]){
		queue.push_back(inf);
	      }
	    }
	  }

    }

  }
  return failstates;
}


template <typename T>
std::vector<DAWG::state> DAWG::getOutStates(const T patt[]) {
  const std::string p(patt);
  return getOutStates(p);
}

template <>
std::vector<DAWG::state> DAWG::getOutStates<char>(const char & patt) {
	const std::string p{ patt };
	return getOutStates(p);
}


//std::vector<DAWG::state> DAWG::getOutStates(std::string patt) {
template <typename T>
std::vector<DAWG::state> DAWG::getOutStates(const T & patt) {
  std::vector<state> outstates;
  state activestate = initialState();
  state cstate;
  state currentstate;
  //state tonum;
  int pos;
  int pattsize = patt.length();
  std::deque<state> st;

  for (int i = 0; i < pattsize; i++) {
    
    pos = transfer(activestate, patt[i]);

    if (pos == -1)
      break;
    
    activestate = pos;
  }


  if (pos == -1)
	  return outstates;
  
  std::deque<state> queue;
  queue.push_back(activestate);

  while (!queue.empty()) {

    cstate = queue.front();
    queue.pop_front();
    if(torb[cstate] == true)
      outstates.push_back(datoac[cstate]);
    
    /*
    for (state s = 0; s < spointer.size(); s++) {
      if(spointer[s] == cstate)
		queue.push_back(s);
    }
    */
    for(auto inf : inv_sp[cstate]){
      queue.push_back(inf);
    }

  }
  return outstates;
}


