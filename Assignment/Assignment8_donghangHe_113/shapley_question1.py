# -*- coding: utf-8 -*-
"""
Created on 2020/11/2 11:03 下午
@Author  : Donghang He
@FileName: shapley_question1.py
@Software: PyCharm
"""
import os
import traceback
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier

input_dir = r'datasets'
title = 'HSBC'
input_file = os.path.join(input_dir, title + '_weekly_return_volatility.csv')
input_file1 = os.path.join(input_dir, title + '_label.csv')

sc = StandardScaler()
lr = LogisticRegression()
model = LinearRegression(fit_intercept=True)
knn_classifier = KNeighborsClassifier(n_neighbors=7)
# three model name
mo = ['Logistic Regression', 'kNN', 'Linear Regression']
# two features
title = ['mean_return', 'volatility']
# data in accuracy list
# logistic, knn, linear
# only standard deviation, only return, all
accuracy = [[], [], []]
label_train, label_test, x_test, x_train = 0, 0, 0, 0
# week close price in 2018
week_close = []


# get the week close price in 2018 and save in list
def week_close_price(week, adj):
    for i in range(len(adj) - 1):
        if week[i] != week[i + 1]:
            week_close.append(adj[i])
    week_close.append(adj[len(adj) - 1])


def logistic_regression():
    lr.fit(x_train, label_train)
    prediction = lr.predict(x_test)
    acc = np.mean(prediction == label_test)
    accuracy[0].append(acc)


def knn():
    global x_train
    x_train = sc.fit(x_train).transform(x_train)
    knn_classifier.fit(x_train, label_train)
    pred_k = knn_classifier.predict(x_test)
    acc = np.mean(pred_k == label_test)
    accuracy[1].append(acc)


def linear_model():
    model.fit(x_train, week_close)
    predict = model.predict(x_test)
    # transform the predict week adj price to label
    label = get_label(predict)
    acc = np.mean(label == label_test)
    accuracy[2].append(acc)


def get_label(predict):
    predict = predict.tolist()
    # insert the last week adj price of 2018 to compare with the first predict price in 2019
    predict.insert(0, week_close[len(week_close) - 1])
    # insert the last week label of 2018
    label = ["green"]
    for i in range(len(predict)):
        if i == 0:
            continue
        # set label strategy
        if predict[i] > predict[i - 1]:
            label.append("green")
        elif predict[i] < predict[i - 1]:
            label.append("red")
        else:
            label.append(label[i - 1])
    label.pop(0)
    return label


def main():
    global label_train, label_test, x_train, x_test, title
    try:
        print('All answers are summarized in Assignment8.docx')
        df = pd.read_csv(input_file)
        # divide train set and test set
        df_train = df[df['Year'] == 2018]
        df_test = df[df['Year'] == 2019]
        label_train = df_train['Label']
        label_test = df_test['Label']
        # read another file to get the Adj close in 2018
        df_all = pd.read_csv(input_file1)
        df_all_train = df_all[df_all['Year'] == 2018]
        train_price = df_all_train['Adj Close'].tolist()
        week_number = df_all_train['Week_Number'].tolist()
        week_close_price(week_number, train_price)
        # loop three time for three model
        for i in range(3):
            # remove feature
            if i != 2:
                title.pop(i)
            # set x_train and x_test
            x_train = df_train[title]
            x_test = df_test[title]

            logistic_regression()
            knn()
            linear_model()
            # reset the title
            title = ['mean_return', 'volatility']

        for i in range(3):
            for j in range(2):
                print(str(mo[i]) + " marginal contribution of feature " + str(title[j]) + " is: " +
                      str(round((accuracy[i][2] - accuracy[i][j]) * 100, 2)) + "%")
        print(accuracy)

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
