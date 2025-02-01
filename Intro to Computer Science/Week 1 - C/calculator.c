#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int x = get_int("x: ");
    int y = get_int("y: ");

    printf("x + y = %i\n", x + y);
    printf("2x = %i\n", x * 2);
    printf("x / y = %.50f\n", (double) x / y);

    long int dollars = 1;
    while(true)
    {
        char c = get_char("Here's $%li. Double it and give it to the next person? ", dollars);
        if (c == 'y')
        {
            dollars *= 2;
        }
        else
        {
            break;
        }

    }
    printf("Here's $%li.\n", dollars);
}