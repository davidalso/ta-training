import csv
import glob
import os

def main():
    scott = open('Scott.csv', 'w')
    scott_csv = csv.writer(scott)
    for filename in glob.glob(os.path.join('*.txt')):
        print(filename)
        textList = formatTextfile(filename)
        errors = findError(textList)
        scott_csv.writerows(errors)
        

def formatTextfile(filename):
    text = open(filename)
    allRows = []
    row = []
    for line in text:
        words = line.split()
        if len(words) >= 3:
            (timeIn, timeOut) = (float(words[0]), float(words[1]))
            length = timeOut - timeIn
            row = [filename, timeIn, timeOut, length, words[2], ' '.join(words[3:])]
            allRows.append(row)
            row = []
    return allRows
            
def findError(textList):
    timeOut = textList[0][2]
    count = 0
    seenTAQ = False
    errors = []
    for row in range(1, len(textList)):
        line = textList[row]
        timeIn = line[1]
        label = line[4]
        if seenTAQ:
            if timeIn != timeOut:
                errors.append(line)
            if label == 'TA':
                seenTAQ = False
        if label == 'TA-Q:':
            seenTAQ = True
        timeOut = textList[row][2]
    return errors
            
        
                
