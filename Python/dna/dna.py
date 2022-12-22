# Import necessary modules
from sys import argv, exit


def main():

    # TODO: Check for command-line usage
    if len(argv) != 3:
        print("Error: please check arguments and run again")
        exit(1)

    # TODO: Read database file into a variable
    csv_f = open(argv[1], "r")

    segments = []  # Create an array for all strands
    people = {}  # Create an object for all people
    for i, row in enumerate(csv_f):  # Enumerate object to track iterations of the loop
        if i == 0:  # First row
            segments = [segment for segment in row.strip().split(',')][1:]
        else:
            at_row = row.strip().split(',')
            people[at_row[0]] = [int(j) for j in at_row[1:]]  # Gets name at current row [0] and onward using slice operator '1:'

    # TODO: Read DNA sequence file into a variable
    txt_f = open(argv[2], "r").read()

    # TODO: Find longest match of each STR in DNA sequence
    seg_final = []
    for segment in segments:
        n = 0
        seg_max = -1
        highest = 0

        # Iterate to glide viewer across matching segments of the sequence
        while n < len(txt_f):
            viewer = txt_f[n:n+len(segment)]
            if viewer == segment:
                highest += 1
                seg_max = max(seg_max, highest)
                n += len(segment)
            else:
                highest = 0
                n += 1
        seg_final.append(seg_max)

    # TODO: Check database for matching profiles
    for name, seq in people.items():
        if seq == seg_final:
            print(name)
            exit(0)
    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
