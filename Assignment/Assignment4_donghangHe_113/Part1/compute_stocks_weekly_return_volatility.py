# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:37:48 2019

@author: epinsky
"""

# run this  !pip install pandas_datareader
from pandas_datareader import data as web
import os
import math
import numpy as np 
import pandas as pd


ticker = 'HSBC'
input_dir = r'../datasets'
ticker_file = os.path.join(input_dir, ticker + '_label.csv')
output_file = os.path.join(input_dir, ticker + '_weekly_return_volatility.csv')

try:
    df = pd.read_csv(ticker_file)
    df = df[(df['Year']) > 2017]
    df_2 = df[['Year', 'Week_Number', 'Return', 'Label']]
    df_2.index = range(len(df))
    df_grouped = df_2.groupby(['Year', 'Week_Number', 'Label'])['Return'].agg([np.mean, np.std])
    # print(df_grouped)
    df_grouped.reset_index(['Year', 'Week_Number', 'Label'], inplace=True)
    df_grouped.rename(columns={'mean': 'mean_return', 'std': 'volatility'}, inplace=True)
    df_grouped.fillna(0, inplace=True)
    df_grouped['mean_return'] = df_grouped['mean_return'].apply(lambda x: format(x * 100, '.2'))
    df_grouped['volatility'] = df_grouped['volatility'].apply(lambda x: format(x * 100, '.2'))
    df_grouped.to_csv(output_file, index=False)

#    df_grouped_2 = df_grouped.fillna(0)
#    df_grouped_2.to_csv(output_file, index=False)
    
except Exception as e:
    print(e)


output_file = os.path.join(input_dir, ticker + '_weekly_return_volatility_detailed.csv')
combined_df = df.merge(df_grouped, on=['Year', 'Week_Number'], how='inner')
combined_df.to_csv(output_file, index=False)
print("wrote ", len(combined_df), " file to ", output_file)







