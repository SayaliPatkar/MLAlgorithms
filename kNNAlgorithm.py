# linear algebra
import numpy as np
#data processing
import pandas as pd
#%matplotlib notebook
import matplotlib.pyplot as plt
#Split Data
from sklearn.model_selection import train_test_split
#Plot Confusion Matrix
from sklearn.metrics import confusion_matrix
import seaborn as sn

data = pd.read_csv("./Resources/Iris.csv")

y = np.array(data[['Species']])
x = np.array(data.drop(['Id','Species'], axis=1))
data.head(10)

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.33, stratify=y)
print(y_train.shape)
print(x_train.shape)
print(y_test.shape)
print(x_test.shape)

def assessWithPlots(x_train, y_train) :
    Iris_virginica_sl = []; Iris_virginica_sw = []; Iris_virginica_pl = []
    Iris_virginica_pw = []; Iris_setosa_sl = []; Iris_setosa_sw = []
    Iris_setosa_pl = []; Iris_setosa_pw = []; Iris_versicolor_sl = []
    Iris_versicolor_sw = []; Iris_versicolor_pl = []; Iris_versicolor_pw = []

    for type,row in zip(y_train, x_train):
        if type[0] == 'Iris-virginica':
            Iris_virginica_sl.append(row[0])
            Iris_virginica_sw.append(row[1])
            Iris_virginica_pl.append(row[2])
            Iris_virginica_pw.append(row[3])
        if type[0] == 'Iris-setosa':
            Iris_setosa_sl.append(row[0])
            Iris_setosa_sw.append(row[1])
            Iris_setosa_pl.append(row[2])
            Iris_setosa_pw.append(row[3])
        if type[0] == 'Iris-versicolor':
            Iris_versicolor_sl.append(row[0])
            Iris_versicolor_sw.append(row[1])
            Iris_versicolor_pl.append(row[2])
            Iris_versicolor_pw.append(row[3])


    fig = plt.figure()
    pl1 = fig.add_subplot(1,2,1)
    a = pl1.plot(Iris_virginica_sl,Iris_virginica_sw, 'ro', label='Iris virginica')
    b = pl1.plot(Iris_setosa_sl,Iris_setosa_sw, 'go', label = 'Iris setosa')
    c = pl1.plot(Iris_versicolor_sl,Iris_versicolor_sw, 'bo',label = 'Iris versicolor')
    pl1.set_xlabel('Sepal Length')
    pl1.set_ylabel('Sepal Width')
    pl1.legend()

    pl2 = fig.add_subplot(1,2,2)
    pl2.plot(Iris_virginica_pl,Iris_virginica_pw, 'ro', label='Iris virginica')
    pl2.plot(Iris_setosa_pl,Iris_setosa_pw, 'go', label = 'Iris setosa')
    pl2.plot(Iris_versicolor_pl,Iris_versicolor_pw, 'bo',label = 'Iris versicolor')
    pl2.set_xlabel('Petal Length')
    pl2.set_ylabel('Petal Width')
    pl2.legend()
    plt.show()

assessWithPlots(x_train,y_train)

def getEuclidianDistance(dataPoint, testPoint):
    dist = np.sqrt(np.sum((dataPoint - testPoint)**2, axis = 0))
    return dist
print(x_train[0] , x_train[1])
getEuclidianDistance(x_train[0], x_train[1])

def getKey(item):
    return item[1]

def getNeighbours(x_train, y_train, num_neighbours, test_point):
    distances = []
    for row,value in zip(x_train,y_train):
        dist = getEuclidianDistance(row, test_point)
        distances.append([value[0], dist])
    distances.sort(key=getKey)
    neighbours= []
    for num in range (num_neighbours):
        neighbours.append(distances[num])
    #print(neighbours)
    return neighbours

getNeighbours(x_train, y_train, 4, x_test[0])

def predict(x_train, y_train, x_test):
    predictions =[]
    k_neighbours = 5
    for testPoint in x_test:
        neighbours = getNeighbours(x_train, y_train, k_neighbours, testPoint)
        count_setosa = count_virginica = count_versicolor = 0
        for i in neighbours:
            if i[0] =='Iris-virginica':
                count_virginica += 1
            elif i[0] == 'Iris-setosa':
                count_setosa += 1
            else :
                count_versicolor += 1
        if count_setosa > count_virginica and count_setosa > count_versicolor:
            predictions.append('Iris-setosa')
        elif  count_setosa < count_virginica and count_virginica > count_versicolor:
            predictions.append('Iris-virginica')
        else :
            predictions.append('Iris-versicolor')
    return predictions

predictions = predict(x_train, y_train, x_test)
accuracy = 0
for prediction, test_value in zip (predictions, y_test):
    if prediction == test_value:
        accuracy +=1
    print (prediction ,"for true value ", test_value, prediction == test_value)
print(accuracy)
print(accuracy/y_test.shape[0])

cm = confusion_matrix(y_test, predictions)
df_cm = pd.DataFrame(cm, index = [i for i in np.unique(y_train)],
                  columns = [i for i in np.unique(y_train)])
plt.figure(figsize = (5,5))
sn.heatmap(df_cm, annot=True)
plt.show()
