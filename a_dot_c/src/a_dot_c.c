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
	char * p = argv[1];

	if ( *p == 'a' )
		goto state_asterisk;
	puts("reject!");
	return -1;

	state_asterisk:
	++p;
	if ( *p == '.' ) {
		++p;
		goto state_dot;
	}
	if ( *p == (char) 0 ) {
		puts("reject!");
		return -1;
	}
	goto state_asterisk;

	state_dot:
	if ( *p == 'c' )
		goto state_c;
	goto state_asterisk;

	state_c:
	++p;
	if ( *p == (char) 0 )
		goto accept;
	goto state_asterisk;

	accept:
	puts("accept!\n");
	return 0; // finished with no errors.
}
