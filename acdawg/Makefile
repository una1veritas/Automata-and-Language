#Makefile
# Created on: 2017/01/19
#     Author: sin


CXX = g++ -std=c++11
CXXFLAGS = -Wall -O2 -g3
INCDIRS = -I./

HEADERS = dawg.h actrie.h

%.o: %.c  $(HEADERS)
	$(CC) $(CCFLAGS) -c $<

%.o: %.cpp  $(HEADERS)
	$(CXX) $(CXXFLAGS) -c $<

#
LIBOBJS = actrie.o dawg.o

all: acdawg

acdawg:  main.o $(LIBOBJS) $(HEADERS)
	$(CXX) $(CXXFLAGS) $(INCDIRS) -o acdawg.exe main.o $(LIBOBJS)

ac: aho.o $(LIBOBJS) $(HEADERS)
	$(CXX) $(CXXFLAGS) $(INCDIRS) -o ac.exe aho.o $(LIBOBJS)


clean: 
	rm -rf *.o *.exe *.dSYM #*# *~
