import operator
labels = ['A','A','B','B']
k=3
classCount = {}
for i in range(k):
    real_labels = labels[i]
    classCount[real_labels] = classCount.get(real_labels, 0) + 1
    print classCount
for e in classCount.iteritems():
    print e 
print classCount.items()
sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1))
print sortedClassCount



f = open('datingTestSet2.txt')
str = f.readlines()
print str


str = '  a  b    c d       '
print str.strip().split()


import numpy as np
x = np.zeros((3, 4)) 
print x
m = x.shape[0]
print m



