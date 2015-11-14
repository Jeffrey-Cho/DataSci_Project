def removeStopwords(source, dic):
    for word in dic:
        word = " " + word
        word += " "
        source = source.replace(word, " ")
    return source

def markSw(source, makrFile):
    marklist = makrFile.split('\n')

    for swNo in marklist:
        source.replace(swNo, "1")
    return source

def markNonSw(source, markFile):
    marklist = markFile.split('\n')

    for nonSwNo in marklist:
        source.replace(nonSwNo, '0')
    return source

def markNoClassSw(source, markFile):
    marklist = markFile.split('\n')

    for noclass in marklist:
        source.replace(noclass, '0')
    return source

def start():
    sourceFile = open('./FLAT_RCL_Out_14.txt')
    dicFile = open('./stopwords_long.txt')
    outputFile = open('./result_long.txt', 'w')
    swFile = open('./2014RecallNo_Software.csv')
    nonSwFile = open('./2014RecallNo_nonSoftware.csv')
    noClassFile = open('./2014RecallNo_NoClassification.csv')

    sourceData = sourceFile.read()
    dicData = dicFile.read().split('\n')

    result = removeStopwords(sourceData, dicData).replace(" , ", '\t').replace('\r\n', '\n')

    swmarklist = swFile.read().replace('\r\n', '\n').split('\n')

    for swNo in swmarklist:
        result = result.replace(swNo, "1")

    nonmarklist = nonSwFile.read().split('\n')

    for nonSwNo in nonmarklist:
        result = result.replace(nonSwNo, "0")

    otherlist = noClassFile.read().replace('\r\n', '\n').split('\n')

    for other in otherlist:
        print other
        result = result.replace(other, "0")


    #result1 = markSw(result, swFile.read().replace('\r\n', '\n'))
    #print result1
    #result2 = markNonSw(result1, nonSwFile.read().replace('\r\n', '\n'))
    #result3 = markNoClassSw(result2, noClassFile.read().replace('\r\n', '\n'))

    outputFile.write(result)
    sourceFile.close()
    dicFile.close()
    outputFile.close()
    swFile.close()
    nonSwFile.close()
    noClassFile.close()

def start15():
    sourceFile = open('./FLAT_RCL_Out_15.txt')
    dicFile = open('./stopwords_long.txt')
    outputFile = open('./removeStopWord_15.txt', 'w')

    sourceData = sourceFile.read()
    dicData = dicFile.read().split('\n')

    result = removeStopwords(sourceData, dicData).replace(" , ", '\t').replace('\r\n', '\n')

    outputFile.write(result)

