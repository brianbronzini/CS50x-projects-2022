#include <cs50.h>
#include <stdio.h>

/* prompts the user for their name and then prints */
int main(void)
{
    string answer = get_string("What's your name? ");
    printf("hello, %s\n", answer);
}