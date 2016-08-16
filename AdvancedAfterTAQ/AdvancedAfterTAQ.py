import csv
import os
import glob
from statistics import stdev
from statistics import mean
#started adding questions on 2491

#For this program TextLine is simply to store information
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
        
class Code(object):
    codes = ['kb', 'elab', 'fr', 'der', 'any?', 'part',
             'pk', 'admin', 're', 'r?', 'xx', 'Uncoded']
    def __init__(self, code):
        self.code = code
        self.counts = {'WT1':0, 'WT2':0, 'ST':0, 'TA':0}
        self.lengths = {'WT1':[], 'WT2':[], 'ST':[]}

    def __repr__(self):
        return self.code
    
#holds information for .txt files and allows for  individual analysis
class Textfile(object):
    #questions that were not in the question to code dictionary go here
    uncoded = []
    #question events that ended due to audio and are incomplete TA event
    undetermined = []
    STEvent = {'ST', 'ST-Q', 'STQ', 'MS', 'STO'}
    TAEvent = {'TA', 'TAQ:', 'TA-Q:'}
    
    def __init__(self, filename, questions):
        self.filename = filename
        self.week = int(filename[1:3])
        self.section = filename[3]
        self.part =  int(filename[4:6])
        self.readOverlap = False
        if self.part % 2 == 1:
            self.isOdd = True
        else:
            self.isOdd = False
        self.textList = self.formatTextfile()
        self.codes = Textfile.initCodes()
        self.questions = questions

    #prepares the dictionary that will point to Code instances
    @staticmethod
    def initCodes():
        codes = dict()
        for code in Code.codes:
            codes[code] = Code(code)
        return codes
    
    #counts the number of events that occured in a overlap region
    def countOverlap(self):
        count = 0
        for line in self.textList:
            if line.label == 'TA-Q:' or line.label == 'TAQ:':
                if self.isOdd:
                    if line.timeIn < 240:
                        count = count + 1
                else:
                    if line.timeOut > 60:
                        count = count + 1
        return count

    #returns a list containing Texline instances
    def formatTextfile(self):
        textfile = open(self.filename, 'r')
        allLines = []
        for line in textfile:
            words = line.split()
            if len(words) >= 3:
                allLines.append(TextLine(self.filename, words))
        return allLines
    
    #removes the events that are not considered due to overlap
    def trimOverlap(self):
        newTextList = []
        if self.readOverlap:
            self.textList = self.trimEnd(self.textList)
        else:
            for line in self.textList:
                if self.isOdd:
                    if line.timeIn < 240:
                        newTextList.append(line)
                else:
                    if line.timeOut > 60:
                        newTextList.append(line)
            self.textList = self.trimEnd(newTextList)
                    
    #removes any question event that did not reach another TA event
    def trimEnd(self, allLines):
        seenTAQ = False
        index = len(allLines)
        for row in range(len(allLines)):
            line = allLines[row]
            if line.label == 'TA-Q:' or line.label == 'TAQ:':
                seenTAQ = True
                index = row
            elif line.label == 'TA':
                seenTAQ = False
        if seenTAQ:
            Textfile.undetermined.append(allLines[index].getListFormat())
            return allLines[:index]
        else:
            return allLines
        
    #most important method
    #counts the events that occur after TAQ and the lengths
    def afterTAQ(self):
        currentCode = ''
        (isRelevant, seenTAQ, seenST, wasST) = (False, False, False, False)
        for line in self.textList:
            if isRelevant:
                if line.label in Textfile.TAEvent:
                    #the end of an event with either TAQ or TA
                    if wasST:
                        self.codes[currentCode].counts['ST'] += 1
                    else:
                        self.codes[currentCode].counts['TA'] += 1
                    #reset the flags         
                    if line.label == 'TA':
                        (isRelevant, seenTAQ) = (False, False)
                    #TAQ: or TA-Q:
                    else:
                        currentCode = self.tryDict(line)
                        (isRelevant, seenTAQ) = (True, True)
                    (seenST, wasST) = (False, False)
                elif line.label in Textfile.STEvent:
                    (seenST, wasST) = (True, True)
                    self.codes[currentCode].lengths['ST'].append(line.length)
                #remaining gaps G
                else:
                    if seenTAQ:
                        #gap after seeing a TAQ
                        self.codes[currentCode].lengths['WT1'].append(line.length)
                        self.codes[currentCode].counts['WT1'] += 1
                        seenTAQ = False
                    elif seenST:
                        #gap after seeing a student event
                        self.codes[currentCode].lengths['WT2'].append(line.length)
                        self.codes[currentCode].counts['WT2'] += 1
                        seenST = False
                        
            else:
                #only a TAQ event can make it the lines relevant again
                if line.label == 'TA-Q:' or line.label == 'TAQ:':
                    currentCode = self.tryDict(line)
                    (isRelevant,seenTAQ,seenST,wasST) = (True,True,False,False)

    #tries to find the question in the question dictionary
    def tryDict(self, line):
        question = line.text.lower()
        if question in self.questions:
            return self.questions[question]
        Textfile.uncoded.append(line.getListFormat())
        return 'Uncoded'

#must be called to run the entire program
def main():
    (files, questions) = (dict(), prepareDict())
    path = os.path.dirname('AdvancedAfterTAQ.py')
    #go through folder and focuses on .txt files
    for infile in glob.glob( os.path.join(path, '*.txt') ):
        files[infile] = Textfile(infile, questions)
        
    pairs = []
    #creates pairs of file names
    for filename in files:
        if files[filename].isOdd:
            pair = findPair(filename)
            if pair in files:
                pairs.append((filename, pair))
            else:
                pairs.append((filename, None))

    for pair in pairs:
        pairPriority(pair, files)
    for filename in files:
        files[filename].afterTAQ()
    compileRecitations(files)

#creates the question to code dictionary
def prepareDict():
    codes = dict()
    questions = open("QuestionsToCode.csv", 'r')
    questions_csv = csv.reader(questions)
    for row in questions_csv:
        codes[row[0].lower()] = row[1]
    questions.close()
    return codes

#joins all the Textfiles and writes all the .csv files
def compileRecitations(files):
    data = open('AdvancedAfterTAQ.csv', 'w')
    data_csv = csv.writer(data)
    uncoded = open('Uncoded.csv', 'w')
    uncoded_csv = csv.writer(uncoded)
    removed = open('Undetermined.csv', 'w')
    removed_csv = csv.writer(removed)
    
    header = ['WEEK', 'SECTION', 'Code',
              'WT1-COUNT', 'WT2-COUNT', 'ST-COUNT', 'TA-COUNT',
              'WT1-SUM', 'WT1-AVG', 'WT1-STDEV',
              'WT2-SUM', 'WT2-AVG', 'WT2-STDEV',
              'ST-SUM', 'ST-AVG', 'ST-STDEV']
    data_csv.writerow(header)
    for week in range(1, 11):
        for section in ['B', 'C', 'E']:
            origCodes = Textfile.initCodes()

            for filename in files:
                file = files[filename]
                if file.week == week and file.section == section:
                    mergeCodes(origCodes, file.codes)
            

            sectionData = prepareRows(week, section, origCodes)
                
                
            data_csv.writerows(sectionData)
    removed_csv.writerows(Textfile.undetermined)
    uncoded_csv.writerows(Textfile.uncoded)
    data.close()
    removed.close()

#creates a formatted list for the 'AdvancedAfterTAQ.csv'   
def prepareRows(week, section, origDict):
    result = []
    (lenKeys, countKeys) = (['WT1', 'WT2', 'ST'], ['WT1', 'WT2', 'ST', 'TA'])
    for code in Code.codes:
        if code != "Uncoded":
            codeRow = [week, section, code]
            counts = origDict[code].counts
            lengths = origDict[code].lengths
            for key in countKeys:
                codeRow.append(counts[key])
            for key in lenKeys:
                category = lengths[key]
                codeRow.append(sum(category))
                if len(category) > 0:
                    codeRow.append(mean(category))
                else:
                    codeRow.append('N/A')
                if len(category) > 1:
                    codeRow.append(stdev(category))
                else:
                    codeRow.append('N/A')
            result.append(codeRow)
    return result

#determines the pair of odd number file names
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
    
#joins the Code instances together 
def mergeCodes(orig, new):
    for code in Code.codes:
        merge(orig[code].lengths, new[code].lengths)
        merge(orig[code].counts, new[code].counts)
        
#joins a dictionary together
def merge(orig, new):
    for key in orig:
        orig[key] += new[key]
    


