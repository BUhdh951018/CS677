import os
import numpy as np
import pandas as pd
import traceback
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression

sc = StandardScaler()

le = LabelEncoder()

lr = LogisticRegression()

ticker = 'HSBC'
input_dir = r'../datasets'
ticker_file = os.path.join(input_dir, ticker + '_weekly_return_volatility.csv')

try:
    df_HSBC = pd.read_csv(ticker_file)

    # separate data by year
    df_2018 = df_HSBC[(df_HSBC['Year']) == 2018]
    df_2019 = df_HSBC[(df_HSBC['Year']) == 2019]

    # separate data by training set and testing set
    x_2018 = df_2018[["mean_return", "volatility"]].values
    y_2018 = df_2018[["Label"]].values.ravel()

    x_2019 = df_2019[["mean_return", "volatility"]].values
    y_2019 = df_2019[["Label"]].values.ravel()

except Exception as e:
    print(e)
    print(traceback.format_exc())


def draw_portfolio(predict_label, title):
    # set the start value
    week_portfolio = [100]
    week = df_2019['Week_Number'].tolist()
    x = df_2019['mean_return'].tolist()

    # calculate the weekly amount
    for i in range(len(predict_label)):
        if predict_label[i] == 'green':
            temp = week_portfolio[i] * pow((1 + x[i] / 100), 5)
            week_portfolio.append(temp)
        else:
            week_portfolio.append(week_portfolio[i])
    week.append(53)

    # draw on the plot
    plt.plot(week, week_portfolio)
    plt.title('2019 portfolio ' + title)
    plt.xlabel('week')
    plt.ylabel('portfolio')
    plt.show()
