TARGET = all

CC = gcc -Wall 
CXX = g++ -std=c++17 -Wall 

CFLAGS += -O2 

DFAOBJS = dfa.o
NFAOBJS = nfa.o

EXECUTABLE = dfa.exe nfa.exe

all:	$(EXECUTABLE)

dfa.exe:	$(DFAOBJS)
	$(CXX) -o $@ $^

nfa.exe:	$(NFAOBJS)
	$(CXX) -o $@ $^

%.o:	%.cpp 
	$(CXX) -c $(CFLAGS) $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

%.o:	%.c
	$(CC) -c $(CFLAGS) $(CPPFLAGS) -o $@ $<

clean:
	rm -fr $(EXECUTABLE) $(DFAOBJS) $(NFAOBJS)
	rm -f *~
