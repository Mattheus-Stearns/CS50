#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int num;
    do
    {
        num = get_int("How high do yah like your pyramids, luigi? ");
    }while (num < 1 || num > 8);

    for (int row = 0; row < num; row++)
    {
        // Print leading spaces
        for (int space = 0; space < num - row - 1; space++)
        {
            printf(" ");
        }

        // Print left side of the pyramid
        for (int col = 0; col <= row; col++)
        {
            printf("#");
        }

        // Print gap between the two sides
        printf("  ");

        // Print right side of the pyramid
        for (int col = 0; col <= row; col++)
        {
            printf("#");
        }

        // Move to the next line
        printf("\n");
    }

}
