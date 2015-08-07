#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void Split(char *lineString, int *intPtr);
void Sort(int * arrayToSort);

const int MAX_ELEMENTS = 10;
const int MAX_LINE_LENGTH = 80;

int main(int argc, char *argv[]) {

	FILE *ifp;
	char *mode = "r";
	char line[MAX_LINE_LENGTH];
	int intArray[MAX_ELEMENTS];
	int index;

	// Opening the file
	if (argv[1] != NULL)
		ifp = fopen(argv[1], mode);
	else {
		fprintf(stderr, "Expecting a file path as parameter. None passed.\n");
		exit(1);
	}

	if (ifp == NULL) {
		fprintf(stderr, "Cant open input file passed as parameter\n");
		exit(1);
	}

	// reading the file
	while( fgets(line, MAX_LINE_LENGTH, ifp) != NULL) {

		memset(intArray, 0, sizeof(intArray));
		Split(line, intArray);

		Sort(intArray);
		
		for(index=0; index<MAX_ELEMENTS; index++ )
			fprintf(stdout, "%d\t", *(intArray+index));

		fprintf(stdout, "\n");		
	}
	
	// Closing the file
	fclose(ifp);
	return 0;
}

// Split a line into an integer array of size MAX_ELEMENTS
void Split(char * lineString, int * intPtr) {

	char * segment = lineString;
	int i=0;
	
	segment = strtok(lineString, "\t");
	while( segment != NULL && i<MAX_ELEMENTS ) {

		*(intPtr+i) = strtol(segment, NULL, 0);
		segment = strtok(NULL, "\t");
		i++;
	}
}

// Sort the array using Bubble Sort algorithm
void Sort(int * arrayToSort) {

	int i, j, temp=0;

	for( i=0; i<MAX_ELEMENTS; i++ ) {

		for( j=i+1; j<MAX_ELEMENTS; j++ ) {
			
			if ( *(arrayToSort+i) > *(arrayToSort+j) ) {
				temp = *(arrayToSort+i);
				*(arrayToSort+i) = *(arrayToSort+j);
				*(arrayToSort+j) = temp;
			}
		}		
	}
}