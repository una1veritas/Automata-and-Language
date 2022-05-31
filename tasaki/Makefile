
CC	= /opr/local/bin/gcc -std=c99
CFLAGS = -Wall -g -O2

CXX = /opt/local/bin/g++ -std=c++17
CXXFLAGS = -Wall -g -O2

INCDIRS = -I./ -I/usr/local/include

INCLUDES = 
OBJS = main.o commandargs.o xbw.o ACMachine.o
LIBS = -L/usr/local/lib -lsdsl 
TARGET = acm.exe


%.o: %.c $(INCLUDES)
	$(CC) $(CCFLAGS) $(INCDIRS) -c $<

%.o: %.cpp $(INCLUDES)
	$(CXX) $(CXXFLAGS) $(INCDIRS) -c $<


$(TARGET):	$(OBJS) $(INCLUDES)
	$(CXX) -o $(TARGET) $(OBJS) $(LIBS)

all: $(TARGET)

clean:
	\rm -f $(OBJS)