// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Step 3 - Choose number of buckets in hash table
const unsigned int N = 100000;

// Hash table
node *table[N]; // Array of node pointers that if index is NULL, new_n is placed into index (e.g., [_, new_node, _, ...])

// Initialize word count
int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO: Step 5
    int h = hash(word); // Hash word to obtain hash index

    node *cursor = table[h]; // Access linked list at hash index

    // Traverse linked list for (strcasecmp)
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0) // Checks if strings match
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Step 2 - Improve this hash function
    long sum = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        sum += tolower(word[i]); // Converts words to lowercase
    }
    return (sum % N);
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO: Step 1
    // Open dictionary
    FILE *dict = fopen(dictionary, "r");

    if (dictionary == NULL)
    {
        printf("Cannot open %s\n", dictionary);
        return false;
    }

    // Declare buffer array 'char word[]'
    // Length of max word in dictionary '[LENGTH + 1]'
    char next_w[LENGTH + 1];
    // Read one word at a time in dictionary
    while (fscanf(dict, "%s", next_w) != EOF) // fscanf returns EOF once it reaches end of file
    {
        // Create a node
        node *new_n = malloc(sizeof(node)); // populates new node into index (line 25)
        if (new_n == NULL)
        {
            return false;
        }

        // Copy or 'store' word to new_n
        strcpy(new_n->word, next_w);
        new_n->next = NULL;

        // Hash word to obtain hash value
        int h = hash(next_w);

        new_n->next = table[h];
        table[h] = new_n;
        word_count++; // Increments when new_n is added to data structure
    }

    // Close file
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO: Step 4 - Return word count in dictionary if loaded, else 0 if not loaded
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO: Step 6 - Free memory from linked list
    for (int i = 0; i < N; i++) // Iterate through each linked list
    {
        node *head = table[i];
        node *cursor = head;
        node *tmp = head;

        while (cursor != NULL)
        {
            cursor = cursor->next; // Advances cursor to next list
            free(tmp);
            tmp = cursor; // Moves 'tmp' variable with cursor to the next list
        }
    }
    return true; // Returns successful release of memory from unload function
}
