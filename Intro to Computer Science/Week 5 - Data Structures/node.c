#include <stdio.h>
#include <stdlib.h>

int numbers[3];

typedef struct node
{
    int number;
    struct node *next;
} node;

int main(void)
{
    node *list = NULL;
    int numbers[] = {1, 2, 3};

    for (int i = 0; i < 3; i++)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            // TODO: Free any memory already malloc'd
            return 1;
        }
        n->number = numbers[i];
        n->next = NULL;

        /* problem is that this makes it backwards i.e. stacking the list and, printing left to right across the list would result in 3, 2, 1
        n->next = list;

        list = n;
        */

        // Now appending items to the list, so that now printing from left to right across the list would result in 1, 2, 3

        // If list is empty
        if (list == NULL)
        {
            list = n;
        }

        // If list has numbers already
        else
        {
            for (node *ptr = list; ptr != NULL; ptr = ptr->next)
            {
                // If at end of list
                if (ptr->next == NULL)
                {
                    ptr->next = n;
                    break;
                }


            }
        }
    }

    // Time passes

    /* This is for when the list is "stacked"
    node *ptr = list;
    while (ptr != NULL)
    {
        printf("%i\n", ptr->number);
        ptr = ptr->next;
    }
    */

    // advantage of stacking the list is this: O(1) for insertion
    // sadly, stacking the list has O(n) for searching

    for (node *ptr = list; ptr != NULL; ptr = ptr->next)
    {
        printf("%i\n", ptr->number);
    }
    
    // with FIFO, and the implementation that we used to get there, now we also have O(n) for insertion :(

    // Time passes

    node *ptr = list;
    while (ptr != NULL)
    {
        node *next = ptr->next;
        free(ptr);
        ptr = next;
    }

    return 0;
}