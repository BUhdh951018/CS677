import os
import math
import numpy as np
import pandas as pd
import traceback
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ticker = 'online_retail'
input_dir = r'../datasets'
ticker_file = os.path.join(input_dir, ticker + '.csv')
length, length1, length2 = 0, 0, 0
real_p = []


# 3 same method to change the y axis from 0.01 to 1%
def to_percent(y, position):
    global length
    return str(round(100 * y / length, 3)) + "%"


def to_percent1(y, position):
    global length1
    return str(round(100 * y / length1, 3)) + "%"


def to_percent2(y, position):
    global length2
    return str(round(100 * y, 3)) + "%"


def calculate_leading(data):
    leading_digit = []

    # get leading digit of each price
    for row in data:
        temp = str(row)
        leading_digit.append(temp[0])
    # sort the leading digit
    leading_digit.sort()

    # count each leading digit for the question 2
    for i in range(1, 10):
        count = leading_digit.count(str(i))
        real_p.append(round(count / len(leading_digit), 3))
    print(real_p)

    return leading_digit


def main():
    global length, length1, length2, real_p
    try:
        # read file
        df = pd.read_csv(ticker_file)
        # get the UnitPrice column to a new table
        df_price = df[['UnitPrice']]
        # get the price >= 1 to a new table
        df_price = df_price[(df_price['UnitPrice']) >= 1]
        data = df_price['UnitPrice'].tolist()

        # count each leading digit
        leading_digit = calculate_leading(data)

        # get the length of leading digit list
        length = len(leading_digit)

        # draw the plot
        plt.figure()
        # first sub plot show the frequencies for real distribution
        plt.subplot(311)
        plt.hist(leading_digit, bins=9, facecolor='blue', edgecolor='black')
        # set the y axis
        formatter = FuncFormatter(to_percent)
        plt.gca().yaxis.set_major_formatter(formatter)
        plt.title('real distribution')
        plt.ylabel('probability')

        # list for equal weight
        equal_weight = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        length1 = len(equal_weight)

        # second sub plot show the frequencies for equal-weight distribution
        plt.subplot(312)
        plt.hist(equal_weight, bins=9, facecolor='red', edgecolor='black')
        formatter = FuncFormatter(to_percent1)
        plt.gca().yaxis.set_major_formatter(formatter)
        plt.title('equal-weight distribution')
        plt.ylabel('probability')

        # list for Bernford's law
        bernford = [0.301, 0.176, 0.125, 0.097, 0.079, 0.058, 0.058, 0.051, 0.046]

        # third sub plot show the frequencies for Bernford's law
        plt.subplot(313)
        plt.bar(range(1, 10), bernford, color='green', tick_label=equal_weight)
        formatter = FuncFormatter(to_percent2)
        plt.gca().yaxis.set_major_formatter(formatter)
        plt.title('Bernford\'s law')
        plt.xlabel('leading digit')
        plt.ylabel('probability')

        # show the plot
        plt.show()

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
