import os
import pandas as pd
import math
import numpy as np
import traceback

input_dir = r'datasets'
input_file = os.path.join(input_dir, 'HSBC_label.csv')


def candidate(df):
    df = df[['Day', 'Close']]
    days = df['Day'].tolist()

    total = 1000000
    k = 0
    for i in range(len(days)):
        if i == 0:
            continue
        if i == len(days) - 1:
            break

        df_1 = df[(df['Day']) <= days[i]]
        df_2 = df[(df['Day']) > days[i]]
        result_1 = linear_model(df_1)
        result_2 = linear_model(df_2)
        temp_total = result_1 + result_2
        if temp_total < total:
            k = days[i]
            total = temp_total
    print(k)


def linear_model(df):
    weights = np.polyfit(df['Day'], df['Close'], 2)
    model = np.poly1d(weights)
    predicted = model(df['Day'])

    return ((df['Close'].values - predicted) ** 2).sum()


def main():
    try:
        df = pd.read_csv(input_file)

        for i in range(2018, 2020):
            print("Year " + str(i))
            df_year = df[(df['Year']) == i]
            for j in range(2, 3):
                df_month = df_year[(df['Month']) == j]
                candidate(df_month)

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
