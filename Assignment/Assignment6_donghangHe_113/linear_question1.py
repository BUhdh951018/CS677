import os
import pandas as pd
import numpy as np
import traceback
import matplotlib.pyplot as plt


ticker = 'HSBC'
input_dir = r'dataset'
ticker_file = os.path.join(input_dir, ticker + '.csv')
ticker_file1 = os.path.join(input_dir, ticker + '_weekly_return_volatility.csv')

# weekly closing price
week_close = []

# real label
true_label = []

# x for predict
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# accuracy
accuracy = [[], [], []]


def week_close_price(week_number, close):
    for i in range(len(close) - 1):
        if week_number[i] != week_number[i + 1]:
            week_close.append(close[i])


def predict_label_w_degree():
    global true_label

    for i in range(5, 13):
        x_w = x[:i]
        for j in range(1, 4):
            predict = ['red']
            for m in range(12, len(week_close) + 1):
                y_new = linear_model(i, x_w, j, m)
                label = predict_label(round(y_new, 2), m, predict)
                predict.append(label)
            predict.pop(1)
            accuracy[j - 1].append(np.mean(np.array(predict) == np.array(true_label)))


def linear_model(w, x_w, degree, week_m):

    x_w = np.array(x_w)
    y = []
    for i in range(len(x_w), 0, -1):
        y.append(week_close[week_m - i])

    y = np.array(y)
    weights = np.polyfit(x_w, y, degree)
    model = np.poly1d(weights)

    x_new = w + 1
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


def plot_accuracy():
    for i in range(3):
        plt.figure()
        plt.plot(x[-8:], accuracy[i])
        plt.title("accuracy for d = " + str(i+1))
        plt.xlabel('W')
        plt.ylabel('accuracy')
        plt.show()


def main():
    global true_label
    try:
        # read file
        df = pd.read_csv(ticker_file)

        # get true label for
        df_true = pd.read_csv(ticker_file1)
        df_true = df_true[(df_true['Year']) == 2018]
        true_label = df_true['Label'].tolist()

        # the last day of week 41 in 2017
        start_date = '2017-10-13'
        # the last day in 2018
        end_date = '2018-12-31'

        df = df[df['Date'] >= start_date]
        df = df[df['Date'] <= end_date]
        df_new = df[['Week_Number', 'Close']]
        week_number = df_new['Week_Number'].tolist()
        close = df_new['Close'].tolist()

        # get weekly close price
        week_close_price(week_number, close)

        # predict the weekly close and set the label than calculate the accuracy
        predict_label_w_degree()

        print(accuracy)
        # plot the accuracy
        plot_accuracy()

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
