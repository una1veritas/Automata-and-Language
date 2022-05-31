//============================================================================
// Name        : ACTrie.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
using namespace std;

#include "ACTrie.h"

int main() {
	cout << "!!!Hello World!!!" << endl; // prints !!!Hello World!!!

	ACTrie trie;

	cout << (unsigned long) trie.root << std::endl;
	cout << (trie.root == trie.root->failure) << std::endl;
	return 0;
}
