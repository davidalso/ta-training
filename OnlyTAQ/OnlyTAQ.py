import csv
import os
import glob

#Represents the important information for a text file like 'w01A01.txt'
class Textfile(object):
    def __init__(self, filename):
        self.filename = filename
        self.week = int(filename[1:3])
        self.section = filename[3]
        self.part =  int(filename[4:6])
        if self.part % 2 == 1:
            self.isOdd = True
        else:
            self.isOdd = False
#boolean determines whether the whole or part of the text file will be read
        self.readOverlap = False
        self.textList = self.formatTextfile()
#self.result will contain all the TAQ that file finds within itself
        self.result = []

#Goes through its formatted text list and searches for TAQ
    def findTAQ(self):
        for textLine in self.textList:
            if textLine.label == 'TA-Q:' or textLine.label == 'TAQ:':
                if self.readOverlap:
                    self.result.append(textLine.getListFormat())
                else:
                    (timeIn, timeOut) = (textLine.timeIn, textLine.timeOut)
                    if self.isOdd:
                        if timeIn < 240:
                            self.result.append(textLine.getListFormat())
                    else:
                        if timeOut > 60:
                            self.result.append(textLine.getListFormat())
                            
#Takes a .txt file and turns it into a readable 2D list
    def formatTextfile(self):
        textfile = open(self.filename, 'r')
        allLines = []
        for line in textfile:
            words = line.split()
            if len(words) >= 3:
                allLines.append(TextLine(self.filename, words))
        return allLines

#Represents every line in a .txt file
class TextLine(object):
    def __init__(self, filename, listLine):
        self.filename = filename
        self.week = int(filename[1:3])
        self.section = filename[3]
        self.part =  int(filename[4:6])
        self.timeIn = float(listLine[0])
        self.timeOut = float(listLine[1])
        self.length = self.timeOut - self.timeIn
        self.label = listLine[2]
        self.text = ' '.join(listLine[3:])
#prepares the object to be written into a .csv
    def getListFormat(self):
        return [self.filename, self.week, self.section, self.part,
                self.realTime(self.timeIn), self.realTime(self.timeOut),
                self.length, self.label, self.text]
    
#changes a .txt file relative time into the class time based on its part
    def realTime(self, time):
        if self.part % 2 == 1:
            return (self.part // 2) * 9 * 60 + time
        else:
            return ((self.part // 2) * 9 - 5) * 60 + time
        
#Based on two .txt files it chooses to read the overlap for
#the one with the most TAQs
def pairPriority(pair):
    (file1, file2) = pair
    (count1, count2) = (0, 0)
    if file2 != None:
        with open(file1, "r") as text1, open(file2, "r") as text2:
            for row in text1:
                line = row.split()
                if len(line) > 0 and float(line[1]) > 240:
                    if line[2] == 'TA-Q:':
                        count1 = count1 + 1
            for row in text2:
                line = row.split()
                if len(line) > 0 and float(line[0]) < 60:
                    if line[2] == 'TA-Q:':
                        count2 = count2 + 1
    else:
        return file1
    if count1 > count2:
        return file1
    else:
        return file2

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
        files[pairPriority(pair)].readOverlap = True

#Makes all TextFile intances analyze themselves and prepare there TAQs
    for filename in files:
        files[filename].findTAQ()

    writeCSV(files)

#writes the .csv
def writeCSV(files):
    with open('OnlyTAQs.csv', 'w', newline='') as sheet:
        output = csv.writer(sheet, delimiter=',')
#writes the header of the csv
        output.writerow(['File Name', 'Week', 'Section', 'Part', 'Time In',
                         'Time Out', 'Length', 'Label', 'Text'])
        for filename in files:
            output.writerows(files[filename].result)
    sheet.close()

#returns the .txt file name for the corresponding pair of the odd numbered .txt
def findPair(filename):
    textNum = 0
    textNum = int(filename[4:6])
    textNum = textNum + 1
    if textNum < 10:
        return filename[:4] + '0' + str(textNum) + filename[6:]
    return filename[:4] + str(textNum) + filename[6:] 
