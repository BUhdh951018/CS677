# -*- coding: utf-8 -*-

from pandas_datareader import data as web
import os
import math
import numpy as np
import pandas as pd
import traceback
import matplotlib.pyplot as plt

ticker = 'HSBC'
input_dir = r'../datasets'
ticker_file = os.path.join(input_dir, ticker + '_weekly_return_volatility.csv')


def main():
    try:
        # read file
        df = pd.read_csv(ticker_file)
        # get the data of year 2018 and year 2019
        df_2018 = df[(df['Year']) == 2018]
        df_2019 = df[(df['Year']) == 2019]

        plt.figure()
        # sub plot 1 for year 2018
        plt.subplot(211)
        # put each point on the plot
        plt.scatter(df_2018['mean_return'], df_2018['volatility'], c=df_2018['Label'], s=300)
        week = df_2018['Week_Number'].tolist()
        x = df_2018['mean_return'].tolist()
        y = df_2018['volatility'].tolist()
        # put the week id on each point
        for i in range(len(df_2018)):
            plt.annotate(week[i], xy=(x[i], y[i]))
        plt.title('2018')
        plt.xlabel('mean_return')
        plt.ylabel('volatility')
        # plt.show()
        # sub plot 2 for year 2019
        plt.subplot(212)
        plt.scatter(df_2019['mean_return'], df_2019['volatility'], c=df_2019['Label'], s=300)
        week = df_2019['Week_Number'].tolist()
        x = df_2019['mean_return'].tolist()
        y = df_2019['volatility'].tolist()
        for i in range(len(df_2019)):
            plt.annotate(week[i], xy=(x[i], y[i]))
        plt.title('2019')
        plt.xlabel('mean_return')
        plt.ylabel('volatility')
        plt.show()

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()








