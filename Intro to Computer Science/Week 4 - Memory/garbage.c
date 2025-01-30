#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int scores[1024];
    for (int i = 0; i < sizeof(scores); i++)
    {
        printf("%i\n", scores[i]);
    }

    int *x;
    int *y;

    x = malloc(sizeof(int));

    *x = 42;
    *y = 13; // definately causes a crash :) – This is because of the lack of making space for the pointer
    printf("somehow didnt crash?\n");

    y = x;
    *y = 13;
}