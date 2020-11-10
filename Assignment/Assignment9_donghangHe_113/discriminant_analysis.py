# -*- coding: utf-8 -*-
"""
Created on 2020/11/9 5:55 下午
@Author  : Donghang He
@FileName: discriminant_analysis.py
@Software: PyCharm
"""
import os
import traceback
import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
sc = StandardScaler()
lda_classifier = LDA()
qda_classifier = QDA()
input_dir = r'datasets'
title = 'HSBC'
input_file = os.path.join(input_dir, title + '_weekly_return_volatility.csv')
input_file1 = os.path.join(input_dir, title + '_label.csv')


def buy_and_hold(data):
    price = [100]
    length = len(data)
    # two variables for the open price and end price of the green week
    begin, end = data[0][0], 0
    # variable for check the week number
    week_number = 100
    # loop each days in year 2019 to calculate the final price
    for i in range(length):
        # first check the current week whether same to the week of this day
        if week_number != int(data[i][2]):
            # if not update the week number and set the open price
            week_number = int(data[i][2])
        # last day of the year calculate the final price and break
        if i + 1 == length:
            end = data[i][1]
            # calculate the last week price
            price.append(end / begin * 100)
            break
        # end day of week update the price
        if week_number != int(data[i + 1][2]):
            end = data[i][1]
            # calculate the week price, because I'm not out of the market
            # so the price will be end/begin * 100
            price.append(end / begin * 100)

    return price


def label_price(data, label):
    price = [100]
    length = len(data)
    # two variables for the open price and end price of the green week
    begin, end = 0, 0
    week_number = 100
    # flag for whether in the market
    flag = False
    temp_price = 100
    # loop each days in year 2019 to calculate the final price
    for i in range(length):
        # first check the current week whether same to the week of this day
        if week_number != int(data[i][2]):
            # if not update the week number
            week_number = int(data[i][2])

            # last day of the year calculate the final price and break
            if i + 1 == length:
                end = data[i][1]
                price.append(end / begin * temp_price)
                break

            # if today is red day, also it must be the first day of the red week
            # so set the price and jump to next loop
            if label[week_number] == 'red':
                price.append(price[week_number])
                flag = False
                continue
            # else it must be the first day of green week so set the open price
            else:
                if flag is False:
                    begin = data[i][0]
                    flag = True
                    temp_price = price[week_number - 1]

        # or in the same week
        else:
            # red day jump
            if label[week_number] == 'red':
                continue
            # last day of the year calculate the final price and break
            if i + 1 == length:
                end = data[i][1]
                price.append(end / begin * temp_price)
                break
            # end day of green week update the price
            if week_number != int(data[i + 1][2]):
                end = data[i][1]
                price.append(end / begin * temp_price)

    return price


def main():
    print('All answers are summarized in Assignment9.docx')
    try:
        df = pd.read_csv(input_file)
        df_train = df[df['Year'] == 2018]
        df_test = df[df['Year'] == 2019]
        x_train = df_train[['mean_return', 'volatility']].values
        y_train = df_train['Label'].values
        x_test = df_test[['mean_return', 'volatility']].values
        y_test = df_test['Label'].values
        # use standard scaler
        x_train = sc.fit(x_train).transform(x_train)
        x_test = sc.fit(x_test).transform(x_test)

        # question 1
        lda_classifier.fit(x_train, y_train)
        print(f'Equation for linear classifier: ({lda_classifier.coef_[0][0]})x1 + ({lda_classifier.coef_[0][1]})x2 '
              f'+ ({lda_classifier.intercept_[0]}) = 0')
        qda_classifier.fit(x_train, y_train)
        # print(f'Equation for linear classifier: ({lda_classifier.coef_[0][0]})x1 + ({lda_classifier.coef_[0][1]})x2 '
        #       f'+ ({lda_classifier.intercept_[0]}) = 0')
        # TODO quadratic equation

        # question 2
        pred_lda = lda_classifier.predict(x_test)
        pred_qda = qda_classifier.predict(x_test)
        accuracy_lda = np.mean(pred_lda == y_test)
        accuracy_qda = np.mean(pred_qda == y_test)
        print('Accuracy for year 2 for LDA is', accuracy_lda)
        print('Accuracy for year 2 for QDA is', accuracy_qda)

        # question 3
        matrix_lda = confusion_matrix(y_test, pred_lda)
        matrix_qda = confusion_matrix(y_test, pred_qda)
        print('confusion matrix for LDA')
        print(matrix_lda)
        print('confusion matrix for QDA')
        print(matrix_qda)

        # question 4
        print('LDA')
        tpr = matrix_lda[0][0] / (matrix_lda[0][0] + matrix_lda[0][1])
        tnr = matrix_lda[1][1] / (matrix_lda[1][0] + matrix_lda[1][1])
        print("true positive rate is: ", tpr)
        print("true negative rate is: ", tnr)
        print('QDA')
        tpr = matrix_qda[0][0] / (matrix_qda[0][0] + matrix_qda[0][1])
        tnr = matrix_qda[1][1] / (matrix_qda[1][0] + matrix_qda[1][1])
        print("true positive rate is: ", tpr)
        print("true negative rate is: ", tnr)

        # question 5
        df_new = pd.read_csv(input_file1)
        df_new = df_new[df_new['Year'] == 2019]

        week_number = df_test['Week_Number'].tolist()
        week_number.append(53)

        # buy and hold strategy
        df_bh = df_new[['Open', 'Close', 'Week_Number']]
        data = np.array(df_bh)
        price = buy_and_hold(data.tolist())
        plt.plot(week_number, price, color='blue', label='buy-and-hold')
        # LDA strategy
        price = label_price(data, pred_lda)
        plt.plot(week_number, price, color='red', label='LDA')
        # QDA strategy
        price = label_price(data, pred_qda)
        plt.plot(week_number, price, color='yellow', label='QDA')

        plt.title('portfolio growth')
        plt.xlabel('week number')
        plt.ylabel('portfolio value')
        plt.legend()
        plt.show()

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
