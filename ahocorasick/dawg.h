//====================================
// dawg.h
//====================================

#ifndef DAWG_H_
#define DAWG_H_

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <cinttypes>


#ifndef TYPEDEF
#define TYPEDEF
typedef int32_t int32;
typedef uint32_t uint32;
typedef uint16_t uint16;
typedef size_t position;
#endif

class DAWG {
public:
	typedef uint32 state;
	typedef uint16 alphabet;

	typedef const std::vector<alphabet> ustring;
	typedef bool label;
	typedef std::pair<state, label> state_edgelabel;
	typedef std::pair<state, state> fstates;
	
private:
	std::vector<std::map<alphabet, state_edgelabel>> transitions;
	std::vector<state> spointer;
	std::vector<std::set<state>> inv_sp;
	//trunk: true / branch: false
	std::vector<bool> torb;
	std::vector<int> datoac;

	state currentsink;

	state acmstatenum = initialState();

	// class constants
	const static state initial_state = 0;

private:

	void setupInitialState(void);

	int transfer(const state current, const alphabet & c, const int pors = -1, const bool ignore_case = false);
	//	state transition(const state s, const alphabet c);									   

	state initialState() const { return initial_state; }

public:
	DAWG(void);


	uint32 size() const { return transitions.size(); }


	state resetState() { return currentsink = initial_state; }
	state currentState() const { return currentsink; }

	bool atInitialState() const { return currentsink == initial_state; }


	state update(state sink, char c);
	state split(state parentstate, state childstate, char c);

	/*
	template <typename T>
	void builddawg(const T str[]){
	  const std::string s(str);
	  return builddawg(s);
	}

	template <typename T>
	void builddawg(const T & str){
	  state sink;
	  sink = initialState();
	  for(int i =0; i < str.size(); i++) {
	    sink = update(sink, str[i]);
	  }
	}
	*/

	
	template <typename T>
	  void builddawg(const T str[]);

	template <typename T>
	  void builddawg(const T & str);

	template <typename T>
	  void builddawg(const T & str, const int length);
		
	/*
	template <typename T>
	  void buildingdawg(const T & str);

	template <typename T>
	  void buildingdawg(const T str[]);
	  */

	
	template <typename C>
	void buildingdawg(const C & strset) {
		for (auto str : strset) {
			builddawg(str);
		}
	}
	


	template <typename T>
	  std::vector<fstates> getFailStates(int position, const T & patt);

	template <typename T>
	  std::vector<fstates> getFailStates(int position, const T patt[]);

	template <typename T>
	  std::vector<state> getOutStates(const T & patt);

	template <typename T>
	  std::vector<state> getOutStates(const T patt[]);

	void dawgtoacm(bool trunk, int check = -1){
		if (check == -1) {
			if (trunk == true){
				acmstatenum++;
				datoac.push_back(acmstatenum);
			}
			else{
				datoac.push_back(-1);
			}
		}
		else {
			if (trunk == true){
				acmstatenum++;
				datoac[check] = acmstatenum;
			}
		}
	}


};

typedef DAWG dawg;


#endif /* DAWG_H_ */
