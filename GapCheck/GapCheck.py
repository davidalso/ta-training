import glob
import csv
from TAModule import *

def main():
    for filename in glob.glob('*.txt'):
        textfile = Textfile(filename)
        textfile.reviewGaps()

    incorrect = open('GapCheck.csv', 'w', newline = '')
    incorrect_csv = csv.writer(incorrect)
    incorrect_csv.writerows(Textfile.incorrect)
