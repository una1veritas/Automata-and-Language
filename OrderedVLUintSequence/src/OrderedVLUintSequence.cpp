//============================================================================
// Name        : OrderedVLUintSequence.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include "OrderedVLUintSequence.h"

// static utility functions
uint8_t OrderedVLUintSequence::nlz32_IEEEFP(uint32_t x) {
	/* Hacker's Delight 2nd by H. S. Warren Jr., 5.3, p. 104 -- */
	double d = (double)x + 0.5;
	uint32_t *p = ((uint32_t*) &d) + 1;
	return 0x41e - (*p>>20);  // 31 - ((*(p+1)>>20) - 0x3FF)
}

uint8_t OrderedVLUintSequence::signifbits(const uint64_t & x) {
	struct LowHigh64 {
		uint32_t low, high;
	};
	LowHigh64 * lh = & (LowHigh64 &) x;
	const uint8_t nlz_high = nlz32_IEEEFP(lh->high);
	return (nlz_high == 32 ? 32 - nlz32_IEEEFP(lh->low) : 64 - nlz_high );
}
//

OrderedVLUintSequence::const_iterator OrderedVLUintSequence::find(const uint64_t & key) const {
	const_iterator left = uintseq.begin();
	const_iterator right = uintseq.end();
	const_iterator pos;
	while ( left != right ) {
		pos = left + ((right - left)>>1);
		while ( pos != uintseq.end() && (*pos & 0x80) == 0 )
			++pos;
		if ( pos == right ) {
			--pos;
			while ( (*pos & 0x80) == 0 )
				--pos;
		}
		uint64_t val;
		val = read(pos);
		if ( val < key ) {
			if ( left == pos )
				next(pos);
			left = pos;
		} else {
			right = pos;
		}
	}
	return right;
}

/*
	iterator find_linear(const uint64_t & key) {
		iterator itr = uintseq.begin();
		iterator t_itr;
		while ( itr != uintseq.end() ) {
			t_itr = itr;
			if ( key <= next(t_itr) )
				return itr;
			itr = t_itr;
		}
		return itr;
	}
*/

void OrderedVLUintSequence::insert(const iterator & pos, const uint64_t & orgval) {
	uint64_t val = orgval;
	uint8_t digits = signifbits(val);
	uint8_t len = ((digits ? digits : 1) - 1)/7 + 1;
	position offset = pos - uintseq.begin();
	uintseq.insert(pos, len, (uint8_t) ((1<<7) | (val & 0x7f)) );
	val >>= 7;
	iterator it = uintseq.begin() + offset + 1;
	while ( val ) {
		*(it) = (uint8_t) (val & 0x7f);
		++it;
		val >>= 7;
	}
	++count;
}

bool OrderedVLUintSequence::includes(const uint64_t & key) const {
	const_iterator itr = find(key);
	return (itr != uintseq.end() && key == read(itr));
}

void OrderedVLUintSequence::add(const uint64_t & val) {
	iterator itr = uintseq.begin() + (find(val) - uintseq.begin());
	insert(itr, val);
}

uint64_t OrderedVLUintSequence::at(const position & index) const {
	const_iterator it = uintseq.begin();
	skip(it, index);
	return next(it);
}

OrderedVLUintSequence::position OrderedVLUintSequence::skip(OrderedVLUintSequence::const_iterator & pos, const OrderedVLUintSequence::position & count) const {
	position i;
	for(i = 0; i < count; ++i ) {
		if ( pos == uintseq.end() )
			return i;
		++pos;
		while ( pos != uintseq.end() && (*pos & 0x80) == 0 ) {
			++pos;
		}
	}
	return i;
}

uint64_t OrderedVLUintSequence::read(const_iterator it) const {
	return next(it);
}

uint64_t OrderedVLUintSequence::next(const_iterator & it) const {
	if ( it == uintseq.end() )
		return (uint64_t)-1;
	uint64_t rev = *it & 0x7f;
	++it;
	position len = 1;
	for ( ;it != uintseq.end() && (*it & 0x80) == 0; ++it, ++len ) {
		rev <<= 7;
		rev |= *it & 0x7f;
	}
	uint64_t val = 0;
	for ( ; len; --len ) {
		val <<= 7;
		val |= rev & 0x7f;
		rev >>= 7;
	}
	return val;
}

std::ostream & OrderedVLUintSequence::printOn(std::ostream & out) const {
	for (const_iterator it = uintseq.begin(); it != uintseq.end(); ) {
		if ( it != uintseq.begin() ) {
			std::cout << ", ";
		}
		out << (uint64_t) next(it);
	}
	out << ". ";
	return out;
}

