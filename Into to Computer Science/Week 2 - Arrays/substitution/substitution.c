#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[]) 
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    
    
    int keyLength = strlen(argv[1]);
    if (keyLength != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
        
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(argv[1][i]))
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }
    }

    for (int i = 0; i < 26; i++)
    {
        for (int j = i + 1; j < 26; j++)
        {
            if (argv[1][i] == argv[1][j])
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }
    

    string plaintext = get_string("plaintext: ");
    int plaintextLength = strlen(plaintext);
    char ciphertext[plaintextLength + 1];

    for (int i = 0; i < plaintextLength; i++)
    {
        if (isalpha(plaintext[i]))
        {
            if (isupper(plaintext[i]))
            {
                ciphertext[i] = toupper(argv[1][plaintext[i] - 65]);
            } else if (islower(plaintext[i]))
            {
                ciphertext[i] = tolower(argv[1][plaintext[i] - 97]);
            }
        } else
        {
            ciphertext[i] = plaintext[i];
        }
    }

    ciphertext[plaintextLength] = '\0';

    printf("ciphertext: %s\n", ciphertext);

    return 0;
}