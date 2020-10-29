# _*_ coding: utf-8 _*_
"""
Created on Tue Oct 27 2019
@author: Donghang He
"""

import os
import pandas as pd
import numpy as np
import traceback
from sklearn.linear_model import LinearRegression
from scipy.stats import f as fisher_f

input_dir = r'datasets'
input_file = os.path.join(input_dir, 'HSBC_label.csv')


def candidate(df):
    k_list = []
    sse = []
    length = len(df)
    for k in range(2, length):
        x1 = np.array(range(1, k + 1)).reshape(-1, 1)
        y1 = np.array(df['Close'][0:k])

        x2 = np.array(range(k+1, length + 1)).reshape((-1, 1))
        y2 = np.array(df['Close'][k:])

        model = LinearRegression(fit_intercept=True)
        model.fit(x1, y1)
        sse_l = np.sum((y1 - model.predict(x1)) ** 2)

        model.fit(x2, y2)
        sse_r = np.sum((y2 - model.predict(x2)) ** 2)

        k_list.append(k)
        sse.append(sse_l + sse_r)

    best_k = k_list[sse.index(min(sse))]

    x = np.array(range(1, length + 1)).reshape(-1, 1)
    y = np.array(df['Close'])
    x1 = np.array(range(1, best_k + 1)).reshape(-1, 1)
    y1 = np.array(df['Close'][0:best_k])

    x2 = np.array(range(best_k + 1, length + 1)).reshape((-1, 1))
    y2 = np.array(df['Close'][best_k:])

    model = LinearRegression(fit_intercept=True)

    model.fit(x, y)
    l = np.sum((y - model.predict(x)) ** 2)

    model.fit(x1, y1)
    l1 = np.sum((y1 - model.predict(x1)) ** 2)

    model.fit(x2, y2)
    l2 = np.sum((y2 - model.predict(x2)) ** 2)

    f = ((l - (l1 + l2)) / 2) / ((l1 + l2) / (length - 4))

    p_value = fisher_f.cdf(f, 2, length - 4)
    print(best_k)
    if p_value > 0.1:
        status = 'Yes'
    else:
        status = 'No'

    return status


def main():
    try:
        df = pd.read_csv(input_file)

        for i in range(2018, 2020):
            print("Year " + str(i))
            df_year = df[(df['Year']) == i]
            for j in range(1, 13):
                df_month = df_year[df_year['Month'] == j]
                status = candidate(df_month)
                print("month: " + str(j) + " trend: " + str(status))

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
