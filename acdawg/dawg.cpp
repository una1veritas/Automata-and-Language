/*
 * dawg.cpp
 *
 *  Created on: 2017/02/19
 *      Author: sin
 */

#include <algorithm>
#include <stack>
#include <queue>

#include "dawg.h"

std::ostream & DAWG::printOn(std::ostream & os ) const {
	std::queue<const WGNode *> qt;
	qt.push(&nroot);
	os << "DAWG(";
	while( !qt.empty() ) {
		const WGNode & top = *qt.front();
		os << '<' << top.nodenum;
		if ( top.isTrunk() ) {
			os << "(" << top.trunkid << ")";
		}
		os << '>';
		os << "[";
		for( std::pair<const int, WGNode *> assoc : top.edges ) {
			if ( assoc.second != NULL && !isRoot(assoc.second) ) {
				qt.push(assoc.second);
				if ( isprint(assoc.first) )
					os << "'" << (char)assoc.first << "'";
				else
					os << assoc.first << " ";
				os << "-> " << assoc.second->nodenum << "; ";
			}
			else if (assoc.second == NULL) {
				//os << "Error!!! ";
			}
		}
		os << "], " << std::endl;
		qt.pop();
	}
	os << ") ";
	return os;
}


WGNode * DAWG::split(WGNode *parentnode, WGNode *childnode, char a) {
	WGNode *newchildnode = new WGNode(NODE_NUM_DAWG++);
	WGNode *currentnode = parentnode;
	int charnum = a /* - ' ' */;

	parentnode->edges[charnum] = newchildnode;
	parentnode->edge_num[charnum] = 1;

	//childのedgeをすべてnewchildのsecondary-edgeにコピーする
	for (int i = 0; i < SIGMA_SIZE; i++) {
		newchildnode->edges[i] = childnode->edges[i];
		if (childnode->edges[i] != NULL)
			newchildnode->edge_num[i] = 2;
	}

	//parentnode->hassecedgechar[childnode->nodenum] = 0;

	newchildnode->suff = childnode->suff;
	newchildnode->suff->inedges.push_back(newchildnode);
	std::vector<WGNode*>::iterator itr =
			std::find(childnode->suff->inedges.begin(), childnode->suff->inedges.end(), childnode);
	childnode->suff->inedges.erase(itr);
	childnode->suff = newchildnode;
	newchildnode->inedges.push_back(childnode);

	int m = 0;
	while (currentnode != &nroot) {
		currentnode = currentnode->suff;
		for (m = 0; m < SIGMA_SIZE; m++) {
			if ((currentnode->edges[m] == childnode)
					&& (currentnode->edge_num[m] == 2)) {
				currentnode->edges[m] = newchildnode;
				break;
			}
		}

		if (m == (SIGMA_SIZE - 1))
			break;
	}

	return newchildnode;

}

WGNode * DAWG::update(WGNode *activenode, char a) {

	int charnum = a /* - ' ' */;

	if (activenode->edges[charnum] != NULL) {
		//辺がある場合
		if (activenode->edge_num[charnum] == 1) {
			return activenode->edges[charnum];
		} else {
			return split(activenode, activenode->edges[charnum], a);
		}
	} else {
		//辺がない場合
		WGNode *newactivenode = new WGNode(NODE_NUM_DAWG++);
		activenode->edges[charnum] = newactivenode;
		activenode->edge_num[charnum] = 1;

		WGNode *currentnode = activenode;

		while ((currentnode != &nroot) && (newactivenode->suff == NULL)) {
			currentnode = currentnode->suff;

			if ((currentnode->edges[charnum] != NULL)
					&& (currentnode->edge_num[charnum] == 1)) {
				newactivenode->suff = currentnode->edges[charnum];
				newactivenode->suff->inedges.push_back(newactivenode);
			} else if ((currentnode->edges[charnum] != NULL)
					&& (currentnode->edge_num[charnum] == 2)) {
				newactivenode->suff = split(currentnode,
						currentnode->edges[charnum], a);
				newactivenode->suff->inedges.push_back(newactivenode);
			} else {
				currentnode->edges[charnum] = newactivenode;
				currentnode->edge_num[charnum] = 2;
			}
		}

		if (newactivenode->suff == NULL) {
			newactivenode->suff = &nroot;
			nroot.inedges.push_back(newactivenode);
		}
		return newactivenode;
	}
}

std::vector<Trie *> DAWG::getoutstates(std::string &str) {
	std::vector<Trie *> outstates;
	WGNode *activenode = &nroot;
	WGNode *node;
	std::stack<WGNode*> st;

	for (unsigned int i = 0; (i < str.length()) && (activenode != NULL); i++) {
		activenode = activenode->edges[(int)str[i] /* - ' ' */];
	}

	if (activenode != NULL) {
		std::queue<WGNode*> queue;
		queue.push(activenode);
		while (!queue.empty()) {
			node = queue.front();
			queue.pop();
			if ( node->isTrunk() ) { //node->torb == 1) {
				outstates.push_back(node->dtoc);
			}

			for (unsigned int i = 0; i < node->inedges.size(); i++) {
				queue.push(node->inedges[i]);
			}

		}
	}

	return (outstates);
}

std::vector<Trie *> DAWG::getFailStates(std::string &str, int depth) {
	std::vector<Trie *> failstates;
	std::vector<int> tmp;
	WGNode *activenode = &nroot;
//	WGNode *node;
	WGNode *enode;
//	int num;
	std::stack<std::pair<WGNode*,int>> wgstack;
	//std::stack<int> st_num;

	for (unsigned int i = 0; (i <= str.length()) && (activenode != NULL); i++) {
		if ( i >= (unsigned)depth && (activenode != NULL)) {
			wgstack.push(std::pair<WGNode*,int>(activenode,i) );
		}
		if (i == str.length())
			break;

		activenode = activenode->edges[(int)str[i]];
	}

	std::queue<WGNode*> queue;
	std::vector<WGNode*> mark;

	while (!wgstack.empty()) {
		std::pair<WGNode*,int>  nodenum = wgstack.top();
		wgstack.pop();
//		node = wgstack.top();
//		wgstack.pop();
//		num = st_num.top();
//		st_num.pop();
		queue.push(nodenum.first);

		while (!queue.empty()) {
			enode = queue.front();
			queue.pop();

			std::vector<WGNode*>::iterator itr = find(mark.begin(), mark.end(), enode);
			if (itr == mark.end()) {
				mark.push_back(enode);
				//if (enode->torb == 1) {
				if ( enode->isTrunk() ) {
					enode->dtoc->ine_num = nodenum.second;
					failstates.push_back(enode->dtoc);
				} else {
					for (unsigned int i = 0; i < nodenum.first->inedges.size(); i++) {
						queue.push(nodenum.first->inedges[i]);
					}
				}
			}
		}
	}
	return failstates;
}

void DAWG::addString(ACTrie & actrie, const std::string & wordstr) {
	//
	//dawgの構成
	//

//	root().trunkid = ac_num(); //DAWGTOAC_NUM;
	//DAWGTOAC_NUM++;
//	root().setTrunk(); //torb = 1;

	WGNode *activenode;
	activenode = & root();
	WGNode *tnode;

	Trie *trienode;
	Trie *tmptrie;

	for (unsigned int j = 0; j < wordstr.length(); j++)
		activenode = update(activenode, wordstr[j]);

	activenode = &root(); //nroot;
	trienode = &actrie.root();

	activenode = activenode->edges[(int)wordstr[0] /* - ' ' */];
	trienode = trienode->edges[(int)wordstr[0] /* - ' ' */];

	for (unsigned int j = 1; j < wordstr.length(); j++) {
		if ( activenode->isTrunk() ) {
			//if (activenode->torb == 1) {
			setTrunkID(*activenode); //->trunkid = ac_num(); //DAWGTOAC_NUM;
			//DAWGTOAC_NUM++;
			activenode->setTrunk(); //torb = 1;
			activenode->dtoc = trienode;
		}

		tnode = activenode->edges[(int)wordstr[j] /* - ' ' */];
		tmptrie = trienode->edges[(int)wordstr[j] /* - ' ' */];
		activenode = tnode;
		trienode = tmptrie;
	}
	if ( !activenode->isTrunk() ) { //trunk == 0) {
		setTrunkID(*activenode); //->trunkid = ac_num(); //DAWGTOAC_NUM;
		//DAWGTOAC_NUM++;
		activenode->setTrunk(); //torb = 1;
		activenode->dtoc = trienode;
	}
	activenode = & root(); //nroot;
}
