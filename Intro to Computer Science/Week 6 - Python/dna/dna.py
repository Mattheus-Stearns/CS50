import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Error: Invalid amount of Command Line Arguments")
        return
    # TODO: Read database file into a variable
    databaseFile = open(sys.argv[1], "r")
    reader = csv.DictReader(databaseFile)
    str_sequences = reader.fieldnames[1:]  # Exclude the 'name' field
    database = list(reader)
    databaseFile.close()
    # TODO: Read DNA sequence file into a variable
    dnaSequenceFile = open(sys.argv[2], "r")
    dna_sequence = dnaSequenceFile.read().strip()
    dnaSequenceFile.close()
    # TODO: Find longest match of each STR in DNA sequence
    str_matches = {}
    for str_seq in str_sequences:
        str_matches[str_seq] = longest_match(dna_sequence, str_seq)
    # TODO: Check database for matching profiles
    for person in database:
        match = True
        for str_seq in str_sequences:
            if int(person[str_seq]) != str_matches[str_seq]:
                match = False
                break
        if match:
            print(person["name"])
            return

    print("No match")
    return


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
