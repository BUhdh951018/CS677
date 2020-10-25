import os
import pandas as pd
import numpy as np
import traceback
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

ticker = 'HSBC'
input_dir = r'dataset'
ticker_file = os.path.join(input_dir, ticker + '.csv')
ticker_file1 = os.path.join(input_dir, ticker + '_weekly_return_volatility.csv')

# weekly closing price
week_close = []

# real label
true_label = []

# accuracy
accuracy = []

# best w in year 2018
w = [10, 7, 9]

# x for predict
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


def week_close_price(week_number, close):
    for i in range(len(close) - 1):
        if week_number[i] != week_number[i + 1]:
            week_close.append(close[i])


def predict_label_w_degree(df_true):
    global true_label

    for i in range(1, 4):
        x_w = x[:w[i - 1]]
        predict = ['green']
        for m in range(12, len(week_close) + 1):
            y_new = linear_model(x_w, i, m)
            label = predict_label(round(y_new, 2), m, predict)
            predict.append(label)
        predict.pop(1)
        accuracy.append(np.mean(np.array(predict) == np.array(true_label)))

        # question 2
        print("accuracy for d = " + str(i) + " " + str(accuracy[i - 1]))

        # question 3
        print(confusion_matrix(true_label, predict))

        # question 4
        draw_portfolio(predict, i, df_true)


def linear_model(x_w, degree, week_m):

    x_w = np.array(x_w)
    y = []
    for i in range(len(x_w), 0, -1):
        y.append(week_close[week_m - i])

    y = np.array(y)
    weights = np.polyfit(x_w, y, degree)
    model = np.poly1d(weights)

    x_new = w[degree - 1] + 1
    y_new = model(x_new)

    return y_new


def predict_label(predict_close, week_m, predict):

    if predict_close > week_close[week_m - 1]:
        label = 'green'
    elif predict_close < week_close[week_m - 1]:
        label = 'red'
    else:
        label = predict[week_m - 12]

    return label


def draw_portfolio(predict, degree, df_2019):
    # set the start value
    week_portfolio = [100]
    week = df_2019['Week_Number'].tolist()
    x_axis = df_2019['mean_return'].tolist()

    # calculate the weekly amount
    for i in range(len(predict)):
        if predict[i] == 'green':
            temp = week_portfolio[i] * pow((1 + x_axis[i] / 100), 5)
            week_portfolio.append(temp)
        else:
            week_portfolio.append(week_portfolio[i])
    week.append(53)

    # draw on the plot
    plt.plot(week, week_portfolio)
    plt.title('d =  ' + str(degree) + ' W = ' + str(w[degree - 1]))
    plt.xlabel('week')
    plt.ylabel('portfolio')
    plt.show()


def main():
    global true_label
    try:
        # read file
        df = pd.read_csv(ticker_file)

        # get true label for
        df_true = pd.read_csv(ticker_file1)
        df_true = df_true[(df_true['Year']) == 2019]
        true_label = df_true['Label'].tolist()

        # the last day of week 41 in 2018
        start_date = '2018-10-19'
        # the last day in 2018
        end_date = '2019-12-31'

        df = df[df['Date'] >= start_date]
        df = df[df['Date'] <= end_date]
        df_new = df[['Week_Number', 'Close']]
        week_number = df_new['Week_Number'].tolist()
        close = df_new['Close'].tolist()

        # get weekly close price
        week_close_price(week_number, close)

        # predict the weekly close and set the label than calculate the accuracy
        predict_label_w_degree(df_true)

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
