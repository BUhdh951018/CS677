import os
import math
import numpy as np
import pandas as pd
import traceback
from sklearn.metrics import mean_squared_error

ticker = 'online_retail'
input_dir = r'../datasets'
ticker_file = os.path.join(input_dir, ticker + '.csv')
equal_weight = [0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111]


def calculate_leading(data):
    leading_digit = []
    country_f = []

    # get leading digit of each price
    for row in data:
        temp = str(row)
        leading_digit.append(temp[0])

    # count each leading digit
    for i in range(1, 10):
        count = leading_digit.count(str(i))
        country_f.append(round(count / len(leading_digit), 3))
    return country_f


def main():
    try:
        # read file
        df = pd.read_csv(ticker_file)
        df_new = df[(df['Country']).isin(['France', 'Japan', 'United Arab Emirates'])]
        df_new = df_new[['UnitPrice', 'Country']]
        df_new = df_new[(df_new['UnitPrice']) >= 1]
        country = ['France', 'Japan', 'United Arab Emirates']
        for i in range(0, 3):
            df_country = df_new[(df_new['Country']) == country[i]]
            data = df_country['UnitPrice'].tolist()
            country_f = calculate_leading(data)
            print("Country: " + country[i] + " F: " + str(country_f))

            country_error = math.sqrt(mean_squared_error(equal_weight, country_f))
            print("RESE: " + str(country_error))

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
