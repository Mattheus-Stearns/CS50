#include <stdio.h>

void swap(int *a, int *b);

int main(void)
{
    int x = 1;
    int y = 2;
    
    printf("x is %i, y is %i\n", x, y);
    swap(&x, &y);
    printf("x is %i, y is %i\n", x, y);
}

void swap(int *a, int *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

/*

A representation of the stack (from bottom to top):

[swap]
[main]

More specific:

[a = 1, b = 2, tmp = 1] => [a = 2, b = 1, tmp = 1] (swap)
[x = 1, y = 2] (main)

This is what we are doing, passing by reference:

void swap(int a, int b)
{
    int tmp = a;
    a = b;
    b = tmp;
}

What we want to do is pass by value... :

void swap(int *a, int *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

This connects the higher value of the stack with the thing that is below it;...
*/