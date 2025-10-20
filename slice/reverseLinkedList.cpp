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
