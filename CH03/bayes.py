#-*-coding:utf-8-*-
from numpy import *
import feedparser
#加载数据
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]#其中1是带有侮辱性的词汇
    return postingList, classVec

#创建一个包括所有词汇不重复的list
#return vocabList
def createVocabList(dataSet):
    vocabSet = set([])#set保证不重复
    for document in dataSet:
        vocabSet = vocabSet | set(document)#遍历每一行的doc，求并集
    return list(vocabSet)

#将词汇矩阵转变转变为词向量
#参数inputSet是一个文档,
#比如说：第一个文档['my', 'dog', 'has', 'flea', 'problems', 'help', 'please']
#vocabList=['cute', 'love', 'help', 'garbage', 'quit', 'I', 'problems', 'is', 'park', 1, 'flea', 'dalmation', 'licks', 'food', 'not', 'him', 'buying', 'posting', 'has', 'worthless', 'ate', 'to', 'maybe', 'please', 'dog', 'how', 'stupid', 'so', 'take', 'mr', 'steak', 'my']
#那么第一个文档的词向量：[0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList) 
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word: %s is not in my Vocabulary!"
    return returnVec

"""
准备数据为：文档词袋模型，这表示每一个文档中的单词可以出现重复的情况，上述的词集模型不可以出现重复
"""
def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList) 
    for word in inputSet:
        if word in vocabList:
            #与上述的词集模型不同在于下面变为+=1
            returnVec[vocabList.index(word)] += 1
        else:
            print "the word: %s is not in my Vocabulary!"
    return returnVec

"""
朴素贝叶斯分类器训练函数
@param trainMatrix:表示的是由每个文档的词向量组成的矩阵，若文档个数为n，vocabList元素数为m，则是(n,m)的矩阵
@param trainCategory: 表示类别list
"""
def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    #pAbusive是出现侮辱性词汇，也就是分类为1的文档出现的概率
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    #初始化
    #为了避免概率值为0，在这里修改为ones函数,初始分母值为2.0
    #p0Num = zeros(numWords);p1Num = zeros(numWords)
    p0Num = ones(numWords);p1Num = ones(numWords)
    #p0Denom = 0.0;p1Denom = 0.0
    p0Denom = 2.0;p1Denom = 2.0
    #遍历每一行的trainMatrix矩阵
    for i in range(numTrainDocs):
        #如果这行文档的分类为1：即为侮辱性文档
        if trainCategory[i] == 1:
            #这样可以使矩阵直接进行对应位置元素相加,得到的p1Num是1行numWords列的行向量
            p1Num += trainMatrix[i]
            #sum(trainMatrix[i])是指的类别是1的文档的词汇的总个数
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    #为了避免下溢和浮点数四舍五入导致的错误，使用log函数
    p1Vect = log(p1Num/p1Denom)
    p0Vect = log(p0Num/p0Denom)
    return p1Vect, p0Vect, pAbusive

"""
朴素贝叶斯分类函数,根据贝叶斯公式得到的
@param vec2Classify: 是需要判断类别的文档的词向量
@param p0Vect: 是训练函数求得的p0Vect
@param p1Vect: 是训练函数求得的p1Vect
@param pClass1: 是类别1出现的概率，这里是0.5
"""
def classifyNB(vec2Classify, p0Vect, p1Vect, pClass1):
    p1 = sum(vec2Classify * p1Vect) + log(pClass1)
    p0 = sum(vec2Classify * p0Vect) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0
    

"""
main函数对上述的各个方法函数进行一个测试
"""
def main():
    postingList, classVec = loadDataSet()
    vocabList = createVocabList(postingList)
    trainMatrix = []
    for e in postingList:
        trainMatrix.append(setOfWords2Vec(vocabList,e))
    p1Vect, p0Vect, pAbusive = trainNB0(trainMatrix, classVec)
    
    #需要进行测试的测试文档
    test = ['love', 'my', 'dalmation']
    testVec = setOfWords2Vec(vocabList, test)
    print testVec
    classOfTest = classifyNB(testVec, p0Vect, p1Vect, pAbusive)
    print "test的类别是%s"%classOfTest
    
    test2 = ['stupid', 'garbage']
    test2Vec = setOfWords2Vec(vocabList, test2)
    classOfTest2 = classifyNB(test2Vec, p0Vect, p1Vect, pAbusive)
    print "test2的类别是%s"%classOfTest2

"""
使用贝叶斯过滤垃圾邮件
@param bigString:输入的参数是很大的string类型 
"""    
def textParse(bigString):
    import re
    #r'\W*'可以去掉除了字符和数字之外的元素
    listOfTokens = re.split(r'\W*', bigString)
    #去掉长度小于2的tok，并把tok都统一为小写
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def spamTest():
    #首先ham和spam文件夹下都是有26个txt文件的，要进行循环的读取
    docList = []; classList = []; fullText = []
    for i in range(1, 26):
        #将spam下的所有文件导入,分类为1
        wordList = textParse(open('email/spam/%d.txt'%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        #将ham下的所有文件导入，分类为0
        wordList = textParse(open('email/ham/%d.txt'%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    #训练集总共是50封邮件,随机选取10封作为测试集
    #trainingSet是训练集的下标， testSet是测试集的下标
    trainingSet = range(50); testSet = []
    for i in range(10):
        #从50个训练集中随机抽取10个作为测试集，这种方式称为留存交叉验证
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    
    #trainMat为训练矩阵
    trainMat = []; trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p1Vect, p0Vect, pClass1 = trainNB0(trainMat, trainClasses)
    
    errorCount = 0
    #测试集进行测试
    for docIndex in testSet:
        testVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        #训练集训练出来的结果用测试集的文档进行一个验证，训练出来的朴素贝叶斯得到的分类结果为classOfTest
        classOfTest = classifyNB(testVector, p0Vect, p1Vect, pClass1)
        if classOfTest != classList[docIndex]:
            errorCount += 1
            print "classification error", docList[docIndex]
    print "the error rate is:",float(errorCount)/len(testSet)

def calcMostFreq(vocabList, fullText):
    import operator
    #freqDict是记录token出现的频率的
    freqDict = {}
    for token in vocabList:
        freqDict[token]=fullText.count(token)
    #对出现的频率进行排序,出现频率最高的前30个进行返回
    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedFreq[:30]  

def localWords(feed1, feed0):
    import feedparser
    docList = []; classList = []; fullText = []
    minLen = min(len(feed1['entries']), len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    top30Words = calcMostFreq(vocabList, fullText)
    #把出现频率高的单词从vocabList中删除掉
    for pairW in top30Words:
        if pairW[0] in vocabList:vocabList.remove(pairW[0])
    #定义训练集和测试集，训练集 的长度是最小长度的二倍    
    trainingSet = range(2*minLen); testSet=[]
    #从训练集中随机选取20个作为测试集
    for i in range(20):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = [];trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p1V, p0V, pSpam = trainNB0(trainMat, trainClasses)
    errorCount = 0
    for docIndex in testSet:
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(wordVector, p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is:', float(errorCount) / len(testSet)
    return vocabList,p1V,p0V



if __name__ == "__main__":
    #main()
    #spamTest()
    ny = feedparser.parse('http://newyork.craigslist.org/search/stp?format=rss')
    sf = feedparser.parse('http://sfbay.craigslist.org/search/stp?format=rss')
    vocabList,p1V,p0V = localWords(ny, sf)
    #localWords(feed1, feed0)