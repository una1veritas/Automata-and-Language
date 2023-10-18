TARGET = all

CC = gcc -Wall 
CXX = g++ -std=c++17 -Wall 

CFLAGS += -O2 

DFAOBJS = dfa.o
NFAOBJS = nfa.o

EXECUTABLE = dfa.exe 

all:	$(EXECUTABLE)

dfa.exe:	$(DFAOBJS)
	$(CC) -o $@ $^

nfa.exe:	$(NFAOBJS)
	$(CC) -o $@ $^

%.o:	%.cpp 
	$(CXX) -c $(CFLAGS) $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

%.o:	%.c
	$(CC) -c $(CFLAGS) $(CPPFLAGS) -o $@ $<

clean:
	rm -fr $(EXECUTABLE) $(DFAOBJS) $(NFAOBJS)
	rm -f *~
