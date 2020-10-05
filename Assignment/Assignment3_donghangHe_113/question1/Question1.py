import pandas as pd
import numpy as np
import os
import traceback

ticker = 'HSBC'
input_dir = r'../stock_data'
ticker_file = os.path.join(input_dir, ticker + '.csv')


def main():
    try:
        # read file
        df = pd.read_csv(ticker_file)
        df = pd.DataFrame(df)
        # simplify the table
        col1 = df['Weekday']
        col2 = df['Return']
        df = pd.DataFrame(df['Year'])
        df.insert(1, 'Weekday', col1)
        df.insert(2, 'Return', col2)

        print('opened file for ticker: ', ticker)

        # for each years calculate the result
        for i in range(2015, 2020):
            df_new = df[(df['Year']) == i]
            print("Year: ", i)

            # loop 3 times, 0: R; 1: R+; 2: R-
            for j in range(0, 3):
                df_temp = df_new
                if j == 1:
                    df_temp = df_new[(df_new['Return']) >= 0]
                    print("positive")
                elif j == 2:
                    df_temp = df_new[(df_new['Return']) < 0]
                    print("negative")
                # calculate the mean and std for each set, and count the number for each set
                calculator(df_temp)

                print()

    except Exception as e:
        print(e)
        print(traceback.format_exc())


def calculator(df):
    result = df.groupby(['Weekday'])['Return'].agg(['mean', 'std', 'count'])
    mean = df['Return'].mean()
    print(result, "\nAll year Mean ", mean)


main()
