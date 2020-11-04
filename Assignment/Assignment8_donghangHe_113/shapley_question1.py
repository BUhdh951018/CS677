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

mo = ['Logistic Regression', 'kNN', 'Linear Regression']
title = ['mean_return', 'volatility']
# data in accuracy list
# logistic, knn, linear
# only standard deviation, only return, all
accuracy = [[], [], []]
label_train, label_test, x_test, x_train = 0, 0, 0, 0
week_close = []


def week_close_price(week, adj):
    for i in range(len(adj) - 1):
        if week[i] != week[i + 1]:
            week_close.append(adj[i])
    week_close.append(adj[len(adj) - 1])


def logistic_regression():
    prediction = lr.fit(x_train, label_train).predict(x_test)
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
    label = get_label(predict)
    acc = np.mean(label == label_test)
    accuracy[2].append(acc)


def get_label(predict):
    predict = predict.tolist()
    predict.insert(0, week_close[len(week_close) - 1])
    label = ["red"]
    for i in range(len(predict)):
        if i == 0:
            continue

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
        df_train = df[df['Year'] == 2018]
        df_test = df[df['Year'] == 2019]
        label_train = df_train['Label']
        label_test = df_test['Label']

        df_all = pd.read_csv(input_file1)
        df_all_train = df_all[df_all['Year'] == 2018]
        train_price = df_all_train['Adj Close'].tolist()
        week_number = df_all_train['Week_Number'].tolist()
        week_close_price(week_number, train_price)

        for i in range(3):
            if i != 2:
                title.pop(i)

            x_train = df_train[title]
            x_test = df_test[title]

            logistic_regression()
            knn()
            linear_model()

            title = ['mean_return', 'volatility']

        for i in range(3):
            for j in range(2):
                print(str(mo[i]) + " marginal contribution of feature " + str(title[j]) + " is: " +
                      str(round((accuracy[i][0] - accuracy[i][j + 1]) * 100, 2)) + "%")

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
