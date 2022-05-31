#include <iostream>
#include <fstream>
#include <set>
#include <queue>
#include <string>
#include <cstdlib>
#include <time.h>

using namespace std;

const int SIGMA_SIZE = 100;
int NODE_NUM = 0;

struct Trie {
	Trie *edges[SIGMA_SIZE];
	Trie *fail;
	set<string> out;
	//set<Trie*> ine;
	//vector<string> out;
	vector<Trie*> ine;
	int nodenum;

	Trie() {
		fail = NULL;
		nodenum = NODE_NUM;
		NODE_NUM++;
		for (int i = 0; i < SIGMA_SIZE; i++) {
			edges[i] = NULL;
		}

	}
};
Trie *root = new Trie();
Trie * current;

void addString(Trie *node, string &curString, int depth = 0) {
	if ( (unsigned) depth == curString.size()) {
		node->out.insert(curString);
		return;
	}
	int next = curString[depth] - ' ';
	if (node->edges[next] == NULL || node->edges[next] == root) {
		node->edges[next] = new Trie();
	}
	addString(node->edges[next], curString, depth + 1);
}

int addString2(Trie *node, string &curString, int depth = 0, int depth2 = -1) {
	current = node;
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
	return addString2(node->edges[next], curString, depth + 1, depth2);
}

int main(int argc, char * argv[]) {
	// rootの初期化
	for (int i = 0; i < SIGMA_SIZE; i++) {
		root->edges[i] = root;
		root->fail = root;
	}

	Trie *tr[50];
//	int queue_size = 0;
	int out_size = 0;
	int fail_size = 0;

	int word_num = 1;
	if ( argc > 1 )
		word_num = atoi(argv[1]);

	//goto関数の構成
	std::ifstream reading_file;
	string wordstr;
	string file_name;

	file_name = "word_list2.txt";
	//file_name = "test5.txt";
	//file_name = "aho_check_in.txt";

	//std::ifstream reading_file;
	string reading_line;

	reading_file.open(file_name, std::ios::in);
	if (reading_file.fail()) {
		std::cerr << "失敗" << std::endl;
		return -1;
	}

	for (int i = 0; i < word_num; i++) {
		std::getline(reading_file, reading_line);
		addString(root, reading_line);
	}

	// failure関数の構成
	queue<Trie*> q;

	// Must to this before, because of the fact that every edge out of the root is
	// not NULL
	for (int i = 0; i < SIGMA_SIZE; i++) {
		if (root->edges[i] != NULL && root->edges[i] != root) {
			root->edges[i]->fail = root;
			root->ine.push_back(root->edges[i]);
			q.push(root->edges[i]);
		}
	}

//	int j = 1;
	while (!q.empty()) {
		Trie *curNode = q.front();
		q.pop();

		for (int i = 0; i < SIGMA_SIZE; i++) {
			Trie *next = curNode->edges[i];
			if (next != NULL && next != root) {
				q.push(next);

				Trie *f = curNode->fail;
				for (; f->edges[i] == NULL; f = f->fail)
					;

				next->fail = f->edges[i];

				f->edges[i]->ine.push_back(next);

				for (auto s : next->fail->out) {
					next->out.insert(s);
				}
			}
		}
	}

	cout << "struct finish" << endl;

	// テキストからキーワードを検出
	string bigString;
	//std::ifstream ifs("test_text.txt");
	//std::ifstream ifs("test2.txt");
	//std::ifstream ifs("test4.txt");
	std::ifstream ifs("aho_check_out.txt");
	if (ifs.fail()) {
		std::cerr << "失敗" << std::endl;
		return -1;
	}
	getline(ifs, bigString);
	cout << bigString << endl;

	Trie *node = root;
	int k = bigString.size();
	for (int i = 0; i < k; i++) {
		int cur = bigString[i] - ' ';

		for (; node->edges[cur] == NULL; node = node->fail)
			;

		node = node->edges[cur];

		if (node->out.size() != 0) {
			cout << "At position " << i << " we found:\n";

			for (auto s : node->out) {
				cout << s << "\n";
			}
		}
	}

	//std::ifstream readline2("word_list2.txt");
	//std::ifstream readline2("test3.txt");
	std::ifstream readline2("aho_check_in_plus.txt");

	//動的な構成

	string curString2;

	//dynamic start
	while (1) {
		cout << "追加キーワードは？" << endl;
		cin >> curString2;

		clock_t total_start, total_end, start, end, c_start, c_end;
		double time1 = 0, time2 = 0, time3 = 0, c_time = 0;

		total_start = clock();

		if ( curString2.length() > 0 ) {

			int depth = 0;
			Trie *node2 = root;
			Trie *nodepoint;
			Trie *nodepoint2 = root;
//			int size2 = 0;
			int cur3 = 0;

//			size2 = curString2.size();

			start = clock();

			depth = addString2(root, curString2);

			end = clock();
			time1 += end - start;
			cout << "depth = "<< depth << ": " << curString2 << endl;

			if (depth == -1) {
				if (count(node2->out.begin(), node2->out.end(), curString2)
						> 0) {
					cout << "Why am I not occurring in the set .out?" << endl;
				} else {
					queue<Trie*> q4;
					Trie *rq;

					for (int k = 0; k < curString2.size(); k++) {
						cur3 = curString2[k] - ' ';
						node2 = node2->edges[cur3];
					}

					if ( current == node2 )
						cout << "It's current node!" << endl;

					q4.push(node2);

					while (!q4.empty()) {
						rq = q4.front();
						q4.pop();
						rq->out.insert(curString2);
						for (auto s : rq->ine)
							q4.push(s);
					}

				}
			} else {

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

				for (int k = depth; k < curString2.size(); k++) {
					Trie *next2 = nodepoint->edges[curString2[k] - ' '];

					Trie *f = nodepoint->fail;
//					int h = curString2[k] - ' ';

//					int p = 0;
					for (; f->edges[curString2[k] - ' '] == NULL; f = f->fail)
						;

					if (k == 0) {
						next2->fail = root;

						root->ine.push_back(next2);
					} else if (f->edges[curString2[k] - ' '] == root) {
						next2->fail = root;

						root->ine.push_back(next2);
					} else {
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
//				int q2_n = 0;

				start = clock();

				for (int i = 0; i < nodepoint2->ine.size(); i++) {
					if (nodepoint2->ine[i] != next3) {
						q2.push(nodepoint2->ine[i]);
						q2_num.push(depth);
					}
				}

				Trie *temp = root;
				for (int i = 0; i < curString2.size(); i++) {
					tr[i] = temp;
					temp = temp->edges[curString2[i] - ' '];

				}

				char curString3[50];

				for (int i = 0; i < curString2.size(); i++) {
					curString3[i] = curString2[i];
				}

				curString3[curString2.size()] = '*';
				curString3[curString2.size() + 1] = '\0';

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
						nodepoint3->edges[curString3[i] - ' ']->ine.push_back(
								rnext);

						r = rnext;

						nodepoint3 = nodepoint3->edges[curString3[i] - ' '];

						i = i + 1;

					}

					c_start = clock();
					if (curString2.size() <= i) {

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

		total_end = clock();
		std::cout << "total_time: "
				<< (double) (total_end - total_start) / CLOCKS_PER_SEC
				<< "sec.\n";
		std::cout << "time1: " << (double) time1 / CLOCKS_PER_SEC << "sec.\n";
		std::cout << "time2: " << (double) time2 / CLOCKS_PER_SEC << "sec.\n";
		std::cout << "time3: " << (double) time3 / CLOCKS_PER_SEC << "sec.\n";
		std::cout << "c_time: " << (double) c_time / CLOCKS_PER_SEC << "sec.\n";

		cout << "out size " << out_size << endl;

		// Read big string, in which we search for elements
		string bigString2;

		getline(ifs, bigString2);
		cout << bigString2 << endl;

		Trie *node3 = root;
		int k2 = bigString2.size();
		cout << "string size " << k2 << endl;
		cout << "root " << node3->nodenum << endl;

		for (int i = 0; i < k2; i++) {

			int cur = bigString2[i] - ' ';

			//ここまでok
			for (; node3->edges[cur] == NULL; node3 = node3->fail) {
				cout << "failure now... node number " << node3->fail->nodenum
						<< endl;
			}

			node3 = node3->edges[cur];

			cout << "current node number " << node3->nodenum << endl;

			if (node3->out.size() != 0) {
				cout << "At position " << i << " we found:\n";

				for (auto s : node3->out) {
					cout << s << "\n";
				}
			}

		}

	}
	//dynamic finish
	return 0;
}
