import csv
import glob
from TAModule import *

def main():
    for filename in glob.glob('*.txt'):
        textfile = Textfile(filename)
        textfile.reviewTAQEvent()

    incorrect = open('Scott.csv', 'w', newline = '')
    incorrect_csv = csv.writer(incorrect)
    incorrect_csv.writerows(Textfile.incorrect)
