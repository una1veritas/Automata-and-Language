//==========================================
// ahodawg.h
//==========================================

#ifndef AHODAWG_H_
#define AHODAWG_H_

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <deque>
//#include <time.h>
//#include <chrono>

#include <cinttypes>

#include "ACMachine.h"
#include "dawg.h"

class AhoDawg {
private:
	ACMachine ac;
	DAWG da;



public:
	AhoDawg(void);

	typedef uint32 state;
	typedef uint16 alphabet;

	
	template <typename C>
	void BuildAhoandDawg(const C & strset){
		ac.addPatterns(strset);
		da.buildingdawg(strset);
	}
	

	//template <typename T>
	  //void BuildAhoandDawg(const T strset[]);

	//template <typename T>
	  //void BuildAhoandDawg(const T & strset);


	int statesize() {
		return ac.statesize();
	}


	//template <typename T>
	  //void DynamicBAD(const T & strset);

	//template <typename T>
	  //void DynamicBAD(const T strset[]);

	
	template <typename C>
	  //void DynamicBAD(const C & strset){
	void DynamicBAD(const C & str) {
		  //std::cout << strset << std::endl;
	  //for(auto str : strset){
	    //std::cout << "dynamic bad" << std::endl;
	    //std::cout << str << std::endl;

	    int position;
	    position = ac.searchstateposition(str);

	    //std::cout << "check1" << std::endl;

	    ac.addPath(str);
	    ac.addOutput(str);

	    //std::cout << "check2" << std::endl;
		
	    std::vector<DAWG::fstates> failstates;
	    //firststate: from /secondstate: to
	    failstates = da.getFailStates(position, str);
	    //std::cout << "check2.5" << std::endl;
	    ac.addfailurestates(failstates, str);

	    //std::cout << "check3" << std::endl;

	    ac.addFailure(position, str);

	    //std::cout << "check4" << std::endl;

	    std::vector<DAWG::state> outstates;
	    outstates = da.getOutStates(str);
	    ac.addoutstates(outstates, str);

	    //std::cout << "check5" << std::endl;

	    da.builddawg(str);

	    //std::cout << "check6" << std::endl;
	  //}
	}
	

};

typedef AhoDawg ahdawg;

#endif 
