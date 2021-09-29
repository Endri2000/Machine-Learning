import sys
import pandas as pd
import numpy as np
from numpy import genfromtxt

# take the elements in columns and map them to their occurences 
def addToDict(col,labels):
    # dictionary to map the possible values for each feature to their number of occurences in a column
    dictOccurence = {}
    # this maps the occurence of a possible outcome with one of the outcomes(there are two outcomes since its binay)
    dictTemp = {}
    # this will map every possible value of each feature with the maximum output number (if tumor size 30-39 for example had 20 recurrent and 10 nonreccurent)
    # it would map the 20 to the 30-39 feature
    dictMax = {}

    i = 0
    # array of size 2 with the possible labels 
    unique = np.unique(labels)

    # contains all instances of a possible value in a feature column
    for item in col:
        if item not in dictOccurence.keys():
            dictOccurence[item] = 1
        else:
            dictOccurence[item] += 1


    # keep track of the occurence of the first outcome for every value of the feature (we just pick the index 0 for convenience)
    for item in col:
        if labels[i] == unique[0]:
            if item not in dictTemp.keys():
                dictTemp[item] = 1
            else: 
                dictTemp[item] += 1
        
        i+=1        
        
    for item in dictTemp.keys():
        # if the count we stored in the temp dictionary is less than the other outcome (for the same value) we put the other value as max 
        if(((dictOccurence.get(item))-dictTemp.get(item))<dictTemp.get(item)):
            dictMax[item] = dictTemp.get(item)
        else:
            dictMax[item] =dictOccurence.get(item)-dictTemp.get(item)
    i = 0
    return dictMax
         


def main():
    inFile = sys.argv[1]
    print(inFile)

    df = pd.read_csv (inFile)
    data = df.to_numpy()
    last_col = len(data[0])-1

    labels = data[0:,last_col]
    # # # Read input file and save attribute names
    attr_names = []
    label_name = []
    i = 0

    for col in df.columns:
        i += 1
        if i == (last_col+1):
            label_name.append(col)
            break
        attr_names.append(col)
        
    num_attr = len(attr_names)
    attr_train_err  = []

    for i in range(num_attr):
        column =  data[0:,i]
        colSize = len(column)
        dic = addToDict(column,labels)
        correct = 0 
        for item in dic:
            correct += dic[item]
        incorrect = (colSize-correct)
        attr_train_err.append((1-(correct/colSize))*100)


    # Print out the results
    for attr, err in zip(attr_names, attr_train_err):
        print("Attribute: {}, Training Error: {}".format(attr, round(err, 2)))

if __name__ == "__main__":
    main()