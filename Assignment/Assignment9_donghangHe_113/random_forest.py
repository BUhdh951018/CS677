# -*- coding: utf-8 -*-
"""
Created on 2020/11/9 5:55 下午
@Author  : Donghang He
@FileName: random_forest.py
@Software: PyCharm
"""
import os
import traceback
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

input_dir = r'datasets'
title = 'HSBC'
input_file = os.path.join(input_dir, title + '_weekly_return_volatility.csv')
input_file1 = os.path.join(input_dir, title + '_label.csv')


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
    print('All answers are summarized in Assignment9.docx')
    try:
        # read file
        df = pd.read_csv(input_file)
        # divide the train set and test set
        df_train = df[df['Year'] == 2018]
        df_test = df[df['Year'] == 2019]
        x_train = df_train[['mean_return', 'volatility']].values
        y_train = df_train['Label'].values
        x_test = df_test[['mean_return', 'volatility']].values
        y_test = df_test['Label'].values

        # question 1
        plt.title('error rates in different N and d')
        plt.xlabel('N')
        plt.ylabel('error rate')
        # get best N and d
        for i in range(1, 6):
            error = []
            for j in range(1, 11):
                # create model
                model = RandomForestClassifier(n_estimators=j, max_depth=i, random_state=1, criterion='entropy')
                # fit model
                model.fit(x_train, y_train)
                new_instance = np.asmatrix(x_test)
                # predict
                pred = model.predict(new_instance)
                # calculate accuracy
                accuracy = np.mean(pred != y_test)
                error.append(accuracy)
            plt.plot(list(range(1, 11)), error)
            # print("d = ", i, error)
        plt.legend(['d=1', 'd=2', 'd=3', 'd=4', 'd=5'])
        plt.show()

        # question 2 d=5, n=9
        model = RandomForestClassifier(n_estimators=9, max_depth=5, random_state=1, criterion='entropy')
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        matrix = confusion_matrix(y_test, pred)
        print('confusion matrix')
        print(matrix)

        # question 3
        tpr = matrix[0][0] / (matrix[0][0] + matrix[0][1])
        tnr = matrix[1][1] / (matrix[1][0] + matrix[1][1])
        print("true positive rate is: ", tpr)
        print("true negative rate is: ", tnr)

        # question 4
        df_new = pd.read_csv(input_file1)
        df_new = df_new[df_new['Year'] == 2019]

        week_number = df_test['Week_Number'].tolist()
        week_number.append(53)

        # buy and hold strategy
        df_bh = df_new[['Open', 'Close', 'Week_Number']]
        data = np.array(df_bh)
        price = buy_and_hold(data.tolist())
        plt.plot(week_number, price, color='blue', label='buy-and-hold')
        # decision tree strategy
        price = label_price(data, pred)
        plt.plot(week_number, price, color='red', label='Random Forest')

        plt.title('portfolio growth')
        plt.xlabel('week number')
        plt.ylabel('portfolio value')
        plt.legend()
        plt.show()

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
