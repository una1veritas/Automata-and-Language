//============================================================================
//main.cpp
//============================================================================

#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include <sys/time.h>
#include <deque>
#include <time.h>
#include <iomanip>
#include <cstdlib>
#include <unistd.h>

#include "xbw.h"
#include "commandargs.h"
#include "ACMachine.h"

using namespace std;

int main(const int argc, char * const * argv) {
    ifstream ifs, addifs;
    //ifstream addifs;
	int init_word_num = 0;
	bool ignore_case = false;
	bool make_xbw = false;
	bool show_memory = false;
	bool show_time = false;
	bool memory_or_speed = false; //false:memory true:speed
	int m_bytes = 1024*1024;

	string target;
	ifstream targetfile;
	istream * targetinput;

	commandargs optargs(argc, argv, "n:f:ixr:mts");

	pair<bool, const char*> opt;
	opt = optargs.opt('n');
	if (opt.first) {
		init_word_num = atol(opt.second);
	}
	opt = optargs.opt('f');
	if (opt.first) {
		string fname = string(opt.second);
		ifs.open(fname, ios::in | ios::binary );
	}
	opt = optargs.opt('i');
	if(opt.first){
	  ignore_case = opt.first;
	}
	opt = optargs.opt('x');
	if(opt.first){
	  make_xbw = opt.first;
	}
	opt = optargs.opt('r');
	if(opt.first){
	  m_bytes = 1024*1024*atol(opt.second);
	}
	opt = optargs.opt('m');
	if(opt.first){
	  show_memory = opt.first;
	}
	opt = optargs.opt('t');
	if(opt.first){
	  show_time = opt.first;
	}
	opt = optargs.opt('s');
	if(opt.first){
	  memory_or_speed = opt.first;
	}
	if (optargs.arg_count() == 0) {
		targetinput = &cin;
	}
	else {
		target = optargs.arg(0);
		targetfile.open(target);
		if (!targetfile) {
			cerr << "open file " << target << " failed!" << endl;
			if (ifs) ifs.close();
			return EXIT_FAILURE;
		}
		targetinput = &targetfile;
	}

	ACMachine ac;
	Xbw xbw;

	vector<string> words;
	istringstream line;
	//unsigned char d;
	string tmp;
	
	
	while (!ifs.eof()) {
		std::getline(ifs, tmp);
		if (tmp.empty())
			break;
		line.str(tmp);
		line.clear();
		//cout << "tmp string" << tmp << endl;
		while (!line.eof()) {
			line >> tmp;
			if ( words.size() < init_word_num)
				words.push_back(tmp);
			line >> tmp;
		}
		if (words.size() == init_word_num)
			break;
	}
	

	//int init_time = 0;
	//struct timeval init_start; //, init_end;
	if(make_xbw){
		xbw.buildingxbw(words, show_memory, words.size(), memory_or_speed);//xbw-acmachine
		//cout << "xbw-acmachine" << endl;
	}
	else{
		ac.addPatterns(words, show_memory, words.size());//normal-acmachine
		//cout << "normal-acmachine" << endl;
	}	

	words.clear();
	std::vector<std::string>().swap(words);

	if(show_time){

		ACMachine::state byte_count = 0;
		struct timeval start, end;
			
		if(make_xbw){
			//cout << "search start" << endl;
			gettimeofday(&start, NULL); 
			xbw.resetState();
			position pos = 0;
			string swindow = "";
			Xbw::alphabet c;
			while (!targetinput->eof()) {
				c = targetinput->get();
				byte_count++;
				if(byte_count > m_bytes)
					break;
				swindow.push_back(c);
				if (xbw.read(c, ignore_case)) {
					//cout << strwd << endl;
					//cout << "current output:" << xbw.currentOutput() << endl;
								
					if (!xbw.currentOutput().empty()) {
					//	for (auto pattlen : xbw.currentOutput()) {
					//		cout << swindow.substr(swindow.length() - pattlen, pattlen) << " @ " << (pos - pattlen + 1) << ", ";
					//	}
					//	cout << endl;
					}
								
				}
				else {
					//cout << "initial state" << endl;
					swindow.clear();
				}
				pos++;
			}
			//cout << endl;
					
			gettimeofday(&end, NULL);
			int sec = (end.tv_sec - start.tv_sec);
			int micro = (end.tv_usec - start.tv_usec);
			int passed = ((sec*1000000) + micro)/1000;
			//cout << passed << "ms" << endl;
			cout << passed << endl;
		}
		else{
			//cout << "search start" << endl;
			gettimeofday(&start, NULL);
			ac.resetState();
			position pos = 0;
			string swindow = "";
			ACMachine::alphabet c;
			while (!targetinput->eof()) {
				c = targetinput->get();
				byte_count++;
				if(byte_count > m_bytes)
					break;
				swindow.push_back(c);
				if (ac.read(c, ignore_case)) {
					//cout << strwd << endl;
					//cout << "current output:" << xbw.currentOutput() << endl;
								
					if (!ac.currentOutput().empty()) {
					//	for (auto pattlen : xbw.currentOutput()) {
					//		cout << swindow.substr(swindow.length() - pattlen, pattlen) << " @ " << (pos - pattlen + 1) << ", ";
					//	}
					//	cout << endl;
					}
								
				}
				else {
					//cout << "initial state" << endl;
					swindow.clear();
				}
				pos++;
			}
			gettimeofday(&end, NULL);
			int sec = (end.tv_sec - start.tv_sec);
			int micro = (end.tv_usec - start.tv_usec);
			int passed = ((sec*1000000) + micro)/1000;
			//cout << passed << "ms" << endl;
			cout << passed << endl;
			
		}

	}
		
	ifs.close();

	return 0;
	
}
