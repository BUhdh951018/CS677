# -*- coding: utf-8 -*-

import os
import sys
from prettytable import PrettyTable
from colorama import init, Fore
import pandas as pd
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


# make the 'True Label' column has color
def red(s):
    return Fore.LIGHTRED_EX + s + Fore.RESET


def green(s):
    return Fore.LIGHTGREEN_EX + s + Fore.RESET


ticker = 'HSBC'
input_dir = r'../stock_data'
ticker_file = os.path.join(input_dir, ticker + '.csv')

try:
    df = pd.read_csv(ticker_file)
    df = pd.DataFrame(df)

    print('opened file for ticker: ', ticker)
    # check the return and add the label to list
    data = list(df['Return'])
    label = []
    for col in data:
        if float(col) < 0:
            label.append(red(str('-')))
        else:
            label.append(green(str('+')))
    df.insert(14, 'True Label', label)
    # print the label on the table with color
    print(df)
    # print the label on the table without color
    label = []
    for col in data:
        if float(col) < 0:
            label.append(str('-'))
        else:
            label.append(str('+'))
    df.iloc[:, 14] = label
    print(df)

    # save the data to a new file
    df.to_csv('../stock_data/new_HSBC.csv', index=False)
except Exception as e:
    print(e)
    print('failed to read stock data for ticker: ', ticker)
