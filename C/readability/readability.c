#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int main(void)
{
    string text = get_string("Input some text: ");
    int countletter = 0;
    int countword = 1;
    int countsentence = 0;

    // counts the # of letters, words, and sentences.
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
       {
           countletter++;
       }
       else if (text[i] == ' ')
       {
           countword++;
       }
       else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
       {
           countsentence++;
       }
    }

    // prints the # of letters, words, and sentences.
    // printf("%i letters\n%i words\n%i sentences\n", countletter, countword, countsentence);

    // Calc uses the Coleman-Liau index formula to determine grade level.
    float grade = 0.0588 * (100 * (float) countletter / (float) countword) - 0.296 * (100 * (float) countsentence / (float) countword) - 15.8;

    // prints the grade level per the input text.
    if (grade < 16 && grade >= 0)
    {
        printf("Grade %i\n", (int) round(grade));
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Before Grade 1\n");
    }
}