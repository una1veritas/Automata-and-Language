/*
 ============================================================================
 Name        : pattern_matching_program.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char * argv[]) {
	if (argc < 2 ) {
		puts("Give me an input string!\n");
		return -1; // error occurred.
	}
	char * p = argv[1];

	if ( *p++ != 'a' )
		return -1; // reject

loop_asterisk:
	if ( *p++ != '.' )
		goto loop_asterisk;
	if ( *p++ != 'c' )
		goto loop_asterisk;
	if ( *p++ != (char) 0 )
		goto loop_asterisk;

	puts("Accept!\n");
	return 0; // finished with no errors.
}
