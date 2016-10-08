import re

non_basic_char_set = re.compile("[^a-zA-Z0-9. ]")
digits = re.compile("[0-9]")


# Takes a string and removes all the characters that are not spaces, dots or members of the Latin alphabet.
# Also lower-cases all upper-case letters and changes all digits to 0.
def preprocess_line(line):

    # Remove all the non-basic characters (substitute for nothing).
    line = re.sub(non_basic_char_set, "", line)

    # Lowercase all the remaining characters.
    line = line.lower()

    # Substitute all the digits for 0.
    line = re.sub(digits, "0", line)

    # Add '#' as the beginning and end of the sentence delimiters.
    line = "#" + line + "#"

    return line


def build_model(training_file_name):

    file = open(training_file_name)

    count_dictionary = {}

    for line in file.readlines():
        line = preprocess_line(line)
        count_occurrences(count_dictionary, line)

    calculate_probabilities(count_dictionary)

    print "here"


def count_occurrences(count_dictionary, line):

    char_history = line[:2]

    for i in range(2,len(line)):
        if not char_history in count_dictionary:
            count_dictionary[char_history] = {}
        if line[i] in count_dictionary[char_history]:
            count_dictionary[char_history][line[i]] += 1
        else:
            count_dictionary[char_history][line[i]] = 1

        char_history = char_history[1] + line[i]


def calculate_probabilities(count_dictionary):
    for key in count_dictionary:
        total_count = float(sum(count_dictionary[key].values()))
        for history in count_dictionary[key]:
            count_dictionary[key][history] /= total_count


build_model("../training.en")
