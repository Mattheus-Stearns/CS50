#include <cs50.h>
#include <stdio.h>
#include <string.h>

typedef struct 
{
    string name;
    string number;
} person;

int main(void)
{
    /*
    string names[] = {"David", "John", "Yulia"};
    string numbers[] = {"+1-647-495-1000", "+1-949-468-2750", "+1-647-495-1000"};

    string name = get_string("Name: ");

    for (int i = 0; i < 3; i++)
    {
        if (strcmp(names[i], name) == 0)
        {
            printf("Number: %s\n", numbers[i]);
            return 0;
        }
    }
    printf("Not found\n");
    return 1;
    */

    person people[3];

    people[0].name = "David";
    people[0].number = "+1-647-495-1000";

    people[1].name = "John";
    people[1].number = "+1-949-468-2750";

    people[2].name = "Yulia";
    people[2].number = "+1-647-495-1000";

    string name = get_string("Name: ");
    for (int i = 0; i < 3; i++)
    {
        if (strcmp(people[i].name, name) == 0)
        {
            printf("Number: %s\n", people[i].number);
            return 0;
        }
    }
    printf("Not found\n");
    return 1;
}