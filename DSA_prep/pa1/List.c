#include <stdio.h>
#include <stdlib.h>
#include "List.h"

// Node structure
struct NodeObj {
    int data; // in order to store current value 
    Node prev; // to traverse backwards
    Node next; // to traverse forwards
};

// List structure
struct ListObj {
    Node front; // used to go to the first node in the list 
    Node back; // used to go to the last node in the list
    Node cursor; // pointer to "current" node in list 
    int length; // stores number of nodes in the list
    int index; // stored index of node currently under cursor
    // ** if cursor is undef, we set to -1
};


// CONSTRUCTOR: Creating a new list
List newList(void) {
    List L = malloc(sizeof(struct ListObj));
    L->front = NULL;
    L->back = NULL; 
    L->cursor = NULL;
    L->length = 0; 
    L->index = -1;
    return L;
}


// DESTRUCTOR: Freeing the list
void freeList(List* pL) {
    if (pL != NULL && *pL != NULL) {
        // Freeing all nodes 
        Node current = (*pL)->front;
        while (current != NULL) {
            Node temp = current;
            current = current->next;
            free(temp);
        }
        free(*pL);
        *pL = NULL;
    }
}


// ** ACCESS FUNCTIONS **

// returns the number of elements in the list
int length (List L) {
    return L->length;
}

// returns the current position that the index is on
int index (List L) {
    return L->index;
}

// returns front element of L
int front (List L) {
    // Checking validity of list
    if (L == NULL || L->length == 0) {
        fprintf(stderr, "List Error: calling front() on NULL or empty List\n");
        exit(EXIT_FAILURE);
    }
    // Positioning cursor to front
    L->cursor = L->front; 
    L->index = 0; // Setting idex to 0
    return L->front->data;
}

// returns back element of L 
int back (List L) {
    // Checking validity 
    if (L == NULL || L->length == 0) {
        fprintf(stderr, "List Error: calling back on NULL or empty List\n");
        exit(EXIT_FAILURE);
    }
    // Positioining cursor to back of list
    L->cursor = L->back;
    L->index = L->length -1; // Setting index to -1 (last element of list)
    return L->back->data;
}

// returns cursor element of L
int get (List L) {
    if (L == NULL || L->length == 0 || L->cursor == NULL || L->index < 0) {
        fprintf(stderr, "List Error: calling get() on undefined cursor or invalid List\n");
        exit(EXIT_FAILURE);
    }
    return L->cursor->data;
}




// Returns true iff Lists A and B contain the same
// sequence of elements, returns false otherwise.
bool equals(List A, List B) {
    // Checking if both lists are the same object
    if (A == B) {
        return true;
    }
    
    // checking if either list is NULL
    if (A == NULL || B == NULL) {
        return false;
    }

    // checking if lenths are different
    if (A->length != B->length) {
        return false;
    }

    // Comparing elements node by node

    // Initializes to front of the node
    Node nodeA = A->front;
    Node nodeB = B->front;

    // iterating throygh nodes given conditions
    while (nodeA != NULL && nodeB != NULL) {
        if (nodeA->data != nodeB->data) {
            return false;
        }
        // after conditionals, we iterate and progress the list
        nodeA = nodeA->next;
        nodeB = nodeB->next;
    }

    // passes above conditions and lists are identical
    return true;
}


// ** MANIPULATION PROCEDURES **

// Resets L to its original empty state.
void clear(List L) {
    // working on this
}