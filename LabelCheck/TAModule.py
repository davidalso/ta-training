class Code(object):
    codes = ['kb', 'elab', 'fr', 'der', 'any?', 'part',
             'pk', 'admin', 're', 'r?', 'xx', 'Uncoded']
    def __init__(self, code):
        self.code = code
        self.counts = {'WT1':0, 'WT2':0, 'ST':0, 'TA':0}
        self.lengths = {'WT1':[], 'WT2':[], 'ST':[]}



        

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
    def getListFormat(self, inRealTime):
        if inRealTime:
            return [self.filename, self.week, self.section, self.part,
                    self.realTime(self.timeIn), self.realTime(self.timeOut),
                    self.length, self.label, self.text]
        return [self.filename, self.week, self.section, self.part, self.timeIn,
                self.timeOut,self.length, self.label, self.text]
    
#changes a .txt file relative time into the class time based on its part
    def realTime(self, time):
        if self.part % 2 == 1:
            return (self.part // 2) * 9 * 60 + time
        else:
            return ((self.part // 2) * 9 - 5) * 60 + time


        

#holds information for .txt files and allows for  individual analysis
class Textfile(object):
    #questions that were not in the question to code dictionary go here
    uncoded = [['File Name', 'Week', 'Section', 'Part', 'Time In',
                'Time Out', 'Length', 'Label', 'Text']]
    #question events that ended due to audio and are incomplete TA event
    undetermined = [['File Name', 'Week', 'Section', 'Part', 'Time In',
                'Time Out', 'Length', 'Label', 'Text']]
    #labels that need revision
    incorrect = [['File Name', 'Week', 'Section', 'Part', 'Time In',
                'Time Out', 'Length', 'Label', 'Text']]
    TAQs = [['File Name', 'Week', 'Section', 'Part', 'Time In',
                'Time Out', 'Length', 'Label', 'Text']]
    labels = {'ST', 'ST-Q', 'STQ', 'MS', 'STO',
              'TA', 'TAQ:', 'TA-Q:', 'G', 'RAQ'}
    STEvent = {'ST', 'ST-Q', 'STQ', 'MS', 'STO'}
    TAEvent = {'TA', 'TAQ:', 'TA-Q:'}
    
    def __init__(self, filename, questions = dict()):
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
            #get time for within the .txt file
            Textfile.undetermined.append(allLines[index].getListFormat(False))
            return allLines[:index]
        else:
            return allLines

    def findTAQs(self):
        for line in self.textList:
            if line.label == 'TA-Q:' or line.label == 'TAQ:':
                #True to get real time for labels
                Textfile.TAQs.append(line.getListFormat(True))
        
    #checks if the all labels withi a .txt are correctly written
    def reviewLabels(self):
        for line in self.textList:
            if line.label not in Textfile.labels:
                Textfile.incorrect.append(line.getListFormat(False))
        
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
        #get time for within the .txt file
        Textfile.uncoded.append(line.getListFormat(False))
        return 'Uncoded'
