/*
 * OrderedVLUintSequence.h
 *
 *  Created on: 2018/08/30
 *      Author: sin
 */

#ifndef ORDEREDVLUINTSEQUENCE_H_
#define ORDEREDVLUINTSEQUENCE_H_

#include <iostream>
#include <vector>

class OrderedVLUintSequence {
	/// an ordered sequence of variable digit length unsigned integer
	/// coded in 15 bits in uint16 arrays, start word with 1<<15 flag,
	/// in little-endian 16bit-word order

	typedef std::vector<uint8_t>::size_type position;

	std::vector<uint8_t> uintseq;
	position count;

	static uint8_t nlz32_IEEEFP(uint32_t x);
	static uint8_t signifbits(const uint64_t & x);

public:
	typedef std::vector<uint8_t>::iterator iterator;
	typedef std::vector<uint8_t>::const_iterator const_iterator;

private:
	const_iterator find(const uint64_t & key) const;
	void insert(const iterator & pos, const uint64_t & orgval);

	std::ostream & printOn(std::ostream & out) const;

public:
	OrderedVLUintSequence() { uintseq.clear(); count = 0; }

	position size() const { return count; }

	bool includes(const uint64_t & key) const;
	void add(const uint64_t & val);
	uint64_t at(const position & index) const;
	position skip(const_iterator & pos, const position & count = 1) const;
	uint64_t read(const_iterator it) const;

	uint64_t next(iterator & it) const { return next((const_iterator&) it); }
	uint64_t next(const_iterator & it) const;

	friend std::ostream & operator<<(std::ostream & out, const OrderedVLUintSequence & seq) {
		return seq.printOn(out);
	}
};


#endif /* ORDEREDVLUINTSEQUENCE_H_ */
