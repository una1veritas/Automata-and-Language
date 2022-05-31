//============================================================================
//admain.cpp
//============================================================================

#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <sys/time.h>

using namespace std;

#include "ACMachine.h"
#include "dawg.h"
#include "ahodawg.h"
#include "commandargs.h"

#include <time.h>
#include <iomanip>
#include <cstdlib>
#include <unistd.h>
//#include <stdlib.h>

int main(const int argc, char * const * argv) {
	ifstream ifs, addifs;
	int init_word_num = 0;
	int state_width = 10000;
	int state_max = 450000;
	bool ignore_case = false;

	commandargs optargs(argc, argv, "n:f:a:im:w:");

	pair<bool, const char*> opt;
	opt = optargs.opt('n');
	if (opt.first) {
		init_word_num = atol(opt.second);
		cout << "init_word_num = " << init_word_num << ", ";
	}
	opt = optargs.opt('f');
	if (opt.first) {
		string fname = string(opt.second);
		cout << "fname (pattern file) = " << fname << ", ";
		ifs.open(fname);
	}
	opt = optargs.opt('a');
	if (opt.first) {
		string addfname = string(opt.second);
		cout << "addfname (pattern file) = " << addfname << ", ";
		addifs.open(addfname);
	}
	opt = optargs.opt('i');
	ignore_case = opt.first;
	cout << "ignore case = " << ignore_case << ", ";
	opt = optargs.opt('m');
        if (opt.first) {
		state_max = atol(opt.second);
		cout << "state_max = " << state_max << ", ";
	}
	opt = optargs.opt('w');
        if (opt.first) {
		state_width = atol(opt.second);
		cout << "state_width = " << state_width << ", ";
	}
	cout << endl;

	ahdawg ad;

	vector<string> words;
	istringstream line;
	string tmp;
	while (!ifs.eof()) {
		std::getline(ifs, tmp);
		if (tmp.empty())
			break;
		line.str(tmp);
		line.clear();
		while (!line.eof()) {
			line >> tmp;
			if (words.size() < init_word_num)
				words.push_back(tmp);
			line >> tmp;
		}
		if (words.size() == init_word_num)
			break;
	}
	cout << "Got " << words.size() << " words: " << endl;

	ad.BuildAhoandDawg(words);

	ifs.close();
	words.clear();
	cout << "build end" << endl;
	

	//--------------------------------
	//dynamic insertion
	//--------------------------------


	vector<string> addwords;
		
	istringstream addline;
	string addtmp;
		
	int counter_max = state_max / state_width;
		
	int nextstatescount = 1;

	vector<int> statesize_vec;
	vector<int> wordnum_vec;
	vector<int> time_vec;
		

	while (!addifs.eof()) {
		std::getline(addifs, addtmp);
		if (addtmp.empty())
			break;
		addline.str(addtmp);
		addline.clear();
		while (!addline.eof()) {
			addline >> addtmp;
			addwords.push_back(addtmp);
			addline >> addtmp;
		}

	}
	cout << "Got " << addwords.size() << " add words: " << endl;

	int time = 0;
	struct timeval start, end;
	gettimeofday(&start, NULL);
	for(int i = 0; i < addwords.size(); i++){

		ad.DynamicBAD(addwords[i]);
		//cout << i << endl;

		if(ad.statesize() >= (nextstatescount * state_width)){
			gettimeofday(&end, NULL);
			time = (end.tv_sec - start.tv_sec)*1000000 + (end.tv_usec - start.tv_usec) ;
			time_vec.push_back(time);
			wordnum_vec.push_back(i);
			statesize_vec.push_back(ad.statesize());
			//cout << "nextstatescount" << nextstatescount << endl;
			cout << nextstatescount << endl;

			nextstatescount++;
		}

		if(nextstatescount > counter_max)
			break;
	}
	


	for(int i = 0; i < (nextstatescount - 1); i++){
		cout << i+1 << ",";
		cout << statesize_vec[i] << ",";
		cout << wordnum_vec[i] << ",";
		cout << time_vec[i] << ",";
		if(i == 0){
			cout << statesize_vec[i] << ",";
			cout << wordnum_vec[i] << ",";
			cout << time_vec[i] << ",";
			cout << (double)time_vec[i] / wordnum_vec[i];
		}
		if(i != 0){
			cout << statesize_vec[i] - statesize_vec[i-1] << ",";
			cout << wordnum_vec[i] - wordnum_vec[i-1] << ",";
			cout << time_vec[i] - time_vec[i-1] << ",";
			cout << (double)(time_vec[i]-time_vec[i-1])/(wordnum_vec[i]-wordnum_vec[i-1]);
		}
		cout << endl;
	}


	addifs.close();
	addwords.clear();
	
	return 0;
}
