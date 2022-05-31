//============================================================================
// Name        : XBWTrie.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <cstddef>
#include <vector>

#include "ACMachine_varray.h"

using namespace std;

struct XBWTNode {
	uint16_t islast : 1;
	uint16_t isleaf : 1;
	uint16_t alph : 8;
};

int main() {
	cout << "!!!Hello World!!!" << endl; // prints !!!Hello World!!!
	cout << sizeof(XBWTNode) << endl;

	ACMachine pmm;
	vector<string> words = {
			"cat",
			"at",
			"cap",
			"bat",
			"battery",
			"bag",
	};

	pmm.addPatterns(words);
	if ( pmm.parent_child(0,7) ) {
		cout << "yes." << endl;
	} else {
		cout << "No." << endl;
	}

	cout << pmm << endl;

	return 0;
}
