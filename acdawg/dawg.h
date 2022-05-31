/*
 * dawg.h
 *
 *  Created on: 2017/02/19
 *      Author: sin
 */

#ifndef DAWG_H_
#define DAWG_H_

#include <string>
#include <vector>

#include "actrie.h"


//int NODE_NUM_DAWG;
//int DAWGTOAC_NUM;

struct WGNode {
	//dawgにおけるノードの番号
	int nodenum;
	std::map<int, WGNode *> edges;
	//edge_num[i]  0 = edgeなし 1 = primary-edgeあり 2 = secondary-edgeあり
	std::map<int,int> edge_num;
	std::vector<WGNode*> inedges;
	WGNode *suff;
	Trie *dtoc;

	//ACのノードとdawgのノードの番号を一致させるための変数
//	int dawgtoac;
	int trunkid;
private:
	//trunkノードかbranchノードかの判定 1ならtrunk、0ならbranch 初期値は0
	int torb;

public:
	bool isTrunk() const { return torb == 1; }
	void setTrunk() { torb = 1; }
	void setBranch() { torb = 0; }
	void setTrunkID(const int id) { trunkid = id; }

	WGNode(const int id) :
		nodenum(id), edges(), edge_num(), inedges(), suff(NULL), dtoc(NULL), trunkid(0), torb(0) {
	}

};

class DAWG {
	WGNode nroot;

	int NODE_NUM_DAWG;
	int DAWGTOAC_NUM;

public:
	DAWG(void) : nroot(0), NODE_NUM_DAWG(1), DAWGTOAC_NUM(0) {
		nroot.setTrunk();
		DAWGTOAC_NUM++;
	}

	WGNode & root() { return nroot; }
	bool isRoot(const WGNode & node) const { return &nroot == &node; }
	bool isRoot(const WGNode * node) const { return &nroot == node; }
	WGNode * split(WGNode *parentnode, WGNode *childnode, char a);
	WGNode * update(WGNode *activenode, char a);
	std::vector<Trie *> getoutstates(std::string &str);
	std::vector<Trie *> getFailStates(std::string &str, int depth);
	void addString(ACTrie & actrie, const std::string & patt);

	int setTrunkID(WGNode & node) {
		node.setTrunkID(DAWGTOAC_NUM);
		DAWGTOAC_NUM++;
		return DAWGTOAC_NUM;
	}

	std::ostream & printOn(std::ostream &) const;

	// friend operators
	friend std::ostream & operator<<(std::ostream & os, const DAWG & dag) { return dag.printOn(os); }
};



#endif /* DAWG_H_ */
