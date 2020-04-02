import csv
import os
import math
import numpy as np

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

def getClassCounts(data):
    """Counts the number of each type of example in a dataset."""
    counts = {}  # a dictionary of label -> count.
    for row in data:
        # in our dataset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts



def calculateEntropyGain(attr, uniqueVal, decision):
    atr_gain = 0
    total_data = len(decision)

    for val in uniqueVal:
        val_entropy = 0
        countY = 0; countN = 0; total = 0
        for dec, at in zip(decision, attr):
            if at == val and dec == 'No':
                countN += 1
            if at == val and dec == 'Yes':
                countY += 1
        total = countN + countY

        if countN != 0 and countY != 0:
            val_entropy = - countN/total* math.log2(countN/total) - countY/total* math.log2(countY/total)
        #print(val_entropy, "   " ,val)
        atr_gain += total/total_data * val_entropy
    return atr_gain


def makeTree(data, header, decisionDict):

    #print(decisionDict)
    pyes = decisionDict['Yes']
    pno = decisionDict['No']
    total = pyes + pno
    data_entropy = - pyes/total* math.log2(pyes/total) - pno/total* math.log2(pno/total)
    #print(data_entropy)
    gain = []
    decision = getColumnVals(data, 4)
    for i in range(len(header)-1):
        attr = getColumnVals(data, i)
        uniqueVal = getUniqueVals(data, i)
        attr_gain = calculateEntropyGain(attr, uniqueVal, decision)
        gain.append(data_entropy - attr_gain)
    retun gain


    for i in range(1,len(header)-1):
        print(i)
        data = dataDict['Rainy']
        attr = getColumnVals(data, i)
        uniqueVal = getUniqueVals(data, i)
        print(uniqueVal)
        attr_gain = calculateEntropyGain(attr, uniqueVal, decision)
        gain.append(data_entropy - attr_gain)
    print(gain)




header, data = loadData(data_file)
decisionDict = getClassCounts(data)
gain = makeTree(data, header, decisionDict)
idx = gain.index(max(gain))
uniqueVal = getUniqueVals(data, idx)
dataDict = {}
for val in uniqueVal:
    dataDict[val] = [row for row in data if row[idx]==val]
gain = []
