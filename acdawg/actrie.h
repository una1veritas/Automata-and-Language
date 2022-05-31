/*
 * actrie.h
 *
 *  Created on: 2017/02/19
 *      Author: sin
 */

#ifndef ACTRIE_H_
#define ACTRIE_H_

#include <iostream>
#include <vector>
#include <string>
#include <set>
#include <map>

const int SIGMA_SIZE = 255;

struct Trie {
	int nodenum;
	std::set<std::string> out;

	//Trie *edges[SIGMA_SIZE];
	std::map<const int, Trie *> edges;
	Trie *fail;
	int ine_num;

	Trie(const int id) : nodenum(id), out(), fail(NULL), ine_num(0) {
		out.clear();
	}

	int id(void) const { return nodenum; }

	bool addOutput(const std::string & str) {
		return (out.insert(str)).second;
	}

	std::ostream & printOn(std::ostream &) const;

	// friend operators
	friend std::ostream & operator<<(std::ostream & os, const Trie & trie) { return trie.printOn(os); }

};

// AC Machine by Trie
class ACTrie {
	Trie troot; // = Trie(0);
	int node_num;

	Trie * current;

public:
	ACTrie() : troot(0), node_num(1), current(&troot) {
		// rootの初期化
		for (int i = 0; i < SIGMA_SIZE; i++) {
			root().edges[i] = &root();
			root().fail = &root();
		}
	}

	unsigned int size() const {
		return node_num;
	}
	Trie & root(void) {	return troot; }
	bool isRoot(const Trie & t) const {
		return &t == &troot;
	}
	bool isRoot(const Trie * t) const {
		return t == &troot;
	}
	Trie * branch(Trie & node, int ch) const;
	inline Trie * branch(int ch) const { return branch(*current, ch); }

	Trie & addBranch(Trie & node, int ch) {
		node.edges[ch] = new Trie(node_num);
		node_num++;
		return node;
	}
	inline Trie & addBranch(int ch) { return addBranch(*current, ch); }
	int addStringPath(const std::string &str);
	bool addOutput(const std::string & str) { return current->addOutput(str); }

	void addPattern(const std::string & patt);

	void buildFailures();
	void scan(std::string & text, std::vector<std::pair<int,std::string>> & occurrs);


	void resetState(void) { current = &troot; }
	Trie & currentState(void) { return *current; }
	void transferState(int ch);
	void setState(Trie & node) { current = &node; }

	std::ostream & printOn(std::ostream &) const;

	// friend operators
	friend std::ostream & operator<<(std::ostream & os, const ACTrie & trie) { return trie.printOn(os); }
};


#endif /* ACTRIE_H_ */
