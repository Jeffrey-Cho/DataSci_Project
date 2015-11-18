from numpy import *
import re

DEBUG = False
TEST_MODE = True
MI_THRESH_HOLD = 2.5

"""
Remove stop word from input string
"""
def rmStopWord(string):
    string = replaceId(string)
    string = string.lower()

    stopwordfile = open('./stopwords_long.txt')
    wordlist = stopwordfile.readlines()

    monthList = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

    for word in wordlist:
        word = word.strip().lower()
        word = ' '+word+' '
        string = re.sub(word, ' ', string)

    for word in monthList:
        string = re.sub(word, '', string)

    string = re.sub(' , ', '\t', string)

    # remove numeric pattern value
    string = re.sub('[0-9]', '', string)

    string = re.sub('sensors', 'sensor', string)
    string = re.sub('lights', 'light', string)
    string = re.sub('wheels', 'wheel', string)

    stopwordfile.close()

    return string


"""
Replace id to 1 or 0 for analysis
"""
def replaceId(string):
    swidfile = open('./2014RecallNo_Software.csv').readlines()
    nonswfile = open('./2014RecallNo_nonSoftware.csv').readlines()
    noclassfile = open('./2014RecallNo_NoClassification.csv').readlines()

    for swid in swidfile:
        swid = swid.strip()
        string = re.sub(swid, 'sw', string)

    for nonswid in nonswfile:
        nonswid = nonswid.strip()
        string = re.sub(nonswid, 'ns', string)

    for noclassid in noclassfile:
        noclassid = noclassid.strip()
        string = re.sub(noclassid, 'ns', string)

    return string

"""
tokenize the input string and add list
add word over 2 character except digit and month name
"""
def textParse(string):
    listOfTokens = re.split(r'\W*', string)
    returnList = []
    for tok in listOfTokens:
        if len(tok) > 2:
            returnList.append(tok.lower())
    return returnList

"""
Textbook Example Function
"""
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                ['mr', 'licks', 'ate', 'my', 'steak', 'how','to', 'stop', 'him'],
                ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec

"""
create the vocabulary list
"""
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

"""
create vector list each description
"""
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        #else:
            #print "the word %s is not in my vocabulary" % word
    return returnVec

"""
create vector list with bagging
"""
def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]+= 1
    return returnVec

"""
training with naive baysian algorithm
"""
def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pSoftware = sum(trainCategory) / float(numTrainDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])

    p1Vect = log(p1Num / p1Denom)
    p0Vect = log(p0Num / p0Denom)

    return p0Vect, p1Vect, pSoftware

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

"""
textbook example code
"""
def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print classifyNB(thisDoc, p0V, p1V, pAb)

"""
caclulate Mutual Information value of each token
"""
def calculateMI(vocabList, trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pSoftware = sum(trainCategory) / float(numTrainDocs)    # probability P(software)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 0.0
    p1Denom = 0.0
    p1Doc = 2.0         # for preventing minus probability, it will make log value NaN
    p0Doc = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
            p1Doc += 1.0
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
            p0Doc += 1.0

    p11Vect = p1Num / p1Doc                 # probability P(word = 1, category = Software)
    p00Vect = p0Num / p0Doc                 # probability P(word = 1, category = non-Software)
    p01Vect = ones(numWords) - p11Vect      # probability P(word = 0, category = Software)
    p10Vect = ones(numWords) - p00Vect      # probability P(word = 0, category = non-Software)

    pWordVect = (p1Num + p0Num) / float(numTrainDocs)   # probability P(word)

    # logBaseSwVect = p11Vect/(pWordVect*pSoftware)
    # logBaseSwVect2 = p01Vect/((ones(numWords)-pWordVect)*pSoftware)
    # logBasenonSwVect = p10Vect/((ones(numWords)-pWordVect)*(1-pSoftware))
    # logBasenonSwVect2 = p00Vect/(pWordVect*(1-pSoftware))

    #debugging
    # for i in range(numWords):
    #     if isnan(log(logBaseSwVect[i])):
    #         print 'first'
    #         print vocabList[i]
    #         print logBaseSwVect[i]
    #     if isnan(log(logBaseSwVect2[i])):
    #         print 'second'
    #         print vocabList[i]
    #         print logBaseSwVect2[i]
    #         print p01Vect[i]
    #         print (ones(numWords)-pWordVect)[i]*pSoftware
    #     if isnan(log(logBasenonSwVect[i])):
    #         print 'third'
    #         print vocabList[i]
    #         print logBasenonSwVect[i]
    #     if isnan(log(logBasenonSwVect2[i])):
    #         print 'forth'
    #         print vocabList[i]
    #         print logBasenonSwVect2[i]


    miVect = p11Vect*log(p11Vect/(pWordVect*pSoftware)) + \
    p01Vect*log(p01Vect/((ones(numWords)-pWordVect)*pSoftware)) + \
    p10Vect*log(p10Vect/((ones(numWords)-pWordVect)*(1-pSoftware))) + \
    p00Vect*log(p00Vect/(pWordVect*(1-pSoftware)))

    return miVect

def debugWrite(string):
    if DEBUG is True:
        tempfile = open('tempResult.txt', 'w')
        tempfile.write(string)
        tempfile.close()

def debugPrint(string):
    if DEBUG is True:
        print string

"""
Main function
"""
def run():
    trainingString = open('./a.txt').read()
    predictionString = open('./b.txt').read()

    trainingString = rmStopWord(trainingString)
    predictionString = rmStopWord(predictionString)

    docList = []
    classList = []
    fullText = []
    predictionDocList = []

    trainingList = trainingString.split('\n')
    totalNo = len(trainingList)
    testSetNo = int(totalNo * 0.2)      # for testing set ratio 20%

    predictionList = predictionString.split('\n')
    totalNo_15 = len(predictionList)

    # initial parsing and make classification list for 2014 data
    for line in trainingList:
        wordList = textParse(line)
        docList.append(wordList)
        fullText.extend(wordList)
        if line.startswith('sw'):
            classList.append(1)
        else:
            classList.append(0)

    # prepare 2015 data
    for line in predictionList:
        wordList = textParse(line)
        predictionDocList.append(wordList)

    # make raw vocabList
    vocabList = createVocabList(docList)

    trainMat = []
    trainClass = []

    for docIndex in range(totalNo):
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
        trainClass.append(classList[docIndex])

    # calculate MI value
    miVect = calculateMI(vocabList, array(trainMat), array(trainClass))

    str = ""
    newvocabList = []

    # make new vocabList based on MI value over 2.7
    for index in range(len(vocabList)):
        str += vocabList[index] + '\t' + "%.10f" % miVect[index] + '\n'
        if miVect[index] > MI_THRESH_HOLD:
            newvocabList.append(vocabList[index])

    debugWrite(str)

    trainingSet = range(totalNo)

    if TEST_MODE == True:
        testSet = []

        for i in range(testSetNo):
            randIndex = int(random.uniform(0, len(trainingSet)))
            testSet.append(trainingSet[randIndex])
            del(trainingSet[randIndex])


    # make new training matrix based on new vocabList
    trainMat2 = []
    trainClass2 = []

    for docIndex in trainingSet:
        trainMat2.append(setOfWords2Vec(newvocabList, docList[docIndex]))
        trainClass2.append(classList[docIndex])

    # make model
    p0V, p1V, pSoftware = trainNB0(array(trainMat2), array(trainClass2))


    if TEST_MODE == True:
        errorCount = 0
        truePositive = 0
        trueNegative = 0
        falsePositivie = 0
        falseNegative = 0

        for docIndex in testSet:
            wordVector = setOfWords2Vec(newvocabList, docList[docIndex])
            decisionResult = classifyNB(array(wordVector), p0V, p1V, pSoftware)
            if classList[docIndex] == 1:
                if decisionResult == 1:
                    truePositive += 1
                elif decisionResult == 0:
                    trueNegative += 1
            else :
                if decisionResult == 0:
                    falseNegative += 1
                elif decisionResult == 1:
                    falsePositivie += 1

            if decisionResult != classList[docIndex]:
                errorCount += 1

        recall = truePositive / float(truePositive + trueNegative)
        precision = truePositive / float(truePositive + falsePositivie)
        accuracy = 1 - (errorCount / float(len(testSet)))

        print "MI value: ", MI_THRESH_HOLD
        print "Recall: ", recall
        print "Precision: ", precision
        print "Accuray: ", accuracy

    # Test 2015 data

    prdictionResult = open('./predictionResult.txt', 'w')
    str = ''

    for docIndex in range(totalNo_15):
        wordVector = setOfWords2Vec(newvocabList, predictionDocList[docIndex])
        if classifyNB(array(wordVector), p0V, p1V, pSoftware) == 1:
            str += '1\n'
        else:
            str += '0\n'

    prdictionResult.write(str)
    prdictionResult.close()


