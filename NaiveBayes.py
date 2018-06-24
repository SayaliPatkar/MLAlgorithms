import csv
import os
import math
import numpy as np

"""
Class uses naive bayes algorithm to predict whether to play golf or not using
data from tennis.csv and given test examples
For greater understanding of how Naive Bayes works internally i have written
logic to calculate priors, likelihood and predicator

Easy Way Out
from sklearn.naive_bayes import GaussianNB
model.fit(X, y)
#Predict Output
predicted= model.predict(x_test)
"""
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
data_file = os.path.join(script_dir, "Resources/tennis.csv")


def loadData(data_file:str):
    data = []
    file = open(data_file)
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

    attributes = data[0]
    data.remove(attributes)
    return attributes, data

def getUniqueVals(data, column):
    return set(entry[column] for entry in data)

def getColumnVals(data, column):
    return [entry[column] for entry in data]

def getdecisionCounts(decision):
    """Counts the number of each type of decision in a dataset."""
    countY = 0; countN = 0
    for row in decision:
        # in our dataset format, the label is always the last column
        if row == 'No':
            countN += 1
        else :
            countY += 1
    return countY, countN

def getClassCounts(column, uniqueVal, decision, yes, no , total):
    """Counts the number of each type of example in a dataset."""
    dataDict = {}  # a dictionary of labels
    for val in uniqueVal:
        label1 = val + '/Y'
        label2 = val + '/N'
        dataDict[label1] = 0; dataDict[label2]  = 0
        for dec, at in zip(decision, column):
            if at == val and dec == 'No':
                dataDict[label2] += 1
            if at == val and dec == 'Yes':
                dataDict[label1] += 1
        dataDict[val] = (dataDict[label2]+ dataDict[label1])/ total
        dataDict[label2] = dataDict[label2] / no
        dataDict[label1] = dataDict[label1] / yes
    return dataDict

header, data = loadData(data_file)
decision = getColumnVals(data, -1)
yes, no = getdecisionCounts(decision)
total = yes + no
probDict = {}
for i in range(len(header)-1):
    column = getColumnVals(data, i)
    uniqueVal = getUniqueVals(data, i)
    dataDict = getClassCounts(column, uniqueVal, decision, yes, no , total)
    probDict.update(dataDict)

print(probDict)
# in probDict Sunny/Y + Overcast/Y + rainy/Y = 1
# Sunny/N + Overcast/N + rainy/N = 1
# sunny + overcast + rainy = 1
# similarly check forother attribute
X = ['Sunny','Mild', 'High','FALSE']
pX = probDict['Sunny'] * probDict['Mild'] * probDict['High']* probDict['False']
# to find play or no play
pYesGivnSunny = probDict['Sunny/Y']
pYesGivnMild = probDict['Mild/Y']
pYesGivnHigh = probDict['High/Y']
pYesGivnFalse = probDict['False/Y']
pYes = yes/total

pYesGivnX = pYesGivnSunny * pYesGivnMild * pYesGivnHigh * pYesGivnFalse * pYes / pX
print(pYesGivnX)

pNoGivnSunny = probDict['Sunny/N']
pNoGivnMild = probDict['Mild/N']
pNoGivnHigh = probDict['High/N']
pNoGivnFalse = probDict['False/N']
pNo = no/total

pNoGivnX = pNoGivnSunny * pNoGivnMild * pNoGivnHigh * pNoGivnFalse * pNo / pX
print(pNoGivnX)
if pYesGivnX > pNoGivnX:
    print("For given feature x =",X," player will play")
else:
    print("For given feature x =",X," player will NOT play")

X = ['Sunny','Cool', 'High','True']
pX = probDict['Sunny'] * probDict['Cool'] * probDict['High']* probDict['True']

pYesGivnSunny = probDict['Sunny/Y']
pYesGivnCool = probDict['Cool/Y']
pYesGivnHigh = probDict['High/Y']
pYesGivnTrue = probDict['True/Y']
pYes = yes/total

pYesGivnX = pYesGivnSunny * pYesGivnCool * pYesGivnHigh * pYesGivnTrue * pYes / pX
print(pYesGivnX)

pNoGivnSunny = probDict['Sunny/N']
pNoGivnCool = probDict['Cool/N']
pNoGivnHigh = probDict['High/N']
pNoGivnTrue = probDict['True/N']
pNo = no/total

pNoGivnX = pNoGivnSunny * pNoGivnCool * pNoGivnHigh * pNoGivnTrue * pNo / pX
print(pNoGivnX)
if pYesGivnX > pNoGivnX:
    print("For given feature x =",X," player will play")
else:
    print("For given feature x =",X," player will NOT play")
