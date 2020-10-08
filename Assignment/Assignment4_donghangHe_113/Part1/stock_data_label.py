import pandas as pd
import numpy as np
import os
import traceback

ticker = 'HSBC'
input_dir = r'../datasets'
ticker_file = os.path.join(input_dir, ticker + '_label.csv')


def final_price(data):
    price = 100
    length = len(data)
    # two variables for the open price and end price of the green week
    begin, end = 0, 0
    # variable for check the week number
    week_number = 100
    # flag for whether in the market
    flag = False
    # loop each days in year 2019 to calculate the final price
    for i in range(length):
        # first check the current week whether same to the week of this day
        if week_number != int(data[i][3]):
            # if not update the week number
            week_number = int(data[i][3])

            # last day of the year calculate the final price and break
            if i + 1 == length:
                end = data[i][1]
                price = end / begin * price
                break

            # if today is red day, also it must be the first day of the red week
            # so set the price and jump to next loop
            if data[i][2] == 'red':
                price = price
                flag = False
                continue
            # else it must be the first day of green week so set the open price
            else:
                if flag is False:
                    begin = data[i][0]
                    flag = True
        # or in the same week
        else:
            # red day jump
            if data[i][2] == 'red':
                continue
            # last day of the year calculate the final price and break
            if i + 1 == length:
                end = data[i][1]
                price = end / begin * price
                break
            # end day of green week update the price
            if week_number != int(data[i + 1][3]):
                end = data[i][1]
                # if next week is also green so the price will not update
                temp_price = end / begin * price
                # or we will out of the market and check the current price
                if data[i + 1][2] == 'red':
                    price = temp_price

    return price


def main():
    try:
        # read file
        df = pd.read_csv(ticker_file)
        # get the data of 2019
        df = df[(df['Year']) == 2019]
        # set the open price and end price
        df_open = df[(df['Date']) == '2019/1/2']
        df_close = df[(df['Date']) == '2019/12/31']
        open_price = df_open['Open'].tolist()
        close_price = df_close['Close'].tolist()

        # calculate the price
        price = 100
        price = close_price[0] / open_price[0] * price
        # Question 1
        print("buy-and-hold strategy final price is: " + str(round(price, 2)))

        # simplify the table
        df_label = df[['Open', 'Close', 'Label', 'Week_Number']]
        # change to list
        data = np.array(df_label)
        data = data.tolist()
        # print(data)

        # Question 2
        price = final_price(data)
        print("my strategy final price is: " + str(round(price, 2)))
    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
