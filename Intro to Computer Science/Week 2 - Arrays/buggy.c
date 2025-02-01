#include <stdio.h>
#include <cs50.h>

void print_column(int h);

int main(void)
{
    for (int i = 0; i < 3; i++)
    {
        printf("i is %i\n", i); // used for debugging
        printf("#\n");
    }

    int h = get_int("Height: ");
    print_column(h);
}

void print_column(int h)
{
    for (int i = 0; i < h; i++)
    {
        printf("#\n");
    }
}