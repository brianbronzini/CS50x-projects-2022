#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // Check for one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    // Checks that only alphabet characters are used
    // 'key' string picks up the first argument 'argv[1]'
    // '0' starts from the first character of the string
    string key = argv[1];
    for (int i = 0; i < strlen(key); i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Usage: ./substitution key\n");
            return 1;
        }
    }
    // Check that string 'key' consists of 26 characters
    // Note that 'return; 1' terminates the program
    if (strlen(key) != 26)
    {
        printf("Your key must contain 26 characters.\n");
        return 1;
    }
    // Check that string 'key' contains only unique characters with a nested loop
    for (int i = 0; i < strlen(key); i++)
    {
        for (int j = i + 1; j < strlen(key); j++)
        {
            if (toupper(key[i]) == toupper(key[j]))
            {
                printf("Usage: ./substitution key\n");
                return 1;
            }
        }
    }

    // prompt user for plaintext
    string plaintext = get_string("plaintext: ");

    // Convert alphabet to uppercase
    for (int i = 0; i < strlen(key); i++)
    {
        if (islower(key[i]))
        {
            key[i] = key[i] - 32;
        }
    }

    // print ciphertext
    printf("ciphertext: ");

    // Check position of plaintext letter per ASCII uppercase and lowercase
    // 'printf("%c", key[letter] + 32);' converts alphabet back to lowercase
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isupper(plaintext[i]))
        {
            int letter = plaintext[i] - 65;
            printf("%c", key[letter]);
        }
        else if (islower(plaintext[i]))
        {
            int letter = plaintext[i] - 97;
            printf("%c", key[letter] + 32);
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
}