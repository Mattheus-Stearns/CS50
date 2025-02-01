#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int get_points(string s);

int main(void)
{
    string player1 = get_string("Player 1: ");
    string player2 = get_string("Player 2: ");

    if (get_points(player1) > get_points(player2))
    {
        printf("Player 1 wins!\n");
    }
    else if (get_points(player1) < get_points(player2))
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

    return 0;
}

int get_points(string s)
{
    int counter = 0;
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (islower(s[i]))
        {
            s[i] = toupper(s[i]);
        }

        switch (s[i])
        {
            case 'A':
                counter += 1;
                break;
            case 'B':
                counter += 3;
                break;
            case 'C':
                counter += 3;
                break;
            case 'D':
                counter += 2;
                break;
            case 'E':
                counter += 1;
                break;
            case 'F':
                counter += 4;
                break;
            case 'G':
                counter += 2;
                break;
            case 'H':
                counter += 4;
                break;
            case 'I':
                counter += 1;
                break;
            case 'J':
                counter += 8;
                break;
            case 'K':
                counter += 5;
                break;
            case 'L':
                counter += 1;
                break;
            case 'M':
                counter += 3;
                break;
            case 'N':
                counter += 1;
                break;
            case 'O':
                counter += 1;
                break;
            case 'P':
                counter += 3;
                break;
            case 'Q':
                counter += 10;
                break;
            case 'R':
                counter += 1;
                break;
            case 'S':
                counter += 1;
                break;
            case 'T':
                counter += 1;
                break;
            case 'U':
                counter += 1;
                break;
            case 'V':
                counter += 4;
                break;
            case 'W':
                counter += 4;
                break;
            case 'X':
                counter += 8;
                break;
            case 'Y':
                counter += 4;
                break;
            case 'Z':
                counter += 10;
                break;
            default:
                counter += 0;
                break;
        }
    }

    return counter;
}