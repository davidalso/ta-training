import csv
import os
import glob
from TAModule import *
        
#returns the .txt file name for the corresponding pair of the odd numbered .txt
def findPair(filename):
    textNum = 0
    textNum = int(filename[4:6])
    textNum = textNum + 1
    if textNum < 10:
        return filename[:4] + '0' + str(textNum) + filename[6:]
    return filename[:4] + str(textNum) + filename[6:] 
        
#determines which of the pair's overlap will be considered
def pairPriority(pair, files):
    (file1, file2) = pair
    if file1 in files and file2 in files:
        (textfile1, textfile2) = (files[file1],
                                    files[file2])
        if textfile1.countOverlap() > textfile2.countOverlap():
            textfile1.readOverlap = True
        else:
            textfile2.readOverlap = True
        textfile1.trimOverlap()
        textfile2.trimOverlap()
    elif file1 in files and file2 not in files:
        files[file1].readOverlap = True
        files[file1].trimOverlap()
    elif file1 not in files and file2 in files:
        files[file2].readOverlap = True
        files[file2].trimOverlap()

#runs the entire program to turn .txt into the .csv output
def main():
    files = dict()
#seaches through all .txt files within the same folder and adds to dict()
    for infile in glob.glob('*.txt'):
        files[infile] = Textfile(infile)

#prepares the pairs of files for overlap analysis
    pairs = []
    for filename in files:
        if files[filename].isOdd:
            pair = findPair(filename)
            if pair in files:
                pairs.append((filename, pair))
            else:
                pairs.append((filename, None))
                
#analyzes which overlap from the pair will be read/considered
    for pair in pairs:
        pairPriority(pair, files)

#Makes all TextFile intances analyze themselves and prepare there TAQs
    for filename in files:
        files[filename].findTAQs()
        
    onlyTAQs = open('OnlyTAQs.csv', 'w', newline='')
    onlyTAQs_csv = csv.writer(onlyTAQs)
    onlyTAQs_csv.writerows(Textfile.TAQs)
    onlyTAQs.close()


