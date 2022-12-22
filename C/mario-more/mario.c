#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height, row, column, space;
    do

// Asks user to input block height with specified range.
    {
        height = get_int("Enter block height between 1 through 8: ");
    }
    while (height < 1 || height > 8);

    for (row = 0; row < height; row++)
    {
        for (space = 0; space < height - row - 1; space++)
        {
            printf(" ");
        }

// Checks if the condition is true. If the "column" loop is flase, then an additional "#" is printed.
        for (column = 0; column <= row; column++)
        {
            printf("#");
        }
        printf("  ");
        for (column = 0; column <= row; column++)
        {
            printf("#");
        }
        printf("\n");
    }
}