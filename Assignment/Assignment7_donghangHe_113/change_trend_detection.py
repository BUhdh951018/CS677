# _*_ coding: utf-8 _*_
"""
Created on Tue Oct 27 2019
@author: Donghang He
"""

import os
import sys
import pandas as pd
import numpy as np
import traceback
from sklearn.linear_model import LinearRegression
from scipy.stats import f as fisher_f

input_dir = r'datasets'
input_file = os.path.join(input_dir, 'HSBC_label.csv')
# create linear regression model
model = LinearRegression(fit_intercept=True)


def candidate(df):
    # break day
    best_k = 0
    # minimize sse
    sse = sys.maxsize
    length = len(df)
    # sse left and right
    l1, l2 = 0, 0
    # find k
    for k in range(2, length):
        # save sse left and right
        l_list = []
        # predict left and right
        for i in range(2):
            if i == 0:
                start = 1
                end = k + 1
            else:
                start = k + 1
                end = length + 1
            l_list.append(linear_model(start, end, df))
        # whether is smaller than current sse
        if sum(l_list) < sse:
            best_k = k
            sse = sum(l_list)
            l1 = l_list[0]
            l2 = l_list[1]

    # sse for whole month
    l = linear_model(1, length + 1, df)
    # f statistics
    f = ((l - (l1 + l2)) / 2) / ((l1 + l2) / (length - 4))
    # f distribution
    p_value = fisher_f.cdf(f, 2, length - 4)
    # check significant change
    if p_value > 0.1:
        status = 'Yes'
    else:
        status = 'No'

    return status


def linear_model(start, end, df):
    # set x and y
    x = np.array(range(start, end)).reshape(-1, 1)
    y = np.array(df['Adj Close'][start - 1:end - 1])
    # fit model
    model.fit(x, y)
    # predict and compute the sse
    return np.sum((y - model.predict(x)) ** 2)


def main():
    try:
        # read file
        df = pd.read_csv(input_file)
        # 2 years
        for i in range(2018, 2020):
            print("Year " + str(i))
            df_year = df[(df['Year']) == i]
            # 12 months
            for j in range(1, 13):
                df_month = df_year[df_year['Month'] == j]
                status = candidate(df_month)
                # print the trend
                print("month: " + str(j) + " trend: " + str(status))

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
