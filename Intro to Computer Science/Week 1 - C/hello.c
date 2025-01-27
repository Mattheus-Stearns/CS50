#include <stdio.h>
#include <cs50.h>

int main(void)
{
    printf("hello, world!\n");

    string answer = get_string("What's your name? ");
    printf("hello, %s!\n", answer);

}

// code XXX.c = makes a file named XXX.c but can be any type of file
// make XXX = compiles
// ./XXX = runs the code that was compiled
