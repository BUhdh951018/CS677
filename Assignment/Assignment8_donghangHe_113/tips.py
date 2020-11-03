# -*- coding: utf-8 -*-
"""
Created on 2020/11/2 5:49 下午
@Author  : Donghang He
@FileName: tips.py.py
@Software: PyCharm
"""

import pandas as pd
import matplotlib.pyplot as plt
import traceback
time = ['Lunch', 'Dinner']
label = 'tip_percent_of_meal'


def avg_tip_time(df):
    for i in range(2):
        avg_tip = df.loc[df.time == time[i]].tip_percent_of_meal.mean()
        print("Average tip for " + str(time[i]) + " is " + str(round(avg_tip, 2)))


def avg_tip_day(df):
    result = df.groupby(['day'])[label].mean()
    print(result)


def tip_highest(df):
    result = df.groupby(['day', 'time'])[label].mean()
    print(result)


def corr(df, col):
    cor = df[col].corr()
    print(cor)


def smoke_people(df):
    df_smoke = df[df['smoker'] == 'Yes']
    result = len(df_smoke) / len(df)
    print("percentage of people are smoking is", round(result, 4))


def tip_increase(df):
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
        avg_tip_day(df)
        # question 3
        print('Question 3:')
        # TODO donghang 需要优化
        tip_highest(df)
        # question 4
        print('Question 4:')
        # TODO donghang 需要优化
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
        # TODO donghang

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
