#include <cs50.h>
#include <stdio.h>

int main(int argc, string argv[])
{
    // string answer = get_string("What's your name?\n");
    // printf("hello, %s\n", answer);

    if (argc == 2)
    {
        printf("Hello, %s\n", argv[1]);
    }
    else
    {
        printf("Hello, world\n");
    }

    for (int i = 0; i < argc; i++)
    {
        printf("%s\n", argv[i]);
    }
    
}