# -*- coding: utf-8 -*-

import numpy as np
import traceback
import matplotlib.pyplot as plt
from method import df_2018, df_2019, draw_portfolio


def function(x):
    return -84.375 * x + 3.625


def equation(x, y):
    temp = 84.375 * x + y
    if temp >= 3.625:
        return True
    else:
        return False


def main():
    try:

        plt.figure()

        # question 1
        # put each point on the plot
        plt.scatter(df_2018['mean_return'], df_2018['volatility'], c=df_2018['Label'], s=300)
        week = df_2018['Week_Number'].tolist()
        x = df_2018['mean_return'].tolist()
        y = df_2018['volatility'].tolist()

        # put the week id on each point
        for i in range(len(df_2018)):
            plt.annotate(week[i], xy=(x[i], y[i]))

        # set plot attributes
        plt.title('2018')
        plt.xlabel('mean_return')
        plt.ylabel('volatility')

        # draw the line to separate the green and red points
        x1 = np.arange(0.01, 0.06, 0.01)
        y2 = function(x1)
        plt.plot(x1, y2)
        plt.show()

        # question 2
        week = df_2019['Week_Number'].tolist()
        x = df_2019['mean_return'].tolist()
        y = df_2019['volatility'].tolist()

        # save the new predict label in a list
        color = []
        for i in range(len(df_2019)):
            if equation(x[i], y[i]):
                plt.scatter(x[i], y[i], c='g', s=100)
                color.append('green')
            else:
                plt.scatter(x[i], y[i], c='r', s=100)
                color.append('red')
            plt.annotate(week[i], xy=(x[i], y[i]))

        plt.title('2019')
        plt.xlabel('mean_return')
        plt.ylabel('volatility')

        x1 = np.arange(0.01, 0.06, 0.01)
        y2 = function(x1)
        plt.plot(x1, y2)
        plt.show()

        # question 3
        draw_portfolio(color, 'linear')

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()








