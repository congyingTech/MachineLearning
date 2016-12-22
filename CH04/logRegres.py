#-*-coding:utf-8-*-
from numpy import *
import matplotlib.pyplot as plt

#整个过程是：将输入的data先转化为mat，然后进行预测分类，其中涉及到sigmoid函数和梯度上升法求最大值
#sigmoid函数是y在0-1之间的函数，而且不像越阶函数似的，它是连续的，h是每次迭代时根据数据对结果的预测，然后算出每次迭代的error，最终得到weights
def loadDataSet():
    dataMat = []; labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))
                
#首次用到mat矩阵，矩阵和数组不同之处在于矩阵相乘和数组相乘的规则是不同的
def gradAscent(dataMatIn, classLabels):
    #dataMatrix是m行3列矩阵
    dataMatrix = mat(dataMatIn)
    #转置矩阵，labelMat成了m行1列矩阵
    labelMat = mat(classLabels).transpose()
    m,n = shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    #weights是三行一列的全1矩阵
    weights = ones((n,1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix*weights)
        #error是m行1列的矩阵，是真是类别labelMat与预测类别h的差值
        #dataMatrix是m行3列的矩阵，转置成3行m列，并与error矩阵相乘，得到了与weights矩阵一样是3行1列的矩阵
        error=(labelMat - h)
        #alpha是目标移动步长，maxCycles是迭代次数
        weights = weights + alpha * dataMatrix.transpose() * error
    #weights是训练好的回归系数
    return weights
def plotBestFit(weights):
    dataMat, labelMat = loadDataSet()
    dataArr = array(dataMat)
    #得到矩阵的行数
    n = shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i ,1]); ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1]); ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0]-weights[1]*x) / weights[2]
    ax.plot(x, y)
    plt.xlabel('X1'); plt.ylabel('X2');
    plt.show()  

#随机梯度上升法，当数据量大的时候，就不能进行500次迭代了，所以就简化了迭代操作  
#dataMatrix是数组而非矩阵，所以不需要进行mat的转换 
def stocGradAscent0(dataMatrix, classLabels):
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)   #initialize to all ones
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i]*weights))
        #error也不再是矩阵，而是数字
        error = classLabels[i] - h
        weights = weights + alpha * error * dataMatrix[i]
    return weights
   
#改进的随机梯度上升法，加上了迭代次数150次
def stocGradAscent1(dataMatrix, classLabels, numIter = 150):
    m,n = shape(dataMatrix)
    weights = ones(n)   #initialize to all ones
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            #1)alpha是一处变动：会随着迭代次数不断的变小
            alpha = 4/(1.0+j+i) + 0.0001
            #2)增加此处的意义在于随机选取样本来更新回归系数，这种将减少周期性波动
            randIndex = int(random.uniform(0, len(dataIndex))) 
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha*error*dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights

def classifyVector(inX, weights):
    prob = sigmoid(sum(inX*weights))
    if prob > 0.5:return 1.0
    else:return 0.0

def colicTest():
    frTrain = open('horseColicTraining.txt');frTest = open('horseColicTest.txt')
    trainingSet = []; trainingLabels = []
    
    

if __name__ =="__main__":
    dataMatIn, classLabels = loadDataSet()
    #梯度上升法
    weights = gradAscent(dataMatIn, classLabels)
    print weights
    #getA是返回矩阵对应的数组
    #print type(weights)
    #print type(weights.getA())
    plotBestFit(weights.getA())
    #随机梯度上升法，由图像可得，显然随机梯度上升法得到的数据误差更大一点
    weights1 = stocGradAscent0(array(dataMatIn), classLabels)
    print weights1
    plotBestFit(weights1)
    #改进型的随机梯度上升法
    weights2 = stocGradAscent1(array(dataMatIn), classLabels)
    print weights2
    plotBestFit(weights2)
    
