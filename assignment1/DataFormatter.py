import random
import re
import string
import math as m

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

    # Add '##' as the beginning sentence delimiter and '#' as the end of the sentence delimiter.
    line = "##" + line + "#"

    return line

# Takes a file, splits it so that each sentence is in a new line and strips it from the
def preprocess_file(f_name, output_name):

    # Open the input file and a file for transformed output.
    file = open(f_name)
    file2 = open(output_name, "w+")

    # Read all the text in one large string.
    # TODO this might be impossible if the file is too large.
    text = ""
    for line in file.readlines():
        text += line

    # Strip from the new lines.
    #text = re.sub("[\\\\]", "", text)
    text = re.sub("[\n]", " ", text)
    # Insert a new line by the end of each sentence (assume that sentences end with dots only).
    text = re.sub("\\.", ".\n", text)

    # Write the result to a new file.
    file2.write(text)
