#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

bool checksum(char* n);

char* issuer(char* n);

bool is_numeric(string n)
{
    for (int i = 0, len = strlen(n); i < len; i++)
    {
        if (!isdigit(n[i]))
        {
            return false;
        }
    }
    return true;
}

int main(void)
{
    string n;
    int lengthN;
    do 
    {
        n = get_string("Number: ");
        lengthN = strlen(n);
    } while (!is_numeric(n));

    bool result = checksum(n);
    
    if (result == true)
    {
        printf("%s", issuer(n));
    }
    else
    {
        printf("INVALID\n");
    }

    
}

bool checksum(char* n)
{
    int lengthN = strlen(n);
    int checksum = 0;
    
    for (int i = lengthN - 1; i >= 0; i -= 2)
    {
        checksum += n[i] - '0';
        if (i > 0)
        {
            int doubleNum = (n[i - 1] - '0') * 2;
            checksum += doubleNum / 10 + doubleNum % 10;
        }
    }

    if (lengthN != 13 && lengthN != 15 && lengthN != 16)
    {
        return false;
    }  
    else if (checksum % 10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

char* issuer(char* n)
{
    char twoDigitStr[3] = {n[0], n[1], '\0'};
    int twoDigitIdentifier = atoi(twoDigitStr);
    int oneDigitIdentifier = n[0] - '0';  // Directly convert char to int
    int lengthN = strlen(n);

    if ((twoDigitIdentifier == 34 || twoDigitIdentifier == 37) && lengthN == 15)
    {
        return "AMEX\n";
    }
    else if (twoDigitIdentifier > 50 && twoDigitIdentifier < 56 && lengthN == 16)
    {
        return "MASTERCARD\n";
    }
    else if (oneDigitIdentifier == 4 && (lengthN == 13 || lengthN == 16))
    {
        return "VISA\n";
    }
    else
    {
        return "INVALID\n";
    }

}