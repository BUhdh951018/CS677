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
ticker_file = os.path.join(input_dir, ticker + '_label.csv')


def buyandhold_final_price(data):
    price = [100]
    length = len(data)
    # two variables for the open price and end price of the green week
    begin, end = data[0][0], 0
    # variable for check the week number
    week_number = 100
    # loop each days in year 2019 to calculate the final price
    for i in range(length):
        # first check the current week whether same to the week of this day
        if week_number != int(data[i][2]):
            # if not update the week number and set the open price
            week_number = int(data[i][2])
        # last day of the year calculate the final price and break
        if i + 1 == length:
            end = data[i][1]
            # calculate the last week price
            price.append(end / begin * 100)
            break
        # end day of week update the price
        if week_number != int(data[i + 1][2]):
            end = data[i][1]
            # calculate the week price, because I'm not out of the market
            # so the price will be end/begin * 100
            price.append(end / begin * 100)

    return price


def final_price(data):
    price = [100]
    length = len(data)
    # two variables for the open price and end price of the green week
    begin, end = 0, 0
    week_number = 100
    # flag for whether in the market
    flag = False
    temp_price = 100
    # loop each days in year 2019 to calculate the final price
    for i in range(length):
        # first check the current week whether same to the week of this day
        if week_number != int(data[i][3]):
            # if not update the week number
            week_number = int(data[i][3])

            # last day of the year calculate the final price and break
            if i + 1 == length:
                end = data[i][1]
                price.append(end / begin * temp_price)
                break

            # if today is red day, also it must be the first day of the red week
            # so set the price and jump to next loop
            if data[i][2] == 'red':
                price.append(price[week_number])
                flag = False
                continue
            # else it must be the first day of green week so set the open price
            else:
                if flag is False:
                    begin = data[i][0]
                    flag = True
                    temp_price = price[week_number - 1]

        # or in the same week
        else:
            # red day jump
            if data[i][2] == 'red':
                continue
            # last day of the year calculate the final price and break
            if i + 1 == length:
                end = data[i][1]
                price.append(end / begin * temp_price)
                break
            # end day of green week update the price
            if week_number != int(data[i + 1][3]):
                end = data[i][1]
                price.append(end / begin * temp_price)

    return price


def main():
    try:
        # read file
        df = pd.read_csv(ticker_file)
        df_2019 = df[(df['Year']) == 2019]
        # simplify the table
        df_bh = df_2019[['Open', 'Close', 'Week_Number']]
        df_label = df_2019[['Open', 'Close', 'Label', 'Week_Number']]
        # get the week number for x axis
        week_number = df_2019['Week_Number'].tolist()
        week_number = list(set(week_number))
        # the week number in the data set is from 0 to 52 and we have our origin week with price is 100,
        # so we need to add one more week
        week_number.append(53)
        # change to list
        data = np.array(df_bh)
        data = data.tolist()

        # 'buy and hold' price list and plot
        price = buyandhold_final_price(data)
        # print(price)
        plt.plot(week_number, price, color='blue', label='buy-and-hold')

        data_new = np.array(df_label)
        data_new = data_new.tolist()

        # 'true label' price list and plot
        price = final_price(data_new)
        # print(price)
        plt.plot(week_number, price, color='red', label='true labels')

        plt.title('portfolio growth')
        plt.xlabel('week number')
        plt.ylabel('portfolio value')
        plt.legend()
        plt.show()

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
