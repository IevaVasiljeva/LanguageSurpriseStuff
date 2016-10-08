import random
import re
import string

non_basic_char_set = re.compile("[^a-zA-Z0-9. ]")
digits = re.compile("[0-9]")
vocabulary = list(string.ascii_lowercase) + ['0', ' ', '.', '#']


# Takes a string and removes all the characters that are not spaces, dots or members of the Latin alphabet.
# Also lower-cases all upper-case letters and changes all digits to 0.
def preprocess_line(line):

    # Remove all the non-basic characters (substitute for nothing).
    line = re.sub(non_basic_char_set, "", line)

    # Lowercase all the remaining characters.
    line = line.lower()

    # Substitute all the digits for 0.
    line = re.sub(digits, "0", line)

    # Add '##' as the beginning sentence delimiter and '#' as the end of the sentence delimiter.
    line = "##" + line + "#"

    return line


def build_model(training_file_name):

    file = open(training_file_name)

    probability_dictionary = initialise_dictionary()

    for line in file.readlines():
        line = preprocess_line(line)
        count_occurrences(probability_dictionary, line)

    calculate_probabilities(probability_dictionary)

    return probability_dictionary


# Initialises an empty dictionary of all the possible two character combinations
# mapped to a dictionary of all the possible characters and the number of times that they have been seen proceeding the first two characters.
def initialise_dictionary():

    probability_dictionary = {}

    # Loop through all the possible combinations of two characters.
    for char1 in vocabulary:
        for char2 in vocabulary:
            history_combination = "" + char1 + char2
            # Create an empty dictionary entry for each combination.
            probability_dictionary[history_combination] = {}
            # Loop through all the possible third characters and add a map entry (initially set to 0).
            for char3 in vocabulary:
                probability_dictionary[history_combination][char3] = 0

    return probability_dictionary


# For all character combinations char1char2 and all characters char3 counts the number of times char1char2 is followed by char3.
def count_occurrences(count_dictionary, line):

    # Take the first two characters.
    char_history = line[:2]

    # Loop through the rest of the characters one by one.
    for i in range(2, len(line)):
        next_char = line[i]
        # Increase the number of times we have seen the previous two chars being followed by the next one.
        count_dictionary[char_history][next_char] += 1
        # Update the two history characters.
        char_history = char_history[1] + next_char


# Given the counts of any two characters being followed by any third one,
# obtain the probabilities of this combination using maximum likelihood estimate.
def calculate_probabilities(count_dictionary):

    # Loop through all the two character combinations.
    for key in count_dictionary:
        # Get the total number of times the current combination has been encountered.
        total_count = float(sum(count_dictionary[key].values()))
        # Divide the counts of char3 following char1char2 by the total number of times char1char2 has been encountered.
        # (obtain ML estimate of char3 following char1char2).
        for history in count_dictionary[key]:
            if not total_count == 0:
                count_dictionary[key][history] /= total_count


def print_model(probability_dictionary, output_file):

    file = open(output_file, 'w+')

    for char_history in probability_dictionary:
        for next_char in probability_dictionary[char_history]:
            file.write(char_history + next_char + "\t" + str(probability_dictionary[char_history][next_char]) + "\n")


# Reads in a language model and stores it as a dictionary of all the possible two character combinations
# mapped to a dictionary of all the possible characters
# and the number of times that they have been seen proceeding the first two characters.
# The input file is formatted as char1char2char3 <tab> P(char3|char1char2)
def read_file(model_file):
    file = open(model_file)
    model = {}

    for line in file.readlines():
        char_sequence = line.split("\t")[0]
        prob = float(line.split("\t")[1])
        char_history = char_sequence[0:2]

        if not char_history in model:
            model[char_history] = {}

        model[char_history][char_sequence[-1]] = prob

    return model


# Generates a character sequence of the given length according to the given trigram model.
def generate_from_LM(model, length):

    # Every sequence starts with "##".
    sequence = "##"

    # Generate characters until the necessary length is reached.
    while len(sequence) < length:
        # Get a random float between 0 and 1.
        randomiser_result = random.uniform(0, 1)
        #
        current_history = sequence[-2:]
        current_trigram_probs = model[current_history]
        prob_sum = 0
        for key, value in current_trigram_probs.iteritems():
            prob_sum += value
            if prob_sum > randomiser_result:
                sequence += key
                if key == "#":
                    sequence += "#"
                    break

    print sequence
    return sequence


model = build_model("../training.en")
print_model(model, "../model.en")
