import csv
import os
import glob
from statistics import stdev
from statistics import mean
from TAModule import *

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
    


