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

title = ['mean_return', 'volatility']
# data in accuracy list
# logistic, knn, linear
# only standard deviation, only return, all
accuracy = [[], [], []]
label_train, label_test, x_test, x_train = 0, 0, 0, 0


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


'''
def linear_model(df):
    x = np.array(df).reshape(-1, 1)
    y = 
'''


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
        x_all_train = df_all_train['Adj Close']

        for i in range(3):
            if i != 2:
                title.pop(i)

            x_train = df_train[title]
            x_test = df_test[title]

            logistic_regression()
            knn()
            # linear_model(df_train['Week_Number'])

            title = ['mean_return', 'volatility']

        print(accuracy)

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
