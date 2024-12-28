
List.h : 



List.c : 

understanding the difference between index and cursor was troubling at first. Index is the numbering system relative to the length of the list & cursor is the specific element that the cursor is pointing to currently.

Another important error that I caught was using -1 and L->length -1 in back() function. It was important to remember that we want to reference the last element in the list. -1 refers to an undefined value
