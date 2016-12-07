#-*- coding:utf-8 -*-
import trees
import treePlotter

dataSet, labels = trees.creatDataSet()
myTree = trees.createTree(dataSet, labels)
trees.storeTree(myTree, 'classifierStorage.txt')
print trees.grabTree('classifierStorage.txt')

fr = open('lenses.txt')
lensesData=[line.strip().split('\t') for line in fr.readlines()]
lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
lensesTree = trees.createTree(lensesData, lensesLabels)
treePlotter.createPlot(lensesTree)


