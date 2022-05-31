/*
 * ACTrie.h
 *
 *  Created on: 2018/07/18
 *      Author: sin
 */

#ifndef ACTRIE_H_
#define ACTRIE_H_

struct TrieNode;

class ACTrie {
	struct TrieNode {
		static const unsigned int alphabet_size = 1<<(sizeof(char)*8);
		TrieNode * child[ alphabet_size ];
		TrieNode * failure;
		char * matched_words;

		TrieNode() {
			for (int i = 0; i < alphabet_size; i++) {
				child[i] = NULL;
			}
			failure = NULL;
			matched_words = NULL;
		}

		~TrieNode() {
		}
	};

public:
	TrieNode * root;

	ACTrie() {
		root = new TrieNode();
		root->failure = root;
	}

	~ACTrie() {
		delete root;
	}

};

#endif /* ACTRIE_H_ */
