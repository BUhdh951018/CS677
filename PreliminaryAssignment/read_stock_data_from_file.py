# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 14:37:29 2018

@author: epinsky
this scripts reads your ticker file (e.g. MSFT.csv) and
constructs a list of lines
"""
import os
import sys
from prettytable import PrettyTable

ticker = 'HSBC'
input_dir = r'/Users/donghanghe/study/PreliminaryAssignment'
ticker_file = os.path.join(input_dir, ticker + '.csv')

try:
    with open(ticker_file) as f:
        lines = f.read().splitlines()
    print('opened file for ticker: ', ticker)
    """    your code for assignment 1 goes here
    """
    data = []
    for row in lines:
        data.append(row.split(','))
    temp = []
    for i in range(0, 16):
        temp.append(data[0][i])
    table = PrettyTable(temp)

    j = 0
    for row in data:
        if j == 0:
            j = 1
            continue
        temp = []
        for i in range(0, 16):
            temp.append(row[i])
        table.add_row(temp)

    print(table)
except Exception as e:
    print(e)
    print('failed to read stock data for ticker: ', ticker)
