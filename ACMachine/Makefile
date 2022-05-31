
CC	= gcc -std=c99
CFLAGS = -Wall -g -O2

CXX = g++ -std=c++11
CXXFLAGS = -Wall -g -O2

INCDIRS = -I./

INCLUDES = ACMachine_varray.h
OBJS = ACMachine_varray.o cmdargs.o main_varray.o
LIBS = 
TARGET = acm.exe


%.o: %.c $(INCLUDES)
	$(CC) $(CCFLAGS) $(INCDIRS) -c $<

%.o: %.cpp $(INCLUDES)
	$(CXX) $(CXXFLAGS) $(INCDIRS) -c $<


$(TARGET):	$(OBJS) $(INCLUDES)
	$(CXX) -o $(TARGET) $(OBJS) $(LIBS)

all: $(TARGET)

clean:
	rm -f *.o $(TARGET) *~
