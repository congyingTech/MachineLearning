#-*-coding:utf-8-*-
from numpy import *
import operator
import matplotlib.pyplot as plt

def file2matrix(filename):
    fr = open(filename)
    contents = fr.readlines()
    numberOfLines = len(contents)
    #零矩阵numberOfLinesh行3列
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    index = 0
    for line in contents:
        line = line.strip()#strip删除首尾的空白符'\n', '\r',  '\t',  ' '
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        #分类的标签
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector

def createDataSet():
    #array 和 matrix是不一样的
    group = array([[1.0, 1.1],[1.0, 1.0],[0, 0],[0,0.1]])
    labels = ['A' ,'A', 'B', 'B']
    return group, labels

#inX是输入向量
def classify0(inX, dataSet, labels, k):
    #c.shape获得数组的大小,dataSet.shape = (4,2) 因为dataSet是4行两列的数据集
    #dataSet.shape[0]得出的是数据集 的行数
    dataSetSize = dataSet.shape[0]
    #numpy.tile(A, reps)-->Construct an array by repeating A the number of times given by reps.
    #具体的tile的使用方法在笔记里
    #下面的是求欧式距离公式：                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistance = sqDiffMat.sum(axis = 1)
    distances = sqDistance ** 0.5                                         
    print distances
    #对distances进行排序，argsort返回的是按照从小到大的序列的数字的下标的排序
    sortedDistIndicies = distances.argsort()
    #test
    print sortedDistIndicies
    
    classCount = {}
    #选出前k个元素
    for i in range(k):
        #选取出k个主要的标签
        voteIlabel = labels[sortedDistIndicies[i]]
        #对voteIlabel进行计数
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    #对classCount的第二个域进行排序,也就是计数的值,要把classCount变为可以iterate的iterator,例如，A出现2次，B出现1次，就把A选出来
    sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse = True)
    #将出现频率最高的return，那就是类别
    return sortedClassCount[0][0]  

def autoNorm(dataSet):
    minVals = dataSet.min(0)  
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    #与dataSet有相同行列的零向量
    normDataSet = zeros(shape(dataSet))
    #m是行数
    m = normDataSet.shape[0]
    #将最小minVals重复m行1次
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet/tile(ranges, (m, 1))
    return normDataSet, ranges, minVals
        
        
if __name__ == "__main__":
    #group,labels = createDataSet()
    #print classify0([0,0], group, labels, 3)        
    
    dataSet, labels = file2matrix('datingTestSet2.txt')
    #把数据归一化
    normDataSet, ranges, minVals = autoNorm(dataSet)
    print dataSet
    print labels
    print 40*'-'
    print normDataSet
    fig = plt.figure()
    fig2 = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax2 = fig2.add_subplot(1,1,1)
    ax.scatter(dataSet[:,0], dataSet[:,1], 15.0*array(labels), 15.0*array(labels))
    ax2.scatter(normDataSet[:,0], normDataSet[:,1], 15.0*array(labels), 15.0*array(labels))
    plt.show()                                                                                                    