#-*-coding:utf-8-*-
from math import log
import operator
#计算香农熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    #计算每个label出现的次数
    for featVec in dataSet:
        #最后一列值属于分类标签
        currentLabel = featVec[-1]
        #如果当前的标签还没有被加入到labelCount里面,就将label加入并初始化计数器为0
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        #算label出现的概率
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob*log(prob, 2)
    return shannonEnt

#创建数据集
def creatDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    #labels是特征标签
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

#划分数据集:参数axis是划分特征的选定，选定第几个特征作为划分依据，value是划分的特征值
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    #将选定的特征值从这一行中删除
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

#选定最优的特征值
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0])#dataSet的列数
    #计算原始熵
    baseEntropy = calcShannonEnt(dataSet)
    #初始化最佳熵差值，和最佳特征
    bestInfoGain = 0.0;bestFeature = -1
    for i in range(numFeatures):
        #featList是第i列的所有值，也就是选取第i个特征的所有特征值
        featList = [example[i] for example in dataSet]
        #保证特征值的唯一性，用set去重
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            #第i个特征，循环遍历特征值，进行划分特征子集
            subDataSet = splitDataSet(dataSet, i, value)
            #根据子集在总集合中出现的概率与子集信息熵的乘积进行相加
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob*calcShannonEnt(subDataSet)
        #划分数据集的最大原则是：将无序的数据变得更加有序，在划分数据集前后的信息发生的
        #变化叫做信息增益，获得信息增益最高的特征就是最好的选择。
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature
#多数表决法决定叶子节点的分类
def majorityCnt(classList):
    classCount = {}
    #对分类进行统计
    for vote in classList:
        if vote not in classCount.keys():classCount[vote] = 0
        classCount[vote] += 1
    #对classCount字典按值进行排序
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

#主方法：递归构建决策树
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    #第一个递归停止的条件是：所有的类标签完全相同，直接返回该类标签
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    #第二个递归停止的条件是：使用完了所有特征，仍不能将数据集划分成仅包含唯一类别的分组，就
    #返回多数表决法出现次数最多的特征
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)   
    #首先找出最佳的特征值，这个特征值是作为树的根节点的。
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    #将已经进入树中的特征值删除，进行递归
    del(labels[bestFeat])
    #将最佳特征所在的列元素全部存储到featValues中
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree   

# 辅助方法
def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict): 
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else: classLabel = valueOfFeat
    return classLabel

#决策树的存储，使用pickle进行序列化
def storeTree(inputTree,filename):
    import pickle
    fw = open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()
    
def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

#if __name__ == "__main__":
   # dataSet, labels = creatDataSet()
   # print dataSet
   # print labels
   # print chooseBestFeatureToSplit(dataSet)
   # print createTree(dataSet, labels)

