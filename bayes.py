from numpy import *


def textParse(bigString):
    import re
    calendarList = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    listOfTokens = re.split(r'\W*', bigString)
    returnList = []
    for tok in listOfTokens:
        if len(tok) > 2 and not tok.isdigit():
            if tok.lower() in calendarList:
                continue
            returnList.append(tok.lower())
    return returnList
    #return [tok.lower() for tok in listOfTokens if len(tok) > 2 and not tok.isdigit() and if tok not in calendarList]

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                ['mr', 'licks', 'ate', 'my', 'steak', 'how','to', 'stop', 'him'],
                ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec

def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        #else:
            #print "the word %s is not in my vocabulary" % word
    return returnVec

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

def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]+= 1
    return returnVec

def calculateMI(vocabList, trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pSoftware = sum(trainCategory) / float(numTrainDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    p1Doc = 0.0
    p0Doc = 0.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
            p1Doc += 1
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
            p0Doc += 1

    p11Vect = p1Num / p1Doc
    p10Vect = p0Num / p0Doc
    p01Vect = ones(numWords) - p11Vect
    p00Vect = ones(numWords) - p10Vect

    pWordVect = p1Num / float(numTrainDocs)

    #print p1Denom
    #print p0Denom
    #print pWordVect

    #print p11Vect
    #print p11Vect + log(p11Vect/(pWordVect*pSoftware))

    miVect = p11Vect*log(p11Vect/(pWordVect*pSoftware)) + \
    p01Vect*log(p01Vect/((ones(numWords)-pWordVect)*pSoftware)) + \
    p10Vect*log(p10Vect/(pWordVect*(1-pSoftware))) + \
    p00Vect*log(p00Vect/((ones(numWords)-pWordVect)*(1-pSoftware)))

    #print miVect

    return miVect



def Test():
    docList = []
    classList = []
    fullText = []
    docList_15 = []
    calendarList = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

    sourceFile = open('./result_long.txt').readlines()
    sourceFile_15 = open('./removeStopWord_15_modify.txt').readlines()

    totalNo = len(sourceFile)
    testSetNo = int(totalNo * 0.2)
    totalNo_15 = len(sourceFile_15)

    #print 'total document: ', totalNo
    #print 'sampling document: ', testSetNo

    # initial parsing and make classification list for 2014 data
    for line in sourceFile:
        wordList = textParse(line)
        docList.append(wordList)
        fullText.extend(wordList)
        if line.startswith('1'):
            classList.append(1)
        else:
            classList.append(0)

    # prepare 2015 data
    for line in sourceFile_15:
        wordList = textParse(line)
        docList_15.append(wordList)

    #print 'total software document ', sum(classList)

    # make raw vocabList
    vocabList = createVocabList(docList)
    #print vocabList

    trainingSet = range(totalNo)
    #testSet = []

    #for i in range(testSetNo):
    #    randIndex = int(random.uniform(0, len(trainingSet)))
    #   testSet.append(trainingSet[randIndex])
    #    del(trainingSet[randIndex])

    trainMat = []
    trainClass = []

    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
        trainClass.append(classList[docIndex])

    # calculate MI value
    miVect = calculateMI(vocabList, array(trainMat), array(trainClass))

    print miVect

    str = ""
    newvocabList = []

    # make new vocabList based on MI value over 2.7
    for index in range(len(vocabList)):
        print index, vocabList[index], "%.10f" % miVect[index]
        str += vocabList[index] + '\t' + "%.10f" % miVect[index] + '\n'
        if miVect[index] > 2.45:
            newvocabList.append(vocabList[index])

    miResult = open('./miResult2.txt', 'w')
    miResult.write(str)
    miResult.close()

    # make new training matrix based on new vocabList
    trainMat2 = []
    trainClass2 = []

    for docIndex in trainingSet:
        trainMat2.append(setOfWords2Vec(newvocabList, docList[docIndex]))
        trainClass2.append(classList[docIndex])

    # make model
    p0V, p1V, pSoftware = trainNB0(array(trainMat2), array(trainClass2))

    errorCount = 0

    #for docIndex in testSet:
    #   wordVector = setOfWords2Vec(newvocabList, docList[docIndex])
    #    if classifyNB(array(wordVector), p0V, p1V, pSoftware) != classList[docIndex]:
    #        errorCount += 1

    # Test 2015 data

    result_15 = open('./2015_result.txt', 'w')
    str = ''
    for docIndex in range(totalNo_15):
        wordVector = setOfWords2Vec(newvocabList, docList_15[docIndex])
        if classifyNB(array(wordVector), p0V, p1V, pSoftware) == 1:
            str += '1\n'
        else:
            str += '0\n'

    result_15.write(str)
    result_15.close()

    #print 'error count: ', errorCount, ' / total sampling test set ', len(testSet)
    #print 'the error rate is: ', float(errorCount)/len(testSet)


