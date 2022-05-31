//============================================================================
// Name        : ACMachine.cpp
// Author      : Sin Shimozono
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <string>
#include <sstream>
#include <fstream>

using namespace std;

#include "ACMachine_varray.h"
#include "cmdargs.h"

#include <time.h>

int main(const int argc, char * const * argv) {
	unsigned long wordcount_max = 0;
	unsigned long additionalcount_max = 0;
	bool show_machine = false;
	bool show_words = false;
	bool ignore_case = false;
	bool verboseout = false;
	string target;
	ifstream patternfile;
	istream * patterninput = &cin;
	ifstream targetfile;
	istream * targetinput;

	commandargs optargs(argc, argv, "n:p:x:isvw");

	/*
	 * ./acm.exe -n $wc -x $adc -p -
	 *
	 * ./acm.exe -v -s -p microwords.txt smalltext.txt
	 *
	 */
	pair<bool,const char*> opt;
	opt = optargs.opt('v');
	if ( opt.first ) {
		verboseout = true;
	}
	opt = optargs.opt('n');
	if ( opt.first ) {
		wordcount_max = atol(opt.second);
	}
	opt = optargs.opt('x');
	if ( opt.first ) {
		additionalcount_max = atol(opt.second);
	}
	opt = optargs.opt('p');
	if ( opt.first ) {
		string fname = string(opt.second);
		if ( fname == "-" ) {
			if ( verboseout ) cout << "read patterns from std::cin " << fname << ", ";
			patterninput = &cin;
		} else {
			patternfile.open(fname);
			if ( verboseout ) cout << "read patterns from " << fname ;
			if ( !patternfile ) {
				cerr << ": open failed!" << endl;
				return EXIT_FAILURE;
			}
			patterninput = &patternfile;
			if ( verboseout ) cout << ", ";
		}
	}
	opt = optargs.opt('i');
	ignore_case = opt.first;
	opt = optargs.opt('s');
	show_machine = opt.first;
	opt = optargs.opt('w');
	show_words = opt.first;
	if ( optargs.arg_count() == 0 ) {
		if ( verboseout ) cout << "search in = cin" ;
		targetinput = &cin;
	} else {
		target = optargs.arg(0);
		if ( verboseout ) cout << "search in file = " << target;
		targetfile.open(target);
		if ( !targetfile ) {
			cerr << "open file " << target << " failed!" << endl;
			if ( patternfile ) patternfile.close();
			return EXIT_FAILURE;
		}
		targetinput = &targetfile;
	}
	if ( verboseout ) {
		cout << "wordcount_max = " << wordcount_max << ", ";
		cout << "additionalcount_max = " << additionalcount_max << ", ";
		cout << "ignore case = " << ignore_case << ", ";
		cout << "show_machine = " << show_machine << ", ";
		cout << "show_words = " << show_words << ", ";
		cout << endl;
	}

	ACMachine pmm;

	if ( verboseout )
		cout << "reading... " << std::flush;

	vector<string> words;
	istringstream line;
	string tmp;
	while ( !patterninput->eof() ) {
		std::getline(*patterninput, tmp);
		if ( tmp.empty() )
			continue; //break;
		line.str(tmp);
		line.clear();
		while ( !line.eof() ) {
			line >> tmp;
			if ( wordcount_max == 0 || words.size() < wordcount_max )
				words.push_back(tmp);
		}
	}
	if ( patternfile.is_open() ) patternfile.close();
	if ( verboseout )
		cout << "got " << words.size() << " words, " << std::endl;

	if ( show_words ) {
		cout << endl;
		for(auto tmp : words)
			cout << tmp << ", ";
		cout << endl << endl;
	}

	time_t sw = clock();
	pmm.addPatterns(words);
	sw = clock() - sw;

	words.clear();
	cout << "machine construction took " << sw / (double) CLOCKS_PER_SEC
			<< " sec." << endl;
	cout << pmm.stateCount() << " states, approx. " << (pmm.byteSize()/1024) << " Kbytes." << endl;
	if ( show_machine ){
		cout << endl << pmm << endl << endl;
	}
	//cout << "proceed?" << endl;
	//std::getline(cin, tmp);

	sw = clock();
	pmm.resetState();
	position pos = 0;
	string swindow = "";
	ACMachine::alphabet c;
	while ( !targetinput->eof() ) {
		c = targetinput->get();
		swindow.push_back(c);
		if ( pmm.read(c, ignore_case) ) {
			if ( !pmm.currentOutput().empty() ) {
				for(auto itr = pmm.currentOutput().begin();
						itr != pmm.currentOutput().end(); ++itr) {
				}
				for(auto pattlen : pmm.currentOutput()) {
					cout << swindow.substr(swindow.length() - pattlen, pattlen) << " @ " << (pos - pattlen + 1) << ", ";
				}
				cout << endl;
			}
		} else {
			//cout << "initial state" << endl;
			swindow.clear();
		}
		pos++;
	}
	//cout << endl;
	sw = clock() - sw;
	cout << "search took " << sw / (double) CLOCKS_PER_SEC << " sec." << endl;

	if ( targetfile ) targetfile.close();

	if ( verboseout ) cout << "bye." << endl;
	return 0;
}
