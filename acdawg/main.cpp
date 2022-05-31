#include <iostream>
#include <fstream>
#include <sstream>
#include <set>
#include <map>
#include <queue>
#include <string>
#include <vector>
#include <stack>
#include <algorithm>
#include <time.h>

#include <ctype.h>

#include "actrie.h"
#include "dawg.h"

using namespace std;

struct TextFile {
private:
	ifstream file;
	string wbuf;

	void getNextWord() {
		if ( file.eof() )
			wbuf = "";
		else
			file >> wbuf;
	}

public:
	TextFile(string & fname) {
		file.open(fname, ios::in);
		if ( file.fail() )
			wbuf = "";
		else
			getNextWord();
	}

	~TextFile(void) {
		file.close();
	}

	bool failed() { return file.fail(); }
	bool atEnd() {
		return wbuf.empty() || file.eof();
	}

	void reset() {
		file.clear();
		file.seekg(0);
		getNextWord();
	}

	string & word() {
		return wbuf;
	}

	TextFile & next() { getNextWord(); return *this; }
};


int main(int argc, char * argv[]) {
	string file1name = "word_list2.txt";
	string checkfilename = "aho_check_out.txt";
	stringstream sstream;
	int word_build_num = 10;
	int word_add_num = 10;

	//キーワード（の集合）が入力として与えられる
	//キーワードを用いて、通常の方法でACマシンとDAWGを作る

	//
	//ACマシンの構成
	//

	DAWG dawg;
	ACTrie actrie;

	int out_size = 0;

	//goto関数の構成

	if ( argc == 4 ) {
		file1name = argv[1];
		sstream.str(argv[2]);
		sstream.clear();
		sstream >> word_build_num;
		sstream.str(argv[3]);
		sstream.clear();
		sstream >> word_add_num;
	}

	cout << "Opening ile " << file1name << "... ";
	TextFile txfile(file1name);
	if ( txfile.failed() ) {
		std::cerr << std::endl << "failed to open " << file1name << std::endl;
		return EXIT_FAILURE;
	}
	cout << "done. " << std::endl;

	// goto関数と状態の追加
	for (int i = 0; i < word_build_num && !txfile.atEnd(); i++ ) {
		string & word = txfile.word();
		cout << i << ": " << word << endl;
		actrie.addStringPath(word); // Add goto transitions and transfer to there
		actrie.addOutput(word); // Add output string to the current state
		txfile.next();
	}
	actrie.buildFailures();

	cout << "Construct ac machine finished." << endl;
	cout << actrie << endl << endl;

	txfile.reset();
	for (int i = 0; i < word_build_num && !txfile.atEnd(); i++, txfile.next() ) {
		string & word = txfile.word();
		dawg.addString(actrie, word);
	}
	cout << "Construct DAWG finished." << endl << endl;
	cout << dawg << endl << endl;

	//（動作確認）
	string text;
	std::ifstream ifs(checkfilename);
	if (ifs.fail()) {
		std::cerr << "failed to open " << checkfilename << std::endl;
		return EXIT_FAILURE;
	}
	while ( !ifs.eof() ) {
		string str;
		getline(ifs, str);
		text.append(str);
		text.append("\n");
	}

	cout << "test text = '" << text << "'" << endl;
	cout << "length = " << text.length() << std::endl;
	vector<pair<int,string>> occurrences;
	actrie.scan(text, occurrences);
	for(const pair<int,string> & occurr : occurrences ) {
		std::cout << "'" << occurr.second << "'@" << occurr.first << ", ";
	}
	cout << std::endl << std::endl;
	occurrences.clear();

	//
	//キーワードを新たに与える（一語ずつ）
	//DAWGを動的に構成
	//DAWGをもとにACマシンを更新
	//

	//dynamic start

	cout << "Going to add " << word_add_num << " keywords to the existing machine. " << endl << endl;

		clock_t start, end, total_start, total_end;
		double time1 = 0, time2 = 0, time3 = 0, time4 = 0, time5 = 0;

		total_start = clock();

		for (int i = 0; i < word_add_num && !txfile.atEnd(); i++, txfile.next() ) {
			Trie * tactivenode;
			Trie *newstates[50];
//			int depth = 0;

			string & curString2 = txfile.word();
			int size2 = 0;
//			int cur3 = 0;

			WGNode *activenode = &dawg.root(); //nroot;
			WGNode *tnode = &dawg.root(); //nroot;

			cout << i << ": "<< curString2 << " " << endl;

			size2 = curString2.size();

			//Algorithm1

			start = clock();

			int trie_depth = 10000;
/*
			tactivenode = &actrie.root();
			int charnum = 0;
			for (int i = 0; i < size2; i++) {
				newstates[i] = tactivenode;
				charnum = curString2[i]; // - ' ';
				if (tactivenode->edges[charnum] != NULL
						&& tactivenode->edges[charnum] != &actrie.root()) {
					tactivenode = tactivenode->edges[charnum];
				} else {

					if (trie_depth == 10000) {
						trie_depth = i + 1;
					}
					//Trie *newstate = new Trie();
					//tactivenode->edges[charnum] = newstate;
					actrie.addBranch(*tactivenode, charnum);
					tactivenode = tactivenode->edges[charnum];
				}
			}
			cout << "Arrived at " << *tactivenode << endl;

			cout << "trie_depth = " << trie_depth << endl;
	*/
			actrie.resetState();
			trie_depth = 1 + actrie.addStringPath(curString2);
			cout << "trie_depth = " << trie_depth << endl;
			//tactivenode = &actrie.currentState();
			actrie.addOutput(curString2);
			cout << "addStringPath arrived at " << actrie.currentState() << endl;
			cout.flush();

			newstates[size2] = &actrie.currentState(); //tactivenode;
			//tactivenode->out.insert(curString2);

			end = clock();
			time1 += (end - start);

			start = clock();

			vector<Trie*> failstates;
			failstates = dawg.getFailStates(curString2, trie_depth);
			int fstatesize = failstates.size();

			for (int i = fstatesize - 1; i >= 0; i--) {
				cout << "failstates = " << failstates[i]->ine_num << endl;
				failstates[i]->fail = newstates[failstates[i]->ine_num];
			}

			end = clock();
			time2 += (end - start);

			tactivenode = &actrie.root();
			Trie *failurenode;

			start = clock();

			int charnum2 = 0;

			for (int i = 0; i < size2; i++) {
				cerr << "i = " << i << endl;
				cerr.flush();
				charnum2 = curString2[i] /* - ' ' */;

				if ((i + 1) >= trie_depth) {
					if (tactivenode == &actrie.root()) {
						tactivenode->edges[charnum2]->fail = &actrie.root();
						tactivenode = tactivenode->edges[charnum2];
					} else {
						failurenode = tactivenode->fail;

						int j = 0;
						cerr << "failurenode " << *failurenode << endl;
						cerr.flush();
						while ((failurenode->edges[charnum2] == NULL)
								|| (failurenode->edges[charnum2] == tactivenode)
								|| (failurenode == &actrie.root())) {

							if (j >= 2)
								break;

							failurenode = failurenode->fail;
							if (failurenode == &actrie.root())
								j++;

						}

						tactivenode = tactivenode->edges[charnum2];

						tactivenode->fail = failurenode->edges[charnum2];

						for (auto s : failurenode->edges[charnum2]->out)
							tactivenode->out.insert(s);

					}

				} else {
					tactivenode = tactivenode->edges[(int)curString2[i] /* - ' ' */];
				}
			}

			end = clock();
			time3 += (end - start);

			vector<Trie *> outstates;

			start = clock();

			outstates = dawg.getoutstates(curString2);

			int outstatesize = outstates.size();

			out_size += outstatesize;

			for (int i = 0; i < outstatesize; i++) {
				outstates[i]->out.insert(curString2);
			}

			end = clock();
			time4 += (end - start);

//			Trie *check_trie = troot;

			activenode = &dawg.root(); //nroot;

			start = clock();

			for (int i = 0; i < size2; i++)
				activenode = dawg.update(activenode, curString2[i]);

			activenode = &dawg.root(); //nroot;
			Trie *trienode = &actrie.root();
			Trie *tmptrie;

			activenode = activenode->edges[(int)curString2[0] /* - ' ' */];
			trienode = trienode->edges[(int)curString2[0] /* - ' ' */];

			for (int i = 1; i < size2; i++) {
				if ( !activenode->isTrunk() ) { //trunk == 0) {
					dawg.setTrunkID(*activenode); //->trunkid = dawg.ac_num(); //DAWGTOAC_NUM;
					//dawg.inc_ac_num(); //DAWGTOAC_NUM++;
					activenode->setTrunk(); //torb = 1;
					activenode->dtoc = trienode;
				}

				tnode = activenode->edges[(int)curString2[i] /* - ' ' */];
				tmptrie = trienode->edges[(int)curString2[i] /* - ' ' */];
				activenode = tnode;
				trienode = tmptrie;
			}

			if (activenode->trunkid == 0) {
				dawg.setTrunkID(*activenode); //->trunkid = dawg.ac_num(); //DAWGTOAC_NUM;
				//dawg.inc_ac_num(); //DAWGTOAC_NUM++;
				activenode->setTrunk(); //torb = 1;
				activenode->dtoc = trienode;
			}

			activenode = &dawg.root(); //nroot;

			end = clock();
			time5 += (end - start);

		}

		total_end = clock();

		cout << actrie << endl << endl;

		cout << "total time: "
				<< (double) (total_end - total_start) / CLOCKS_PER_SEC << "sec."
				<< std::endl;
		cout << "time1: " << (double) time1 / CLOCKS_PER_SEC << "sec."
				<< std::endl;
		cout << "time2: " << (double) time2 / CLOCKS_PER_SEC << "sec."
				<< std::endl;
		cout << "time3: " << (double) time3 / CLOCKS_PER_SEC << "sec."
				<< std::endl;
		cout << "time4: " << (double) time4 / CLOCKS_PER_SEC << "sec."
				<< std::endl;
		cout << "time5: " << (double) time5 / CLOCKS_PER_SEC << "sec."
				<< std::endl;

		cout << "out size " << out_size << endl;

		// Read big string, in which we search for elements
		string bigString2;

		getline(ifs, bigString2);
		cout << bigString2 << endl;

		Trie *node3 = &actrie.root();
		int k2 = bigString2.size();
		cout << "string size " << k2 << endl;

		for (int i = 0; i < k2; i++) {

			int cur = bigString2[i] /* - ' ' */;

			for (; node3->edges[cur] == NULL; node3 = node3->fail) {
				cout << "failure now... node number " << node3->fail->nodenum
						<< endl;
			}

			node3 = node3->edges[cur];

			cout << "current node number " << node3->nodenum << endl;

			if (node3->out.size() != 0) {
				cout << "At position " << i << " we found:" << std::endl;

				for (auto s : node3->out) {
					cout << s << std::endl;
				}
			}

		}

	//dynamic finish

	return 0;
}

