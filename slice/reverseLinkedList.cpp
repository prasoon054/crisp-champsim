// { Driver Code Starts
// Initial Template for C++// C program to find n'th Node in linked list
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
using namespace std;

/* Link list Node */
struct Node {
    int data;
    struct Node *next;
    Node(int x) {
        data = x;
        next = NULL;
    }
};

// } Driver Code Ends
/* Linked List Node structure:

struct Node
{
    int data;
    struct Node *next;
}

*/

class Solution {
  public:
    // Function to reverse a linked list.
    //  Iterative approach
    struct Node *reverseList1(struct Node *head) {
        // code here
        // return head of reversed list
        Node *current = head;
        Node *prev = NULL;
        Node *next = current->next;
        while (current != NULL) {
            next = current->next;
            current->next = prev;
            prev = current;
            current = next;
        }
        return prev;
    }

    // Recursive approach using similar concept to while loop
    Node *recursion(Node *cur, Node *prev) {
        auto next = cur->next;
        cur->next = prev;
        if (!next)
            return cur;
        return recursion(next, cur);
    }

    // Recursive (another approach)
    struct Node *reverseList(struct Node *head) {
        // as recursive for every head the recursion
        // reaches the end of the linked list thus rest
        // always contains the last element(the new head).
        // But for every recursion call the head next place
        // thus we have to transfer the head to the head's
        // next to next place and then the head is severed
        // from the link list by putting NULL in its next.
        // Ex:
        // 1 2 3 4 5 6
        // recursion call reaches to the last and where the node
        // with 6 is returned back to the call where head is 5
        // now we store 5 in 5's next to next place. i.e. 5->6->5
        // and now we severe the head from this new link by
        // head->next=NULL, thus now we have linked list as
        // 6->5.
        // On careful observation we notice that this 5 is linked to
        // two nodes one is 6 the other is 4, as we know 4's next is
        // 5. Thus the complete linked list is
        // 6->5<-4<-3<-2<-1         ------------------------------I
        // Now 4 had previously called 4->next i.e. 5, thus now again
        // the same occurs here for this call 4 is the head.
        // Thus 4->5->4 which after severing becomes 5->4,
        // thus making the overall linked list as 5->4<-3<-2<-1
        // Also from I we know 5 is also the next of 6, thus the
        // complete linked list is:
        // 6->5->4<-3<-2<-1         -----------------------------II
        // In II we observe that now 4 is next of both 5 and 3.
        // Same procedure occurs until the complete linked list is
        // reversed. And also at all times the rest contains the 6,
        // which is the new head.
        if (head->next == NULL)
            return head;
        Node *rest = reverseList(head->next);
        head->next->next = head;
        head->next = NULL;
        return rest;
    }

    // Also can use stack method to reverse , see 2reverseInGroup.cpp for that
    // method.
};

// { Driver Code Starts.

void printList(struct Node *head) {
    struct Node *temp = head;
    while (temp != NULL) {
        printf("%d ", temp->data);
        temp = temp->next;
    }
}

/* Driver program to test above function*/
int main() {
    Node *head = new Node(1);
    Node *cur = head;
    int i = 0, e = 0;
    // Create link list of random single digit numbers of size 10^6
    while (i++ < 1e5) {
        e = rand() % 10;
        Node *newNode = new Node(e);
        cur->next = newNode;
        cur = cur->next;
    }
    Solution ob;
    head = ob.reverseList(head);
    printList(head);
    return 0;
}

// } Driver Code Ends
