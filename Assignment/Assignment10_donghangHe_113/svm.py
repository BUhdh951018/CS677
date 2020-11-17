# -*- coding: utf-8 -*-
"""
Created on 2020/11/16 6:51 下午
@Author  : Donghang He
@FileName: svm.py
@Software: PyCharm
"""

import os
import traceback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix

input_dir = r'datasets'
title = 'HSBC'
input_file = os.path.join(input_dir, title + '_weekly_return_volatility.csv')
input_file1 = os.path.join(input_dir, title + '_label.csv')

svm_classifier = svm.SVC(kernel='linear')
svm_classifier_g = svm.SVC(kernel='rbf')
svm_classifier_p = svm.SVC(kernel='poly', degree=2)
sc = StandardScaler()


def buy_and_hold(data):
    price = [100]
    length = len(data)
    # two variables for the open price and end price of the green week
    begin, end = data[0][0], 0
    # variable for check the week number
    week_number = 100
    # loop each days in year 2019 to calculate the final price
    for i in range(length):
        # first check the current week whether same to the week of this day
        if week_number != int(data[i][2]):
            # if not update the week number and set the open price
            week_number = int(data[i][2])
        # last day of the year calculate the final price and break
        if i + 1 == length:
            end = data[i][1]
            # calculate the last week price
            price.append(end / begin * 100)
            break
        # end day of week update the price
        if week_number != int(data[i + 1][2]):
            end = data[i][1]
            # calculate the week price, because I'm not out of the market
            # so the price will be end/begin * 100
            price.append(end / begin * 100)

    return price


def label_price(data, label):
    price = [100]
    length = len(data)
    # two variables for the open price and end price of the green week
    begin, end = 0, 0
    week_number = 100
    # flag for whether in the market
    flag = False
    temp_price = 100
    # loop each days in year 2019 to calculate the final price
    for i in range(length):
        # first check the current week whether same to the week of this day
        if week_number != int(data[i][2]):
            # if not update the week number
            week_number = int(data[i][2])

            # last day of the year calculate the final price and break
            if i + 1 == length:
                end = data[i][1]
                price.append(end / begin * temp_price)
                break

            # if today is red day, also it must be the first day of the red week
            # so set the price and jump to next loop
            if label[week_number] == 'red':
                price.append(price[week_number])
                flag = False
                continue
            # else it must be the first day of green week so set the open price
            else:
                if flag is False:
                    begin = data[i][0]
                    flag = True
                    temp_price = price[week_number - 1]

        # or in the same week
        else:
            # red day jump
            if label[week_number] == 'red':
                continue
            # last day of the year calculate the final price and break
            if i + 1 == length:
                end = data[i][1]
                price.append(end / begin * temp_price)
                break
            # end day of green week update the price
            if week_number != int(data[i + 1][2]):
                end = data[i][1]
                price.append(end / begin * temp_price)

    return price


def main():
    try:
        print("all answer shown in the doc file assignment10.docx")
        df = pd.read_csv(input_file)
        df_train = df[df['Year'] == 2018]
        df_test = df[df['Year'] == 2019]

        x_train = df_train[['mean_return', 'volatility']].values
        y_train = df_train['Label'].values
        x_train = sc.fit(x_train).transform(x_train)
        x_test = df_test[['mean_return', 'volatility']].values
        y_test = df_test['Label'].values
        x_test = sc.fit(x_test).transform(x_test)

        # question 1
        svm_classifier.fit(x_train, y_train)
        predicted = svm_classifier.predict(np.asmatrix(x_test))
        accuracy = np.mean(predicted == y_test)
        print("Accuracy of SVM for year 2 is ", accuracy)

        # question 2
        matrix = confusion_matrix(y_test, predicted)
        print('confusion matrix')
        print(matrix)

        # question 3
        tpr = matrix[0][0] / (matrix[0][0] + matrix[0][1])
        tnr = matrix[1][1] / (matrix[1][0] + matrix[1][1])
        print("true positive rate is: ", tpr)
        print("true negative rate is: ", tnr)

        # question 4
        svm_classifier_g.fit(x_train, y_train)
        pred_g = svm_classifier_g.predict(x_test)
        accuracy_g = np.mean(y_test == pred_g)
        print("Accuracy of Gaussian SVM for year 2 is ", accuracy_g)

        # question 5
        svm_classifier_p.fit(x_train, y_train)
        pred_p = svm_classifier_p.predict(x_test)
        accuracy_p = np.mean(y_test == pred_p)
        print("Accuracy of polynomial SVM for year 2 is ", accuracy_p)

        # question 6
        # read another file with weekly open and close price
        df_new = pd.read_csv(input_file1)
        # select 2019 data for plot the chart
        df_new = df_new[df_new['Year'] == 2019]
        # set the week number and add another week, because the first week is 100
        week_number = df_test['Week_Number'].tolist()
        week_number.append(53)

        # buy and hold strategy
        df_bh = df_new[['Open', 'Close', 'Week_Number']]
        data = np.array(df_bh)
        price = buy_and_hold(data.tolist())
        print("final price ", price[-1])
        plt.plot(week_number, price, color='blue', label='buy-and-hold')
        # svm strategy
        price = label_price(data, predicted)
        print("final price ", price[-1])
        plt.plot(week_number, price, color='red', label='linear SVM')

        plt.title('portfolio growth')
        plt.xlabel('week number')
        plt.ylabel('portfolio value')
        plt.legend()
        plt.show()

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
