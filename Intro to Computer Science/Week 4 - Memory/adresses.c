#include <cs50.h>
#include <stdio.h>

int main(void)
{
    
    int n = 50;
    int *p = &n;
    printf("%d\n", *p);


    string s = "HI!";
    printf("%p\n", s);
    printf("%p\n", &s[0]);
    printf("%p\n", &s[1]);
    printf("%p\n", &s[2]);
    printf("%p\n", &s[3]);

    char *t = "HI!";
    printf("%s\n", t);

    printf("%c\n", t[0]);
    printf("%c\n", t[1]);
    printf("%c\n", t[2]);

    printf("%c\n", *t);
    printf("%c\n", *(t + 1));
    printf("%c\n", *(t + 2));
}
