/*
* commandargs.h
*
*  Created on: 2017/03/02
*      Author: sin
*/

#ifndef COMMANDARGS2_H_
#define COMMANDARGS2_H_

#include <vector>
#include <map>

#include <cstdlib>
#include <cstring>

struct commandargs {
public:
	std::map<const char, const char *> opts;
	std::vector<const char *> args;

	commandargs(const int argc, char * const * argv, const char * optstr)
		: opts(), args() {
		getopt(argc, argv, optstr);
	}

private:
	void getopt(const int argc, char * const * argv, const char * optstr);

public:
	int arg_count() const { return args.size(); }
	int opt_count() const { return opts.size(); }
	std::pair<bool, const char*> opt(const char c) const;
	const char * arg(const int i) const { return args[i]; }
};

#endif /* COMMANDARGS_H_ */
