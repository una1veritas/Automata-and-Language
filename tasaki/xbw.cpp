//=======================================
// xbw.cpp
//=======================================

#include "xbw.h"
#include <deque>
#include <algorithm>
#include <cctype>
#include <unistd.h>



Xbw::Xbw(void) {
	setupInitialState();
	resetState();
}

void Xbw::setupInitialState(void) {
	transitions.clear();
	transitions.push_back(std::map<alphabet, state>());
	failure.clear();
	failure.push_back(initialState());
	// failure to initial state from initial state eats up one symbol at transition.
	output.clear();
	output.push_back(std::list<position>());
}


bool Xbw::transfer(const alphabet & c, const bool ignore_case) {
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
Xbw::state Xbw::addPath(const T patt[]) {
	uint32 len;
	for (len = 0; patt[len] != 0; len++) {}
	return addPath(patt, len);
}

template <typename T>
Xbw::state Xbw::addPath(const T & patt) {
	return addPath(patt, patt.length());
}

template <typename T>
Xbw::state Xbw::addPath(const T & patt, const uint32 & length) {
	uint8 pos;
	state newstate;

	for (pos = 0; pos < length; ++pos) {
	  if (!transfer((unsigned char)patt[pos])) {
			newstate = transitions.size(); //the next state of the existing last state
			transitions.push_back(std::map<alphabet, state>());
			(transitions[current])[(unsigned char)patt[pos]] = newstate;
			failure.push_back(initialState());
			output.push_back(std::list<position>());
			current = newstate;
		}
	}
	return current;
}

template Xbw::state Xbw::addPath<char>(const char patt[]);
template Xbw::state Xbw::addPath<Xbw::alphabet>(const Xbw::alphabet patt[]);
template Xbw::state Xbw::addPath<std::string>(const std::string & patt);

template <typename T>
bool Xbw::addOutput(const T & patt) {
	position tmp = patt.length();
	output[current].push_back(tmp);
	return true;
}

template <typename T>
bool Xbw::addOutput(const T patt[]) {
	const std::string p(patt);
	return addOutput(p);
}

template bool Xbw::addOutput<char>(const char patt[]);
template bool Xbw::addOutput<std::string>(const std::string & patt);


void Xbw::addFailures() {
	std::deque<state> q;

	// for states whose distance from the initial state is one.
	//	std::cout << "states within distance one: ";
	for (auto const & assoc : transitions[initial_state]) {
		//const alphabet c = assoc.first;
		const state nxstate = assoc.second;
		// if is neither an explicit failure, nor go-root-failure
		failure[nxstate] = initial_state;
		q.push_back(nxstate);
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
				//if (!output[nxstate].empty())
				//addcount++;
			}
			//			std::cout << std::endl << "set "<< nxstate << " ~~> " <<  failure[nxstate];
			//			std::cout << std::endl;
		}
	}
	//std::cout << "addfailures addcount " << addcount << std::endl;
}


void Xbw::make_xbw(const state node_size) {
		//tmp
		std::string string_tmp; 
		state state_tmp;
		alphabet label_tmp;
		bool last_tmp;

		std::vector<xbw_element> xbw_element_array;
		xbw_element xbw_element_tmp;


		//queue
		std::deque<state> queue_statenum;         //state number
		std::deque<alphabet> queue_label;         //edge label
		std::deque<std::string> queue_pai;        //pai
		std::deque<bool> queue_last;              //last

		//last, leaf check 
		bool last_flag = true;
		bool leaf_flag = false;

		//root node-----------------------------------------------------------------------------------------------
		//std::cout << "root node check start" << std::endl; 
		string_tmp = " ";
		std::map<alphabet, state>::reverse_iterator x = transitions[initial_state].rbegin();
		for( ; x != transitions[initial_state].rend(); ++x) {
			label_tmp = x->first;
			state_tmp = x->second;
	
			queue_statenum.push_front(state_tmp);
			queue_label.push_front(label_tmp);
			queue_pai.push_front(string_tmp);

			//1st --> true  2nd,3rd,... --> false
			if(last_flag == true){
				queue_last.push_front(true);
				last_flag = false;
			}
			else{
				queue_last.push_front(false);
			}
		}

		xbw_element_tmp.e_alpha = ' ';
		xbw_element_tmp.e_last = true;
		xbw_element_tmp.e_leaf = false;
		xbw_element_tmp.e_string = "";
		xbw_element_tmp.e_failure = failure[initial_state];
		xbw_element_tmp.e_output = output[initial_state];
		xbw_element_tmp.e_idx = initial_state;
		xbw_element_array.push_back(xbw_element_tmp);
		//std::cout << "root node check end" << std::endl; 
		//root node-----------------------------------------------------------------------------------------------

		//trace node preorder-------------------------------------------------------------------------------------
		//std::cout << "other node check" << std::endl;
		while(!queue_statenum.empty()){
			state_tmp = queue_statenum.front();
			queue_statenum.pop_front();
			label_tmp = queue_label.front();
			queue_label.pop_front();
			string_tmp = queue_pai.front();
			queue_pai.pop_front();
			last_tmp = queue_last.front();
			queue_last.pop_front();

			if(last_tmp == true)
				xbw_element_tmp.e_last = true;
			else
				xbw_element_tmp.e_last = false;
			xbw_element_tmp.e_alpha = label_tmp;
			xbw_element_tmp.e_string = string_tmp;
			xbw_element_tmp.e_failure = failure[state_tmp];
			xbw_element_tmp.e_output = output[state_tmp];
			xbw_element_tmp.e_idx = state_tmp;

			std::string next_string_tmp;
			char c_label_tmp;
			alphabet next_label_tmp;

			c_label_tmp = label_tmp;
			std::string label_string{c_label_tmp};
			next_string_tmp = label_string + string_tmp;

			current = state_tmp;
			
			//no child
			if(transitions[current].empty() == true) {
				xbw_element_tmp.e_leaf = true;
				xbw_element_array.push_back(xbw_element_tmp);
			}
			else{
				xbw_element_tmp.e_leaf = false;
				xbw_element_array.push_back(xbw_element_tmp);

				last_flag = true;
				std::map<alphabet, state>::reverse_iterator x = transitions[current].rbegin();
				for( ; x != transitions[current].rend(); ++x) {
					next_label_tmp = x->first;
					state_tmp = x->second;
					
					queue_statenum.push_front(state_tmp);
					queue_label.push_front(next_label_tmp);
					queue_pai.push_front(next_string_tmp);

					if(last_flag == true){
						queue_last.push_front(true);
						last_flag = false;
					}
					else{
						queue_last.push_front(false);
					}

				}
			}

		}
		//std::cout << "other node check end" << std::endl;
		//trace node preorder-------------------------------------------------------------------------------------

		merge_sort(xbw_element_array, size());

		xbw_alphabet = new alphabet[transitions.size()];
		xbw_last = bit_vector(node_size, 0);
		xbw_leaf = bit_vector(node_size, 0);
		xbw_failure = new state[node_size];
		xbw_output = new std::list<position>[node_size];

		std::vector<std::pair<state, state>> ac_to_xbw;
		std::pair<state, state> pr_tmp;

		for(int i = 0; i < size(); i++){
			xbw_alphabet[i] = xbw_element_array[i].e_alpha;
			if(xbw_element_array[i].e_last == true)
				xbw_last[i] = 1;
			else	
				xbw_last[i] = 0;
			if(xbw_element_array[i].e_leaf == true)
				xbw_leaf[i] = 1;
			else	
				xbw_leaf[i] = 0;
			xbw_failure[i] = xbw_element_array[i].e_failure;
			xbw_output[i] = xbw_element_array[i].e_output;
			pr_tmp.first = xbw_element_array[i].e_idx;
			pr_tmp.second = i;
			ac_to_xbw.push_back(pr_tmp);
		}
		merge_sort_idx(ac_to_xbw, size());
		for(int i = 0; i < size(); i++){
			xbw_failure[i] = ac_to_xbw[xbw_failure[i]].second;
		}
		
		xbw_element_array.clear();
		std::vector<xbw_element>().swap(xbw_element_array);
		ac_to_xbw.clear();
		std::vector<std::pair<state, state>>().swap(ac_to_xbw);
		queue_statenum.clear();
		queue_label.clear();
		queue_pai.clear();
		queue_last.clear();
		std::deque<state>().swap(queue_statenum);
		std::deque<alphabet>().swap(queue_label);
		std::deque<std::string>().swap(queue_pai);
		std::deque<bool>().swap(queue_last);
		

		
	}


void Xbw::make_rank_select(const state node_size, bool memory_or_speed) {

		// build F[i] start-----------------------------------------------
		int array_c[256], array_c_leaf[256], alpha_num_leaf[256];
		int using_alphabet_num = 0;
		int using_alphabet_num_leaf = 0;
		std::vector<int> using_alphabet, using_alphabet_leaf;
		int tmp;
		for(int i = 0; i < 256; i++){
			array_c[i] = 0; array_c_leaf[i] = 0;
		}
		for(int i = 0; i < node_size; i++){
			tmp = xbw_alphabet[i];
			array_c_leaf[tmp]++;
			if(xbw_leaf[i] == false){
				array_c[tmp]++;
			}
		}
		for(int i = 0;i < 256; i++){
			if(array_c[i] > 0){
				using_alphabet.push_back(i);
				alpha_num[i] = using_alphabet_num;
				using_alphabet_num++;
			}
			if(array_c_leaf[i] > 0){
				using_alphabet_leaf.push_back(i);
				alpha_num_leaf[i] = using_alphabet_num_leaf;
				using_alphabet_num_leaf++;
			}
		}

		int array_f[using_alphabet_num];
		array_f[0] = 1;
		for(int i = 0; i < using_alphabet_num; i++){
			int s = 0;
			int j = array_f[i];
			while(s != array_c[using_alphabet[i]]){
				//if(std::get<0>(xbw[j++]) == 1)
			    if(xbw_last[j++] == 1)
					s++;
			}
			array_f[i+1] = j;
		}

		// build F[i] end-------------------------------------------------


		// F[i] -> arrayA------------------
		tmp = 0;
		array_A = bit_vector(node_size, 0);
		for(int i = 0; i < node_size; i++){
			if(i == array_f[tmp]){
				array_A[i] = 1;
				tmp++;
			}
			else{
				array_A[i] = 0;
			}
		}
		// F[i] -> arrayA------------------
		
		
		//last rank=================================================================

		//use bit_vector v5-----------------------------------------------
		if(memory_or_speed){
			rank_support_v5<1> v5_rank_last_support_tmp(&xbw_last);
			v5_rank_last_support = v5_rank_last_support_tmp;
		}
		//use bit_vector v5-----------------------------------------------

		//use rrrb_vector-----------------------------------------------
		if(!memory_or_speed){
			rrrb_last = rrr_vector<>(xbw_last);
			rrr_vector<>::rank_1_type rrrb_rank_last_tmp(&rrrb_last);
			rrrb_rank_last_support = rrrb_rank_last_tmp;
			xbw_last.resize(0);
		}
		//use rrrb_vector-----------------------------------------------

		//last rank=================================================================


		//last select===============================================================

		//use bit_vector mcl-----------------------------------------------
		if(memory_or_speed){
			select_support_mcl<1,1> mcl_select_last_support_tmp(&xbw_last);
			mcl_select_last_support = mcl_select_last_support_tmp;
		}
		//use bit_vector mcl-----------------------------------------------

		//use rrrb_vector-----------------------------------------------
		if(!memory_or_speed){
			rrr_vector<>::select_1_type rrrb_select_last_tmp(&rrrb_last);
			rrrb_select_last_support = rrrb_select_last_tmp;
		}
		//use rrrb_vector-----------------------------------------------

		//last select===============================================================

		//arrayA select=============================================================

		//use sd_vector-----------------------------------------------
		sd_array_A = sd_vector<>(array_A);
		sd_vector<>::select_1_type sdb_select_arrayA_tmp(&sd_array_A);
		sdb_select_arrayA_support = sdb_select_arrayA_tmp;
		array_A.resize(0);
		//use sd_vector-----------------------------------------------

		//arrayA select=============================================================


		//alphabet wavelet==========================================================

		std::string filename = "xbw_alphabet.txt";
		std::ofstream writing_file;
		writing_file.open(filename, std::ios::out);

		char top_bit = 0b10000000;
		for(int i = 0; i < node_size; i++){
			char tmp_alphabet = xbw_alphabet[i];
			if(xbw_leaf[i] == 1){
				tmp_alphabet = top_bit | tmp_alphabet;
				writing_file << tmp_alphabet;
			}
			else{
				writing_file << tmp_alphabet;
			} 
		}
		writing_file << std::endl;
		//wt_blcd<> wt;
		construct(wt_alphabet, "xbw_alphabet.txt", 1);
		
		//alphabet wavelet==========================================================


}


void Xbw::make_vlc_failure(state node_size){

		unsigned char vlc_tmp[4];
		std::vector<unsigned char> vlc_failure_tmp;

		int vlc_data = 0;
		int byte_size_check = 0;
		//int byte_hist[4];
		//for(int i = 0; i < 4; i++)
		//	byte_hist[i] = 0;
		std::vector<int> topbit_vec;

		unsigned char top_bit = (1<<7);

		for(int i = 0; i < node_size; i++){

			vlc_data = xbw_failure[i];

			if(vlc_data <= 0xFF){
				//std::cout << "use 1bytes" << std::endl;
				vlc_tmp[0] = 0xFF & vlc_data;
				byte_size_check = 1;
				//byte_hist[0]++;
			}
			else if(vlc_data <= 0xFFFF){
				//std::cout << "use 2bytes" << std::endl;
				vlc_tmp[0] = 0xFF & (vlc_data >> 8);    
				vlc_tmp[1] = 0xFF & vlc_data; 
				byte_size_check = 2;
				//byte_hist[1]++;
			}

			else if(vlc_data <= 0xFFFFFF){
				//std::cout << "use 3bytes" << std::endl;
				vlc_tmp[0] = 0xFF & (vlc_data >> 16); 
				vlc_tmp[1] = 0xFF & (vlc_data >> 8);   
				vlc_tmp[2] = 0xFF & vlc_data;
				byte_size_check = 3;
				//byte_hist[2]++;
			}
			else if(vlc_data <= 0xFFFFFFFF){
				//std::cout << "use 4bytes" << std::endl;
				vlc_tmp[0] = 0xFF & (vlc_data >> 24);   
				vlc_tmp[1] = 0xFF & (vlc_data >> 16);    
				vlc_tmp[2] = 0xFF & (vlc_data >> 8);       
				vlc_tmp[3] = 0xFF & vlc_data; 
				byte_size_check = 4;
				//byte_hist[3]++;
			}			

			for(int j = byte_size_check-1; j >= 0; j--){
				vlc_failure_tmp.push_back(vlc_tmp[j]);
				if(j == (byte_size_check - 1))
					topbit_vec.push_back(1);
				else
					topbit_vec.push_back(0);
			}

		}

		vlc_failure_size = vlc_failure_tmp.size();
		vlc_failure = new unsigned char[vlc_failure_size];
		for(int i = 0; i < vlc_failure_size; i++){
			vlc_failure[i] = vlc_failure_tmp[i];
		}

		b_xbw_failure = bit_vector(vlc_failure_size, 0);
		for(int i = 0; i < vlc_failure_size; i++){
			if(topbit_vec[i] == 1)
				b_xbw_failure[i] = 1;
			else
				b_xbw_failure[i] = 0;
		}
		//mcl
		select_support_mcl<1,1> mcl_select_failure_support_tmp(&b_xbw_failure);
		mcl_select_failure_support = mcl_select_failure_support_tmp;

		vlc_failure_tmp.clear();
		std::vector<unsigned char>().swap(vlc_failure_tmp);
		topbit_vec.clear();
		std::vector<int>().swap(topbit_vec);

	}


bool Xbw::xbw_transfer(alphabet alpha, bool memory_or_speed){
		int ch;
		if(xbw_leaf[current] == true)
			return false;
		alphabet alphabet_tmp;
		alphabet_tmp = xbw_alphabet[current];
		
		int r, c;
		c = alpha_num[alphabet_tmp];
		r = wt_alphabet.rank(current+1, alphabet_tmp);
		int y;
		y = sdb_select_arrayA_support(c+1);
		int z;
		if(memory_or_speed)
			z = v5_rank_last_support(y);
		else
			z = rrrb_rank_last_support(y);
		int first, last;
		if(memory_or_speed){
			first = mcl_select_last_support(z+r-1)+1;
			last = mcl_select_last_support(z+r);
		}
		else{
			first = rrrb_select_last_support(z+r-1)+1;
			last = rrrb_select_last_support(z+r);
		}

		int y1=0, y2=0;
		y1 = wt_alphabet.rank(first, alpha);
		y2 = wt_alphabet.rank(last+1, alpha);
		if((y2 - y1) == 1){
			current =  wt_alphabet.select(y1+1, alpha);
			return true;
		}
		else{
			char top_bit = 0b10000000;
			alpha = alpha | top_bit;
			y1 = wt_alphabet.rank(first, alpha);
			y2 = wt_alphabet.rank(last+1, alpha);
			if((y2 - y1) == 1){
				current =  wt_alphabet.select(y1+1, alpha);
				return true;
			}
			else
				return false;
		}
	
		
	}


Xbw::state Xbw::find_vlc_failure_select(state c){
		state f_num = 0;
		int first = 0, end = 0, byte_num = 0;

		first = mcl_select_failure_support(c+1);
		if(c == (failure_size-1)){
			byte_num = vlc_failure_size - first;
		}
		else{
			end = mcl_select_failure_support(c+2);
			byte_num = end - first;
		}

		state *f_num_tmp = reinterpret_cast<state *>(&vlc_failure[first]);
		if(byte_num == 1)
			f_num = *f_num_tmp & 0xFF;
		else if(byte_num == 2)
			f_num = *f_num_tmp & 0xFFFF;
		else if(byte_num == 3)
			f_num = *f_num_tmp & 0xFFFFFF;
		else if(byte_num == 4)
			f_num = *f_num_tmp & 0xFFFFFFFF;

		return f_num;

}


void Xbw::merge_idx(std::vector<std::pair<state, state>> &ac_to_xbw, int left, int mid, int right) {
	int num = right - left;

	std::vector<std::pair<state, state>> ac_to_xbw_tmp;

		int il = left, ir = mid;

		while (il < mid && ir < right)
		{
			if (ac_to_xbw[il].first <= ac_to_xbw[ir].first) {
				ac_to_xbw_tmp.push_back(ac_to_xbw[il]);
				il++;
			} else {
				ac_to_xbw_tmp.push_back(ac_to_xbw[ir]);
				ir++;
			}
		}

		while(il < mid) {
			ac_to_xbw_tmp.push_back(ac_to_xbw[il]);
			il++;
		}
		while(ir < right) {
			ac_to_xbw_tmp.push_back(ac_to_xbw[ir]);
			ir++;
		}

		for(int i = 0; i < num; i++) {
			ac_to_xbw[left + i] = ac_to_xbw_tmp[i];
		}

	ac_to_xbw_tmp.clear();
	std::vector<std::pair<state, state>>().swap(ac_to_xbw_tmp);

}


void Xbw::merge_sort_sub_idx(std::vector<std::pair<state, state>> &ac_to_xbw, int left, int right) {
		if (right - left <= 1) return;

		int mid = left + (right - left) / 2;
		merge_sort_sub_idx(ac_to_xbw, left, mid);
		merge_sort_sub_idx(ac_to_xbw, mid, right);

		merge_idx(ac_to_xbw, left, mid, right);
}


void Xbw::merge_sort_idx(std::vector<std::pair<state, state>> &ac_to_xbw, state ac_to_xbw_size) {
		merge_sort_sub_idx(ac_to_xbw, 0, ac_to_xbw_size);
}


void Xbw::merge(std::vector<xbw_element> &xbw_element_array, int left, int mid, int right) {
	int num = right - left;
	std::vector<xbw_element> xbw_element_array_tmp; 

	int il = left, ir = mid;

	while (il < mid && ir < right)
	{
		if (xbw_element_array[il].e_string <= xbw_element_array[ir].e_string) {
			xbw_element_array_tmp.push_back(xbw_element_array[il]);
			il++;
		} else {
			xbw_element_array_tmp.push_back(xbw_element_array[ir]);
			ir++;
		}
	}

	while(il < mid) {
		xbw_element_array_tmp.push_back(xbw_element_array[il]);
		il++;
	}
	while(ir < right) {
		xbw_element_array_tmp.push_back(xbw_element_array[ir]);
		ir++;
	}

	for(int i = 0; i < num; i++) {
		//xbw_string[left + i] = xbw_string_tmp[i];
		xbw_element_array[left + i] = xbw_element_array_tmp[i];
	}

	xbw_element_array_tmp.clear();
	std::vector<xbw_element>().swap(xbw_element_array_tmp);

}


void Xbw::merge_sort_sub(std::vector<xbw_element> &xbw_element_array, int left, int right) {
	if (right - left <= 1) return;

	int mid = left + (right - left) / 2;
	merge_sort_sub(xbw_element_array, left, mid);
	merge_sort_sub(xbw_element_array, mid, right);

	merge(xbw_element_array, left, mid, right);
}


void Xbw::merge_sort(std::vector<xbw_element> &xbw_element_array, state array_size) {
	merge_sort_sub(xbw_element_array, 0, array_size);
}




bool Xbw::read(const alphabet & c, bool memory_or_speed) {
	do {
		if(xbw_transfer(c, memory_or_speed)){
			//std::cout << "transfer success" << std::endl;
			//std::cout << "current state " << xbw_to_ac[current] << std::endl;
			return true;
		}
		//std::cout << "transfer fail" << std::endl;
		//current = xbw_failure[current];
		current = find_vlc_failure_select(current);

	} while (current != initialState());
	return false;
}


