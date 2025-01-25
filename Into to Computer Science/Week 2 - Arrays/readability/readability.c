#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int numofWords(string s);
float averageNumofLetters(string s);
float averageNumofSentences(string s);

int main(void)
{
    string text = get_string("Text: ");
    float L = averageNumofLetters(text);
    float S = averageNumofSentences(text);
    float grade = 0.0588 * L - 0.296 * S - 15.8;
    int index = (int) round(grade);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int numofWords(string s)
{
    int words = 0;
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (isspace(s[i]))
        {
            words++;
        }
    }
    words++;

    return words;
}

float averageNumofLetters(string s)
{
    int letters = 0;
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (isalpha(s[i]))
        {
            letters++;
        }
    }

    return 100.0 * letters / numofWords(s);
}

float averageNumofSentences(string s)
{
    int sentences = 0;
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (s[i] == '.' || s[i] == '!' || s[i] == '?')
        {   
            if (i + 1 < n) {
                if (s[i + 1] != '.')
                {
                    sentences++;
                }
            }
            else
            {
                sentences++;
            }
        }
    }
    
    return 100.0 * sentences / numofWords(s);
}