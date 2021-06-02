import os
import pandas as pd
import numpy as np
import numpy.matlib

def get_data(file, ball):
    os.chdir('/Users/ericzhou/Desktop/程序代码/Programming/Visual_Studio/Python/Projects/Lottery')
    data = pd.read_csv(file)
    X = []
    for number in data[ball]:
        X.append(number)
    return X


def get_transprob_matrix(X,ball):
    if ball[0] == 'r':
        matrix = np.matlib.zeros((33,33))
        total = 0
        for i in range(1,len(X)):
            matrix[X[i - 1]-1,X[i]-1] += 1
            total += 1
        matrix = matrix / total
        return matrix
    else:
        matrix = np.matlib.zeros((16,16))
        total = 0
        for i in range(1,len(X)):
            matrix[X[i - 1]-1,X[i]-1] += 1
            total += 1
        matrix = matrix / total
        return matrix

def predict_next(file,ball):
    data_list = get_data(file,ball)
    prob_matrix = get_transprob_matrix(data_list,ball)
    
    result = ball + ":\n"
    if ball[0] == 'r': 
        matrix = np.matlib.ones((1,33))
        matrix = matrix * (1/33)
        predicted = matrix * prob_matrix
        for i in range(33):
            result += str(i+1) + ": " + str(predicted[0,i]) + "\n"
    else:
        matrix = np.matlib.ones((1,16))
        matrix = matrix * (1/16)
        predicted = matrix * prob_matrix
        for i in range(16):
            result += str(i+1) + ": " + str(predicted[0,i]) + "\n"
    print(result)


# def main():
#     list_num = get_data('data.csv','b1')
#     tansprob = get_transprob_matrix(list_num,'b1')
#     print(predict_next(list_num,tansprob,'b1'))
# main()