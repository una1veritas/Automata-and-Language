//==========================================
// ahodawg.cpp
//==========================================

//#include <deque>
//#include <cctype>

#include "ACMachine.h"
#include "dawg.h"
#include "ahodawg.h"


AhoDawg::AhoDawg(void){
	;
}

/*
template <typename T>
void AhoDawg::BuildAhoandDawg(const T strset[]){
  const std::string s(strset);
  return BuildAhoandDawg(s);
}

template <typename T>
void AhoDawg::BuildAhoandDawg(const T & strset){
  ac.addPatterns(strset);
  da.buildingdawg(strset);
}

template void AhoDawg::BuildAhoandDawg<char>(const char patt[]);
template void AhoDawg::BuildAhoandDawg<std::string>(const std::string & patt);
*/

/*
template <typename T>
void AhoDawg::DynamicBAD(const T strset[]){
  const std::string s(strset);
  return DynamicBAD(s);
}
*/

/*
template <typename T>
void AhoDawg::DynamicBAD(const T str[]){
  const std::string s(str);
  return DynamicBAD(s);
}
*/

/*
template <typename T>
void AhoDawg::DynamicBAD(const T & strset){
  for(auto str : strset){
    //std::cout << "dynamic bad" << std::endl;

    int position;
    position = ac.searchstateposition(str);

    ac.addPath(str);
    ac.addOutput(str);

    std::vector<DAWG::fstates> failstates;
    //firststate: from /secondstate: to
    failstates = da.getFailStates(position, str);
    ac.addfailurestates(failstates, str);

    ac.addFailure(position, str);

    std::vector<DAWG::state> outstates;
    outstates = da.getOutStates(str);
    ac.addoutstates(outstates, str);

    da.builddawg(str);
  }
}

//template void AhoDawg::DynamicBAD<char>(const char patt[]);
template void AhoDawg::DynamicBAD<std::string>(const std::string & patt);
*/
