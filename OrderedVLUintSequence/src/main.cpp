//============================================================================
// Name        : main.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include "OrderedVLUintSequence.h"
using namespace std;

int main() {
	cout << "!!!Hello World!!!" << endl; // prints !!!Hello World!!!

	OrderedVLUintSequence seq;
	seq.add(126);
	seq.add(2337);
	seq.add(43324);
	seq.add(13);
	seq.add(938184);
	seq.add(384);
	seq.add(1753);

	cout << "size = " << seq.size() << endl;

	cout << seq << endl;

	uint64_t val = 2800;
	if ( seq.includes(val) ) {
		cout << "found." << endl;
	} else {
		cout << "not found." << endl;
		seq.add(val);
		cout << seq << endl;
	}
	return 0;
}
