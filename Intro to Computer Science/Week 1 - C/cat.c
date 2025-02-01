#include <stdio.h>
#include <cs50.h>

void meow(int n);
int get_positive_integer(void);

int main(void)
{   
    int i = 0;
    while (i < 3)
    {
        meow(1);
        i++;
    }

    int times = get_positive_integer();
    meow(times);

}

int get_positive_integer(void)
{
    int n;

    do
    {
        n = get_int("Number: ");
    } while (n < 1);
    
    return n;
}

void meow(int times)
{
    for (int i = 0; i < times; i++)
    {
        printf("meow\n");
    }
}