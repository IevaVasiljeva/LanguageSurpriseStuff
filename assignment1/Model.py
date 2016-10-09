import random
import math
import DataFormatter


# A trigram language model stored as a dictionary of all the possible two character combinations char1char2
# mapped to a dictionary of all the possible characters char3 and probabilities P(char3|char1char2)
class Model:

    # Can either build and train a new model by providing training file and a vocabulary
    # or read in an existing model by providing a model file name.
    def __init__(self, training_file_name=None, vocabulary=None, alpha=None, model_file_name=None):

        self.vocabulary = vocabulary
        self.probability_dictionary = {}
        # The alpha parameter for additional smoothing.
        self.alpha = alpha

        if alpha is None:
            self.alpha = 1

        if model_file_name is not None:
            self.read_model(model_file_name)
        else:
            self.build_model(training_file_name, vocabulary)

    def build_model(self, training_file_name, vocabulary):

        training_file = open(training_file_name)

        self.initialise_dictionary()

        for line in training_file.readlines():
            line = DataFormatter.preprocess_line(line)
            self.count_occurrences(line)

        self.calculate_probabilities()

    # Initialises an empty dictionary of all the possible two character combinations
    # mapped to a dictionary of all the possible characters and the number of times that they have been seen proceeding the first two characters.
    def initialise_dictionary(self):

        # Loop through all the possible combinations of two characters.
        for char1 in self.vocabulary:
            for char2 in self.vocabulary:
                history_combination = "" + char1 + char2
                # Create an empty dictionary entry for each combination.
                self.probability_dictionary[history_combination] = {}
                # Loop through all the possible third characters and add a map entry (initially set to 0).
                for char3 in self.vocabulary:
                    self.probability_dictionary[history_combination][char3] = 0


    # For all character combinations char1char2 and all characters char3 counts the number of times char1char2 is followed by char3.
    def count_occurrences(self, line):

        # Take the first two characters.
        char_history = line[:2]

        # Loop through the rest of the characters one by one.
        for i in range(2, len(line)):
            next_char = line[i]
            # Increase the number of times we have seen the previous two chars being followed by the next one.
            self.probability_dictionary[char_history][next_char] += 1
            # Update the two history characters.
            char_history = char_history[1] + next_char


    # Given the counts of any two characters being followed by any third one,
    # obtain the probabilities of this combination using maximum likelihood estimate.
    # Use additional smoothing.
    def calculate_probabilities(self):

        # Loop through all the two character combinations.
        for key in self.probability_dictionary:
            # Get the total number of times the current combination has been encountered.
            total_count = float(sum(self.probability_dictionary[key].values())) + len(self.vocabulary)*self.alpha
            # Divide the counts of char3 following char1char2 by the total number of times char1char2 has been encountered.
            # (obtain ML estimate of char3 following char1char2).
            for history in self.probability_dictionary[key]:
                if not total_count == 0:
                    self.probability_dictionary[key][history] = (self.probability_dictionary[key][history] + self.alpha) / total_count

    # Reads in a trigram language model from a file.
    # The input file is formatted as char1char2char3 <tab> P(char3|char1char2)
    def read_model(self, model_file):

        file = open(model_file)
        self.probability_dictionary = {}

        for line in file.readlines():
            char_sequence = line.split("\t")[0]
            prob = float(line.split("\t")[1])
            char_history = char_sequence[0:2]

            if char_history not in self.probability_dictionary:
                self.probability_dictionary[char_history] = {}

            self.probability_dictionary[char_history][char_sequence[-1]] = prob

    # Prints out a language model.
    # Each line is formatted as char1char2char3 <tab> P(char3|char1char2)
    def print_model(self, output_file):

        outp_file = open(output_file, 'w+')

        # Loop through all the trigram probabilities of the model.
        for char_history in self.probability_dictionary:
            for next_char in self.probability_dictionary[char_history]:
                outp_file.write(char_history + next_char + "\t" + str(self.probability_dictionary[char_history][next_char]) + "\n")

    # Generates a character sequence of the given length according to the given trigram model.
    def generate_from_LM(self, length):

        # Every sequence starts with "##".
        sequence = "##"

        # Generate characters until the necessary length is reached.
        while len(sequence) < length:

            # Get a random float between 0 and 1.
            randomiser_result = random.uniform(0, 1)
            # Base the next character on the previous two.
            current_history = sequence[len(sequence)-2:]
            # Get the relevant trigram probabilities.
            current_trigram_probs = self.probability_dictionary[current_history]
            prob_sum = 0

            # Loop through all the potential next characters.
            for key, value in current_trigram_probs.iteritems():
                # Stop when we reach the accumulated probability larger than the generated number.
                # The character falling in this probability slot os the one that gets generated.
                prob_sum += value
                if prob_sum > randomiser_result:
                    sequence += key
                    # As every end of the sentence is also a beginning, add another #.
                    if key == "#":
                        sequence += "#"
                    break

        return sequence

    def calculate_perplexity(self, test_file):
        file = open(test_file)
        #being perplexity the average of the probabilities for each trigram according to our model
        sum_probs = 0
        counter = 0
        for line in file.readlines():
            line = DataFormatter.preprocess_line(line)
            # Take the first two characters.
            char_history = line[:2]

            for i in range(2, len(line)):
                next_char = line[i]
                if not next_char in self.probability_dictionary[char_history]:
                    continue
                log_prob = - math.log(self.probability_dictionary[char_history][next_char],2)
                sum_probs += log_prob
                # Update the two history characters.
                char_history = char_history[1] + next_char
                counter += 1

        average = sum_probs / counter
        perplexity = 2 ** (average)
        print perplexity
        return perplexity