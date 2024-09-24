// list.h 

#ifndef LIST_H
#define LIST_H

// Define the Node structure
typedef struct NodeObj* Node;

// Define the List structure
typedef struct ListObj* List;

// Function prototypes for List ADT

// Creates a new empty List and returns a pointer to it
List newList();

// Frees all memory associated with the List
void freeList(List* pL);

// Moves the cursor to the front of the List
void moveFront(List L);

// Moves the cursor to the back of the List
void moveBack(List L);

// Moves the cursor one step towards the front of the List
void movePrev(List L);

// Moves the cursor one step towards the back of the List
void moveNext(List L);

// Returns the index of the cursor element, or -1 if undefined
int index(List L);

// Returns the cursor element
int get(List L);

// Inserts a new element before the cursor
void insertBefore(List L, int data);

// Inserts a new element after the cursor
void insertAfter(List L, int data);

// Deletes the cursor element
void delete(List L);

// Concatenates two lists and returns a new List
List concatList(List A, List B);

// Additional utility functions as needed...

#endif // LIST_H