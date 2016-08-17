import csv
import os
import glob
from TAModule import *
    
def TAQinTextfile(fileIndex, filename, TAQs, labels):
    textfile = open(filename, 'r')
    textList = formatTextfile(filename)
    textfile.close()
    for row in range(len(textList)):
        words = textList[row]
        if len(words) >= 3:
            if words[2] not in labels:
                TAQs.append(formatRows(fileIndex, filename, words))

def formatRows(fileIndex, filename, words):
    timeIn = float(words[0])
    timeOut =  float(words[1])
    length = timeOut - timeIn
    label = words[2]
    question = words[3]
    return [fileIndex, filename, timeIn, timeOut, length, label, question]
    
def formatTextfile(filename):
    textfile = open(filename, 'r')
    allRows = []
    row = []
    for line in textfile:
        words = line.split()
        if len(words) >= 3:
            row = [words[0], words[1], words[2], ' '.join(words[3:])]
            allRows.append(row)
            row = []
    return allRows

        
def writeCSV(TAQs):
    with open('Errors.csv', 'w', newline='') as sheet:
        output = csv.writer(sheet, delimiter=',')
        output.writerows(TAQs)
    sheet.close()

def main():
    for filename in glob.glob('*.txt'):
        textfile = Textfile(filename)
        textfile.reviewLabels()

    incorrect = open('IncorrectLabels.csv', 'w', newline = '')
    incorrect_csv = csv.writer(incorrect, delimiter = ',')
    incorrect_csv.writerows(Textfile.incorrect)
    
def compileAll():
    labels = {"TA-Q:":0, "G":0, "ST":0, "ST-Q":0, "TA":0,
                       "nextTAQ":0, "MS":0, "STO":0}
    TAQs = [['File Index', 'Filename', 'Time In', 'Time Out', 'Length',
             'Label', 'Question']]
    path = os.path.dirname('TAQAnalyzer.py')
    fileIndex = 1
    for filename in glob.glob( os.path.join(path, '*.txt') ):
        TAQinTextfile(fileIndex, filename, TAQs, labels)
        fileIndex = fileIndex + 1
    writeCSV(TAQs)
    print(labels)
