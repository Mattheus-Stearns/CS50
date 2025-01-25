#include <stdio.h>
#include <cs50.h>

int main(int argc, string argv[]) 
{
    if (argc != 2)
    {
        printf("Usage: ./status <Input>\n");
        return 1;
    }
    printf("hello, %s\n", argv[1]);
    return 0;
}