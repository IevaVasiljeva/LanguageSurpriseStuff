import sys
import math
import numpy

english_char = [A-z, " ", ".", 0-9]

def preprocess_line(line):
	newLine = ""
	for char in line:
		if char in english_char:
			if char.isdigit():
				newLine += "0"
			else:
				newLine += char.lower()
			
	return newLine




			

