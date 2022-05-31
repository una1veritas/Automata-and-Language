//=======================================
// ACMachine.h
//=======================================


#ifndef ACMACHINE_H_
#define ACMACHINE_H_

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <queue>
#include <cinttypes>
#include <time.h>
#include <unistd.h>
#include <sys/time.h>
#include <iomanip>
#include <list>


#ifndef TYPEDEF
#define TYPEDEF
typedef int32_t int32;
typedef uint32_t uint32;
typedef uint16_t uint16;
typedef uint8_t uint8;
typedef uint8 position;
#endif

class ACMachine {
public:
	typedef uint32 state;
	typedef uint8 alphabet;

	typedef const std::vector<alphabet> ustring;

private:
	std::vector<std::map<alphabet, state>> transitions;
	std::vector<state> failure;
	state *failure_array;
	std::vector<std::list<position>> output;

	state current;

	state failure_count = 0;

	// class constants
	const static state initial_state = 0;

private:

	void setupInitialState(void);

	bool transfer(const alphabet & c, const bool ignore_case = false);
	//bool transfer(const alphabet & c, const bool ignore_case = true);
	//	state transition(const state s, const alphabet c);

	state initialState() const { return initial_state; }

public:
	ACMachine(void);


	uint32 size() const { return transitions.size(); }


	state resetState() { return current = initial_state; }
	state currentState() const { return current; }

	bool atInitialState() const { return current == initial_state; }

	const std::list<position> currentOutput() const { return output[current]; }

	// add patt to the trie and output of the destination state.
	template <typename T>
	state addPath(const T & patt, const uint32 & length);
	//template <typename T>
	//state addPath(const T patt[]);
	template <typename T>
	state addPath(const T & patt);

	template <typename T>
	bool addOutput(const T & patt);
	template <typename T>
	bool addOutput(const T patt[]);

	void addFailures();

	template <typename C>
	  void addPatterns(const C & strset, bool show_memory, int word_size) {
		for (auto str : strset) {
			resetState();
			addPath(str);
			addOutput(str);
		}
		addFailures();

		int transitions_size, failure_size, output_size;
		int total_size, node_size;
		
		failure_array = new state[size()];
		for(int i = 0; i < size(); i++){
			failure_array[i] = failure[i];
		}
		failure.clear();
		std::vector<state>().swap(failure);

		if(show_memory){
			//===============================================================================================

		    std::cout << word_size << ",";
		    std::cout << transitions.size() << ",";
			
			node_size = sizeof(std::_Rb_tree_node<std::pair<const state, alphabet>>);
			transitions_size = node_size * transitions.size() + 48 * transitions.size();
			std::cout << transitions_size/1024 << ",";

			//state *temp_sp;
			failure_size = sizeof(state) * size();
			std::cout << failure_size/1024 << ",";


			output_size = 0;
			
			std::list<position> list_t = std::list<position>();
			output_size = (sizeof(position) + sizeof(list_t)) * output.size();
			//std::cout << output_size << ",";

			std::cout << (transitions_size + failure_size)/1024 << std::endl;

			std::cout << std::endl;
			
			//===============================================================================================
		}
		

	}


	bool read(const alphabet & c, const bool ignore_case = false);


};


typedef ACMachine acm;


#endif /* ACMACHINE_H_ */
