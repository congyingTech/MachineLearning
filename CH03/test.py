#-*-coding:utf-8-*-
list = ['cute', 'love', 'help', 'garbage', 'quit', 'I', 'problems', 'is', 'park', 'stop', 'flea', 'dalmation', 'licks', 'food', 'not', 'him', 'buying', 'posting', 'has', 'worthless', 'ate', 'to', 'maybe', 'please', 'dog', 'how', 'stupid', 'so', 'take', 'mr', 'steak', 'my']
word = 'stop'
list[list.index(word)]=1
list1 = [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
list2 = [1,2,3]
dict1 = {1:'1',2:'2',3:'3'}
for e in dict1:
    print e
    print e[0]
    #if e[0] in list2:list2.remove(e[0]) 

print sum(list1)