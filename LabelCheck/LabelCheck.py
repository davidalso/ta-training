import csv
import os
import glob
from TAModule import *

def main():
    for filename in glob.glob('*.txt'):
        textfile = Textfile(filename)
        textfile.reviewLabels()

    incorrect = open('IncorrectLabels.csv', 'w', newline = '')
    incorrect_csv = csv.writer(incorrect, delimiter = ',')
    incorrect_csv.writerows(Textfile.incorrect)
