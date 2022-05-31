/*
 * actrie.cpp
 *
 *  Created on: 2017/02/19
 *      Author: sin
 */

#include <queue>

#include "actrie.h"

std::ostream & Trie::printOn(std::ostream & os) const {
	os << '<' << nodenum << '>';
	if ( !out.empty() ) {
		os << "{";
		for(const std::string & str : out ) {
			os << "\"" << str << "\", ";
		}
		os << "}";
	}
	return os;
}

std::ostream & ACTrie::printOn(std::ostream & os) const {
	std::queue<const Trie *> qt;
	qt.push(&troot);
	os << "ACTrie(";
	while( !qt.empty() ) {
		const Trie & top = *qt.front();
		os << '<' << top.nodenum << '>';
		if ( !top.out.empty() ) {
			os << "{";
			for(const std::string & str : top.out ) {
				os << "\"" << str << "\", ";
			}
			os << "}";
		}
		os << "[";
		for( std::pair<const int, Trie *> assoc : top.edges ) {
			if ( assoc.second != NULL && !isRoot(assoc.second) ) {
				qt.push(assoc.second);
				if ( isprint(assoc.first) )
					os << "'" << (char)assoc.first << "'";
				else
					os << assoc.first << " ";
				os << "-> " << assoc.second->nodenum << "; ";
			}
			else if ( !isRoot(assoc.second) ) {
				os << "Error!!! ";
				if ( isprint(assoc.first) )
					os << "'" << (char)assoc.first;
				else
					os << assoc.first;
				os << " -> NULL; ";
			}

		}
		if ( top.fail != NULL ) {
			os << "*-> " << top.fail->nodenum;
		}

		os << "], " << std::endl;
		qt.pop();
	}
	os << ") ";
	return os;
}

Trie * ACTrie::branch(Trie & node, int ch) const {
	std::map<const int, Trie *>::iterator it = node.edges.find(ch);
	std::pair<const int,Trie*> entry = *it;
	if ( it == node.edges.end() )
		return NULL;
	return entry.second;
}

int ACTrie::addStringPath(const std::string & str) {
	int extendLen = 0;
	resetState();
	for (unsigned int depth = 0; depth < str.size(); depth++) {
		Trie * next = branch(str[depth]);
		if ( next == NULL || isRoot(next) ) {
			addBranch(str[depth]); //node->edges[next] = new Trie();
			extendLen++;
		}
		transferState(str[depth]);
	}
	return extendLen;
}

/*
int ACTrie::addString2(Trie *node, const string &curString, int depth = 0, int depth2 = -1) {

	if (depth == curString.size()) {
		node->out.insert(curString);

		return depth2;
	}

	int next = curString[depth]; // - ' ';

	if (node->edges.find(next) == node->edges.end() || isRoot(*node->edges[next]) ) {
		addBranch(*node, next); //node->edges[next] = new Trie();
		if (depth2 == -1)
			depth2 = depth;
	}

	return addString2(node->edges[next], curString, depth + 1, depth2);
}
*/

void ACTrie::buildFailures() {
	std::queue<Trie *> q;

	// set up failures of root
	// Must to this before, because of the fact that every edge out of the root
	// must not be NULL.
	resetState();
//	for (int i = 0; i < SIGMA_SIZE; i++) {
	// skips if == NULL
	for(auto const & assoc : currentState().edges ) {
		int i = assoc.first;
		// if is neither an explicit failure, nor go-root-failure
		Trie * next = branch(i);
		if ( next == NULL || isRoot(next) )
			continue;
		// if the current (== root) has a fair branch
		branch(i)->fail = &root();
		q.push(branch(i));
	}

	while ( !q.empty() ) {
		setState(*q.front());
		q.pop();

		// skips if == NULL
		for(auto const & assoc : currentState().edges ) {
			int i = assoc.first;
//		for (int i = 0; i < SIGMA_SIZE; i++) {
			Trie * next = branch(i);
//			if (next != NULL && next != &root()) {
			if ( isRoot(*next) )
				continue;
			q.push(next);

			Trie * failnode = currentState().fail;
			while ( branch(*failnode,i) == NULL ) {
				failnode = failnode->fail;
			}
			next->fail = branch(*failnode, i); //->edges.at(i);
			for (const std::string & str : next->fail->out) {
				next->out.insert(str);
			}
		}
	}
}

// ch is the character for which the machine will make a transition.
void ACTrie::transferState(int ch)  {
	while ( branch(ch) == NULL ) {
		current = current->fail;
	}
	current = branch(ch);
}

void ACTrie::scan(std::string & text, std::vector<std::pair<int,std::string>> & occurrs) {
	resetState();
//	Trie *node = &root();

	for (unsigned int i = 0; i < text.size(); i++) {
		transferState(text[i]);
		if (currentState().out.size() != 0) {
			for (const std::string & str : currentState().out) {
				occurrs.push_back(std::pair<int, std::string>(i-str.length()+1, str));
			}
		}
	}

}

//#define NAIVE_PATTERN_ADDITION
#ifdef NAIVE_PATTERN_ADDITION
/*
int addString2(Trie *node, string &curString, int depth = 0, int depth2 = -1) {

	if (depth == curString.size()) {
		node->out.insert(curString);

		return depth2;
	}

	int next = curString[depth] - ' ';

	if (node->edges[next] == NULL || node->edges[next] == root) {
		node->edges[next] = new Trie();
		if (depth2 == -1)
			depth2 = depth;
	}

	addString2(node->edges[next], curString, depth + 1, depth2);
}
 */
void ACTrie::addPattern(const string & patt) {
//	Trie *node2 = root;
//	Trie *nodepoint;
//	Trie *nodepoint2 = root;
//	int cur3 = 0;

	//int size2 = 0;
	//size2 = curString2.size();

	//depth = addString2(root, curString2);
	// seems that depth == -1 means no new branch has spawned,
	// i.e. string is existing or is a prefix of some already-added word.

	int extended = 0;
	resetState();
	extended = addString(patt);
	queue<Trie &> trieq;
//	if (depth == -1) {
	if ( extended == 0 ) {
//		cout << "depth = -1" << endl;
//		cout << curString2 << endl;
		cout << patt << " is just a prefix of some other pattern." << endl;

		//queue<Trie*> q4;
		//Trie *rq;

		trieq.push(currentState());

		while ( !trieq.empty() ) {
			Trie & node = trieq.front();
			trieq.pop();
			node.out.insert(patt);
			for (auto s : node.front().inedges) {
				trieq.push(s);
			}
		}
	}
	else {

		start = clock();

		if (depth != 0) {
			for (int k = 0; k < depth; k++) {
				cur3 = curString2[k] - ' ';
				node2 = node2->edges[cur3];
				//cout << "cur3 " << cur3 << " " << node2->nodenum << endl;
			}
		}

		nodepoint = node2;
		nodepoint2 = nodepoint;

		Trie *next3 = nodepoint->edges[curString2[depth] - ' '];


		for (int k = depth; k < size2; k++) {
			Trie *next2 = nodepoint->edges[curString2[k] - ' '];

			Trie *f = nodepoint->fail;
			int h = curString2[k] - ' ';

			int p = 0;
			for (; (f->edges[curString2[k] - ' '] == NULL); f = f->fail);

			if (k == 0) {
				next2->fail = root;

				root->ine.push_back(next2);
			}
			else if ((f->edges[curString2[k] - ' '] == root)) {
				next2->fail = root;

				root->ine.push_back(next2);
			}
			else {
				next2->fail = f->edges[curString2[k] - ' '];

				f->edges[curString2[k] - ' ']->ine.push_back(next2);

				if (next2->fail->out.size() > 0)
					for (auto s : next2->fail->out)
						next2->out.insert(s);

			}

			nodepoint = next2;

		}

		end = clock();
		time2 += end - start;



		//既存の関数の更新

		// build the fail function
		queue<Trie*> q2;
		queue<int> q2_num;
		int q2_n = 0;

		start = clock();

		for (int i = 0; i < nodepoint2->ine.size(); i++) {
			if (nodepoint2->ine[i] != next3) {
				q2.push(nodepoint2->ine[i]);
				q2_num.push(depth);
			}
		}

		Trie *temp = root;
		for (int i = 0; i < size2; i++) {
			tr[i] = temp;
			temp = temp->edges[curString2[i] - ' '];

		}


		char curString3[50];

		for (int i = 0; i < size2; i++) {
			curString3[i] = curString2[i];
		}


		curString3[size2] = '*';
		curString3[size2+1] = '\0';

		Trie *r, *rnext;
		Trie *nodepoint3;

		fail_size = 0;
		while (!q2.empty()) {
			r = q2.front();
			q2.pop();
			int i = q2_num.front();
			q2_num.pop();

			nodepoint3 = tr[i];

			while ((r->edges[curString3[i] - ' '] != NULL)) {
				rnext = r->edges[curString3[i] - ' '];

				rnext->fail = nodepoint3->edges[curString3[i] - ' '];
				nodepoint3->edges[curString3[i] - ' ']->ine.push_back(rnext);

				r = rnext;

				nodepoint3 = nodepoint3->edges[curString3[i] - ' '];

				i = i + 1;

			}

			c_start = clock();
			if (size2 <= i) {

				auto itr = r->out.find(curString2);
				if (itr == r->out.end()) {
					r->out.insert(curString2);
					out_size++;
				}
			}
			c_end = clock();
			c_time += c_end - c_start;

			for (int j = 0; j < r->ine.size(); j++) {
				q2.push(r->ine[j]);
				q2_num.push(i);
			}

		}

		end = clock();
		time3 += end - start;

	}
}
#endif

