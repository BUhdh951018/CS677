# -*- coding: utf-8 -*-

from pandas_datareader import data as web
import os
import pandas as pd
import traceback
import numpy as np
import statistics
import matplotlib.pyplot as plt

ticker = 'HSBC'
input_dir = r'../datasets'
ticker_file = os.path.join(input_dir, ticker + '_label.csv')


def final_price(data):
    price = [100]
    length = len(data)

    # two variables for the open price and end price of the green week
    begin, end = 0, 0
    week_number = 100
    # flag for whether in the market
    flag = False
    temp_price = 100
    # loop each days in this year to calculate the final price
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
        year = [2018, 2019]

        for i in range(0, 2):
            df_new = df[(df['Year']) == year[i]]
            # simplify the table
            df_label = df_new[['Open', 'Close', 'Label', 'Week_Number']]
            data = np.array(df_label)
            data = data.tolist()
            price = final_price(data)

            # question 1
            print("year " + str(year[i]) + " mean:" + str(statistics.mean(price)) +
                  " volatility: " + str(statistics.stdev(price)))

            # get the week number for x axis
            week_number = df_new['Week_Number'].tolist()
            week_number = list(set(week_number))
            # the week number in the data set is from 0 to 52 and we have our origin week with price is 100,
            # so we need to add one more week
            week_number.append(53)

            # question 2
            plt.plot(week_number, price, color='blue', label='buy-and-hold')
            plt.title(year[i])
            plt.xlabel('week number')
            plt.ylabel('account balance')
            plt.legend()
            plt.show()

            # question 4
            print("final value is: " + str(price[len(price) - 1]))

            # question 5
            temp = price[0]
            duration = [0, 0]
            grow, decrease = 0, 0
            for j in range(1, len(price)):
                if price[j] > temp:
                    grow += 1
                elif price[j] < temp:
                    decrease += 1
                else:
                    duration[0] = (max(duration[0], grow))
                    duration[1] = (max(duration[1], decrease))
                    grow, decrease = 0, 0
                temp = price[j]
            print("growing weeks: " + str(duration[0]) + " decreasing weeks: " + str(duration[1]))

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
