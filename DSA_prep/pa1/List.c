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