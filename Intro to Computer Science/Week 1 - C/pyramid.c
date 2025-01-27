#include <stdio.h>
#include <cs50.h>

void print_row(int n);
void print_pyramid(int n);

int main(void)
{
    const int n = 3;
    
    for (int i = 0; i < 4; i++)
    {
        printf("?");
    }
    printf("\n");

    for (int i = 0; i < n; i++)
    {
        printf("#\n");
    }

    print_row(n);

    int num;
    do
    {
        num = get_int("How high do yah like your pyramids, luigi? ");
    }while (num < 0 && num > 9);
    
    print_pyramid(num);
}

void print_row(int n)
{
    for (int row = 0; row < n; row++)
    {
        for (int col = 0; col < 3; col++)
        {
            printf("#");
        }
        printf("\n");
    }
}

void print_pyramid(int num)
{
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