# -*- coding: utf-8 -*-
"""
Created on 2020/11/16 9:48 下午
@Author  : Donghang He
@FileName: method.py
@Software: PyCharm
"""
import os
import pandas as pd
import numpy as np
import traceback

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm, tree
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA

sc = StandardScaler()
le = LabelEncoder()

knn_classifier = KNeighborsClassifier(n_neighbors=7)
logistic_classifier = LogisticRegression()
nb_classifier = GaussianNB()
clf = tree.DecisionTreeClassifier(criterion='entropy')
model = RandomForestClassifier(n_estimators=9, max_depth=5, random_state=1, criterion='entropy')
lda_classifier = LDA()
qda_classifier = QDA()
svm_classifier = svm.SVC(kernel='linear')

ticker = 'HSBC'
input_dir = r'datasets'
input_file = os.path.join(input_dir, ticker + '_weekly_return_volatility.csv')
input_file1 = os.path.join(input_dir, ticker + '_label.csv')

try:
    df = pd.read_csv(input_file)
    df_train = df[df['Year'] == 2018]
    df_test = df[df['Year'] == 2019]

    # train set
    x_train = df_train[['mean_return', 'volatility']].values
    y_train = df_train['Label'].values
    x_train_sc = sc.fit(x_train).transform(x_train)
    # test set
    x_test = df_test[['mean_return', 'volatility']].values
    y_test = df_test['Label'].values
    x_test_sc = sc.fit(x_test).transform(x_test)

    # read another file with weekly open and close price
    df_new = pd.read_csv(input_file1)
    # select 2019 data for plot the chart
    df_new = df_new[df_new['Year'] == 2019]
    # set the week number and add another week, because the first week is 100
    week_number = df_test['Week_Number'].tolist()
    week_number.append(53)


except Exception as e:
    print(e)
    print(traceback.format_exc())


def acc(predict, name):
    accuracy = np.mean(predict == y_test)
    print("Accuracy of", name, "for year 2 is", round(float(accuracy), 3))


def buy_and_hold(data):
    price = [100]
    length = len(data)
    # two variables for the open price and end price of the green week
    begin, end = data[0][0], 0
    # variable for check the week number
    week_number_cur = 100
    # loop each days in year 2019 to calculate the final price
    for i in range(length):
        # first check the current week whether same to the week of this day
        if week_number_cur != int(data[i][2]):
            # if not update the week number and set the open price
            week_number_cur = int(data[i][2])
        # last day of the year calculate the final price and break
        if i + 1 == length:
            end = data[i][1]
            # calculate the last week price
            price.append(end / begin * 100)
            break
        # end day of week update the price
        if week_number_cur != int(data[i + 1][2]):
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
    week_number_cur = 100
    # flag for whether in the market
    flag = False
    temp_price = 100
    # loop each days in year 2019 to calculate the final price
    for i in range(length):
        # first check the current week whether same to the week of this day
        if week_number_cur != int(data[i][2]):
            # if not update the week number
            week_number_cur = int(data[i][2])
            # last day of the year calculate the final price and break
            if i + 1 == length:
                end = data[i][1]
                price.append(end / begin * temp_price)
                break
            # if today is red day, also it must be the first day of the red week
            # so set the price and jump to next loop
            if label[week_number_cur] == 'red':
                price.append(price[week_number_cur])
                flag = False
                continue
            # else it must be the first day of green week so set the open price
            else:
                if flag is False:
                    begin = data[i][0]
                    flag = True
                    temp_price = price[week_number_cur - 1]
        # or in the same week
        else:
            # red day jump
            if label[week_number_cur] == 'red':
                continue
            # last day of the year calculate the final price and break
            if i + 1 == length:
                end = data[i][1]
                price.append(end / begin * temp_price)
                break
            # end day of green week update the price
            if week_number_cur != int(data[i + 1][2]):
                end = data[i][1]
                price.append(end / begin * temp_price)

    return price
