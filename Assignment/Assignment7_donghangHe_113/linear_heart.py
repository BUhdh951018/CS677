# _*_ coding: utf-8 _*_
"""
Created on Tue Oct 26 2019
@author: Donghang He
"""

import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import traceback

# show all row
pd.options.display.max_columns = None
pd.options.display.max_rows = None
np.set_printoptions(threshold=np.inf)

input_dir = r'datasets'
input_file = os.path.join(input_dir, 'heart_failure_clinical_records_dataset.csv')
output_dir = r'plots'

title = ['surviving', 'deceased']
model_title = ['simple linear regression', 'quadratic', 'cubic spline', 'GLM1', 'GLM2']


def visual_corr(df, status):
    df = df[['creatinine_phosphokinase', 'serum_creatinine', 'serum_sodium', 'platelets']]
    # correlation matrix
    corr = df.corr()
    # absolute the result
    corr = corr.abs()
    # show by the heat map
    plt.title('correlation matrix heatmap of ' + str(status) + ' patients')
    sns.heatmap(corr, annot=True)
    # save the plot as png file
    plt.savefig(os.path.join(output_dir, 'correlation_matrix_' + status + '_patients.png'))
    plt.show()


def split(df, event):
    # get the data for group 2
    x = df['platelets']
    y = df['serum_sodium']
    # 50/50 split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=0)

    # loop for each model
    for i in range(1, 6):
        # i for identify current model and event for live or die
        linear_model(x_train, y_train, x_test, y_test, i, event)


def linear_model(x_train, y_train, x_test, y_test, degree, event):
    # keep the argument not change
    x = x_train
    y = y_train
    x_real = x_test
    title_name = degree
    # do the log for GLM
    if degree == 4:
        degree = 1
        x = np.log(x)
        x_real = np.log(x_real)

    if degree == 5:
        degree = 1
        x = np.log(x)
        x_real = np.log(x_real)
        y = np.log(y)
    # get the weights for current model
    weights = np.polyfit(x, y, degree)
    print("weights for " + str(model_title[title_name - 1]) + ": " + str(weights))
    # create the model
    model = np.poly1d(weights)
    # compute predict values
    predicted = (model(x_real))
    # use exp method making logy to y
    if title_name == 5:
        predicted = np.exp(predicted)
    # plot the actually point and predict points
    plot(x_test, y_test, predicted, title_name, event)
    # compute the corresponding loss function
    sse(y_test, predicted)


def plot(x_real, y_real, y_predict, title_name, event):
    plt.figure()
    plt.title(str(title[event]) + " patients " + str(model_title[title_name - 1]))
    # draw the actual points
    plt.scatter(x_real, y_real, color='b')
    # draw the predict points
    plt.scatter(x_real, y_predict, color='r')
    plt.show()


def sse(real, predict):
    # use SEE formula to calculate the result
    result = ((real - predict) ** 2).sum()
    print("SEE for this model " + str(round(result, 2)))


def main():
    try:
        df = pd.read_csv(input_file)
        # question 1.1
        df = df[['creatinine_phosphokinase', 'serum_creatinine', 'serum_sodium', 'platelets', 'DEATH_EVENT']]
        # divide by patient live or die
        df_0 = df[(df['DEATH_EVENT']) == 0]
        df_1 = df[(df['DEATH_EVENT']) == 1]
        df_new = [df_0, df_1]

        # question 1.2
        for i in range(2):
            # question 1.2
            # visual_corr(df_new[i], title[i])

            print(str(title[i]) + " patients")
            # question 2
            split(df_new[i], i)
            print()

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
