#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // TODO
    // Loop for candidate count
    for (int i = 0; i < candidate_count; i++)
    {
        // Comparison checks that user's vote is similar to candidate
        if (strcmp(candidates[i].name, name) == 0)
        {
            // If similar, then increase vote
            candidates[i].votes++;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // TODO
    // Declare variable for vote limit
    int vote_limit = 0;

    // Iterate through candidate list and test if the # of votes is greater than the maximum
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > vote_limit)
        {
            vote_limit = candidates[i].votes;
        }
    }

    // Iterate through candidate list and test if the # of votes is equal to the maximum
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes == vote_limit)
        {
            printf("%s\n", candidates[i].name);
        }
    }
}