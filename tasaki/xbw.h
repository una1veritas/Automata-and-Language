//=======================================
// xbw.h
//=======================================


#ifndef xbw_H_
#define xbw_H_

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
#include <tuple>
#include <bitset>
#include <algorithm>
#include <assert.h>
#include <chrono>
#include <list>


#include <sdsl/bit_vectors.hpp>
#include <sdsl/rank_support.hpp>
#include <sdsl/select_support.hpp>
#include <sdsl/wavelet_trees.hpp>
#include <sdsl/bp_support.hpp>


using namespace sdsl;

#ifndef TYPEDEF
#define TYPEDEF
typedef int32_t int32;
typedef uint32_t uint32;
typedef uint16_t uint16;
typedef uint8_t uint8;
typedef uint8 position;
#endif


class Xbw {
public:
	typedef uint32 state;
	typedef uint8 alphabet;

private:
	std::vector<std::map<alphabet, state>> transitions;
	std::vector<state> failure;
	std::vector<std::list<position> > output;

	struct xbw_element{
		alphabet e_alpha;
		bool e_last;
		bool e_leaf;
		std::string e_string;
		state e_failure;
		std::list<position> e_output;
		state e_idx;
	}; 
	
	unsigned char *vlc_failure;
	state failure_size;
	state vlc_failure_size;

	bit_vector xbw_last;
	bit_vector xbw_leaf;
	bit_vector b_xbw_failure;
	//rrr_vector<> rrr_leaf;

	alphabet *xbw_alphabet;
	state *xbw_failure;
	std::list<position> *xbw_output;

	bit_vector array_A;
	sd_vector<> sd_array_A;

	int alpha_num[256];

	
	rank_support_v<1> rank_last_support;
	rank_support_v5<1> v5_rank_last_support;

	select_support_mcl<1,1> mcl_select_last_support;
	select_support_mcl<1,1> mcl_select_arrayA_support;
	
	//wt_ap<> wt_alphabet;
	wt_huff<> wt_alphabet;
	//wt_hutu<> wt_alphabet;
	//wt_blcd<> wt_alphabet;
	//wt_int<> wt_alphabet;

	sd_vector<>::select_1_type sdb_select_arrayA_support;
	rrr_vector<>::select_1_type rrrb_select_last_support;
	rrr_vector<>::rank_1_type rrrb_rank_last_support;

	rrr_vector<>::select_1_type rrrb_select_failure_support;
	select_support_mcl<1,1> mcl_select_failure_support;

	sd_vector<> sdb_last;
	rrr_vector<> rrrb_last;
	rrr_vector<> rrrb_failure;

	state current;

	// class constants
	const static state initial_state = 0;

private:

	void setupInitialState(void);
	void setupInitialState_failure(void);

	bool transfer(const alphabet & c, const bool ignore_case = false);
	//bool transfer(const alphabet & c, const bool ignore_case = true);
	//	state transition(const state s, const alphabet c);

	state initialState() const { return initial_state; }

public:
	Xbw(void);


	uint32 size() const { return transitions.size(); }


	state resetState() { return current = initial_state; }
	state currentState() const { return current; }

	bool atInitialState() const { return current == initial_state; }
	std::list<position> currentOutput(){ return xbw_output[current]; }

	// add patt to the trie and output of the destination state.
	template <typename T>
	state addPath(const T & patt, const uint32 & length);
	template <typename T>
	state addPath(const T patt[]);
	template <typename T>
	state addPath(const T & patt);
	template <typename T>
	state addPath_failure(const T & patt, const uint32 & length);
	template <typename T>
	state addPath_failure(const T patt[]);
	template <typename T>
	state addPath_failure(const T & patt);
	template <typename T>
	bool addOutput(const T & patt);
	template <typename T>
	bool addOutput(const T patt[]);
	void addFailures();

	void merge_idx(std::vector<std::pair<state, state>> &xbw_element_array, int left, int mid, int right);
	void merge_sort_sub_idx(std::vector<std::pair<state, state>> &xbw_element_array, int left, int right);
	void merge_sort_idx(std::vector<std::pair<state, state>> &xbw_element_array, state ac_to_xbw_size);
	void merge(std::vector<xbw_element> &xbw_element_array, int left, int mid, int right);
	void merge_sort_sub(std::vector<xbw_element> &xbw_element_array, int left, int right);
	void merge_sort(std::vector<xbw_element> &xbw_element_array, state array_size);
	

	void make_xbw(const state node_size);
	void make_rank_select(const state node_size, bool memory_or_speed);
	

	template <typename C>
	void addPatterns(const C & strset) {
		for (auto str : strset) {
			resetState();
			addPath(str);
			addOutput(str);
		}

		addFailures();

	}

	
	void make_vlc_failure(state node_size);
	
	bool xbw_transfer(alphabet alpha, bool memory_or_speed);
	state find_vlc_failure_select(state c);


	template <typename C>
	void buildingxbw(const C & strset, bool show_memory, int words_size, bool memory_or_speed) {

		int node_size = 0;

		addPatterns(strset);
		node_size = size();
		make_xbw(node_size);
		make_rank_select(node_size, memory_or_speed);
		make_vlc_failure(node_size);
		failure_size = failure.size();

		


		//std::cin >> ch;
		
		if(show_memory){
			//use memory check============================================================================================================

			std::cout << words_size << ",";
			std::cout << node_size << ",";
			
			int xbw_alphabet_size=0, xbw_last_size=0, xbw_leaf_size=0, xbw_array_total=0;
			int last_rank_size=0, last_select_size=0, arrayA_size=0, arrayA_select_size=0, wavelet_size=0, support_total=0;
			int xbw_array_support_total=0;
			//int failure_size=0, output_size=0;

			//xbw_alphabet----------------------------------------------------------------
			xbw_alphabet_size = sizeof(alphabet) * node_size;
			std::cout << xbw_alphabet_size << ",";
			//xbw_alphabet----------------------------------------------------------------

			//xbw_last----------------------------------------------------------------
			//use bit_vector-----------------------------------------------------------
			if(memory_or_speed)
				xbw_last_size = size_in_bytes(xbw_last);
			//use rrr_vector-----------------------------------------------------------
			if(!memory_or_speed)
				xbw_last_size = size_in_bytes(rrrb_last);

			std::cout << xbw_last_size << ",";
			//xbw_last----------------------------------------------------------------
			
			//xbw_leaf----------------------------------------------------------------
			xbw_leaf_size = size_in_bytes(xbw_leaf);
			std::cout << xbw_leaf_size << ",";
			//xbw_leaf----------------------------------------------------------------

			//xbw array total(KB)----------------------------------------------------------------
			xbw_array_total = xbw_alphabet_size + xbw_last_size + xbw_leaf_size;
			std::cout << xbw_array_total/1024 << ",";
			//xbw array total(KB)----------------------------------------------------------------
			
			//last rank support--------------------------------------------------------------------------------------
			//use bit_vector-----------------------------------------------------------
			if(memory_or_speed)
				last_rank_size = size_in_bytes(v5_rank_last_support);
			//use rrr_vector-----------------------------------------------------------
			if(!memory_or_speed)
				last_rank_size = 10;

			std::cout << last_rank_size << ",";
			//last rank support--------------------------------------------------------------------------------------

			//last select support--------------------------------------------------------------------------------------
			//use bit_vector-----------------------------------------------------------
			if(memory_or_speed)
				last_select_size = size_in_bytes(mcl_select_last_support);
			//use rrr_vector-----------------------------------------------------------
			if(memory_or_speed)
				last_select_size = 8;

			std::cout << last_select_size << ",";
			//last select support--------------------------------------------------------------------------------------

			//arrayA --------------------------------------------------------------------------------------
			//use sd_vector-----------------------------------------------------------
			arrayA_size = size_in_bytes(sd_array_A);
			std::cout << arrayA_size << ",";
			//arrayA --------------------------------------------------------------------------------------

			//arrayA select support --------------------------------------------------------------------------------------
			//use sd_vector-----------------------------------------------------------
			arrayA_select_size = 8;
			std::cout << arrayA_select_size << ",";
			//arrayA select support --------------------------------------------------------------------------------------

			//wavelet --------------------------------------------------------------------------------------
			wavelet_size = size_in_bytes(wt_alphabet);
			std::cout << wavelet_size << ",";
			//wavelet --------------------------------------------------------------------------------------
			
			//support total(KB) --------------------------------------------------------------------------------------
			support_total = last_rank_size + last_select_size + arrayA_size + arrayA_select_size + wavelet_size;
			std::cout << support_total/1024 << ",";
			//support total(KB) --------------------------------------------------------------------------------------
			
			//xbw array support total(KB) --------------------------------------------------------------------------------------
			xbw_array_support_total = xbw_array_total + support_total;
			std::cout << xbw_array_support_total/1024 << ",";
			//xbw array support total(KB) --------------------------------------------------------------------------------------

			//vlc failure array --------------------------------------------------------------------------------------
			int vlc_failure_array_size = vlc_failure_size;
			std::cout << vlc_failure_array_size << ",";
			//vlc failure array --------------------------------------------------------------------------------------

			//vlc failure support --------------------------------------------------------------------------------------
			int vlc_failure_bv_size = size_in_bytes(b_xbw_failure);
			int vlc_failure_mcl_size = size_in_bytes(mcl_select_failure_support);
			int vlc_failure_support_size = vlc_failure_bv_size + vlc_failure_mcl_size;
			std::cout << vlc_failure_support_size << ",";
			//vlc failure support --------------------------------------------------------------------------------------

			//vlc failure total(KB) --------------------------------------------------------------------------------------
			int vlc_failure_total = vlc_failure_array_size + vlc_failure_support_size;
			std::cout << vlc_failure_total/1024 << ",";
			//vlc failure total(KB) --------------------------------------------------------------------------------------

			//total(KB) --------------------------------------------------------------------------------------
			std::cout << (xbw_array_support_total + vlc_failure_total)/1024 << ",";
			//total(KB) --------------------------------------------------------------------------------------

			//vlc element size --------------------------------------------------------------------------------------
			std::cout << vlc_failure_size << ",";
			//vlc element size --------------------------------------------------------------------------------------

			//failure size --------------------------------------------------------------------------------------
			std::cout << node_size * 4 << ",";
			//failure size --------------------------------------------------------------------------------------
			
			std::cout << std::endl;
			
			//use memory check============================================================================================================
		}

		transitions.clear();
		std::vector<std::map<alphabet, state>>().swap(transitions);
		failure.clear();
		std::vector<state>().swap(failure);
		delete[] xbw_failure;

		
		//std::cin >> ch;

	}


	bool read(const alphabet & c, bool memory_or_speed);


};


typedef Xbw xbw;


#endif /* ACMACHINE_H_ */
