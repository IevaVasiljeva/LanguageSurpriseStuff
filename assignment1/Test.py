import string
import numpy as np
import DataFormatter
import Model as m
import matplotlib.pyplot as plt

vocabulary = list(string.ascii_lowercase) + ['0', ' ', '.', '#']

def print_genSequence(our_model, given_model):
    text_file = open("../genSequence.txt", "w+")
    text_file.write(
        "Model: " + our_model.generate_from_LM(300) + "\n" +
        "Model_br: " + given_model.generate_from_LM(300)
    )
    text_file.close()


def optimize_alpha():
    values = np.linspace(0.001, 3, 80)
    x = []
    y = []
    for i in values:
        alpha = i
        model = m.Model("../training.en", vocabulary, alpha)
        perplexity = model.calculate_perplexity("../test")
        x.append(alpha)
        y.append(perplexity)
    plt.scatter(x, y)
    plt.grid(which = 'both')
    plt.show()
    idx = y.index(min(y))
    print x[idx]


optimize_alpha()

#preprocess_file("../HG.txt", "../HG2.txt")
# model_theirs = m.Model(model_file_name="../model-br.en")
# model_ours = m.Model("../HG2.txt", vocabulary)
# calculate_Perplexity(model_theirs, "../HG2.txt")
# calculate_Perplexity(model, "../HG2.txt")
# generate_from_LM(model, 600)
# generate_from_LM(model_theirs, 600)