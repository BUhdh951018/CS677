# -*- coding: utf-8 -*-
"""
Created on 2020/11/2 5:49 下午
@Author  : Donghang He
@FileName: tips.py.py
@Software: PyCharm
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import traceback
time = ['Lunch', 'Dinner']
label = 'tip_percent_of_meal'
le = LabelEncoder()


def avg_tip_time(df):
    # loop 2 times for lunch and dinner
    for i in range(2):
        # calculate the mean
        avg_tip = df.loc[df.time == time[i]].tip_percent_of_meal.mean()
        print("Average tip for " + str(time[i]) + " is " + str(round(avg_tip, 2)))


def average(df, col):
    # calculate the mean for each day of the week
    result = df.groupby(col)[label].mean()
    print(result)


def corr(df, col):
    print("correlation matrix")
    # use numpy corr function to calculate the correlation matrix of question 8
    if col[1] == 'smoker':
        # transform label
        y = le.fit_transform(df[col[1]])
        cr = np.corrcoef(df[col[0]], y)
        print(cr)
        return
    # calculate the correlation matrix
    cor = df[col].corr()
    print(cor)


def smoke_people(df):
    # select the smoke people
    df_smoke = df[df['smoker'] == 'Yes']
    # calculate the percentage
    result = len(df_smoke) / len(df)
    print("percentage of people are smoking is", round(result, 4))


def tip_increase(df):
    # plot the chart to check whether increase
    plt.figure()
    df.groupby(['day'])['tip'].plot(legend=True)
    plt.show()


def main():
    try:
        df = pd.read_csv('datasets/tips.csv')
        # add column average tip as a percentage of meal cost
        df[label] = df['tip'] / df['total_bill'] * 100
        print('All answers are summarized in Assignment8.docx')
        # question 1
        print('Question 1:')
        avg_tip_time(df)
        # question 2
        print('Question 2:')
        average(df, ['day'])
        # question 3
        print('Question 3:')
        average(df, ['day', 'time'])
        # question 4
        print('Question 4:')
        corr(df, ['tip', 'total_bill'])
        # question 5
        print('Question 5:')
        corr(df, ['tip', 'size'])
        # question 6
        print('Question 6:')
        smoke_people(df)
        # question 7
        print('Question 7:')
        tip_increase(df)
        # question 8
        print('Question 8:')
        corr(df, ['tip', 'smoker'])

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
