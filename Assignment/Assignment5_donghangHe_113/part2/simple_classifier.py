# -*- coding: utf-8 -*-

import os
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from method import df_banknote, le

plot_dir = r'../plots'


def main():

    df = df_banknote

    x_train, x_test = train_test_split(df, test_size=0.5, random_state=0)
    df = x_train

    question1(df)

    df = x_test
    question3(df)


def plot_histograms(df, cols, color):
    for n_col in cols:
        print("mean for ", n_col, " is ", df[n_col].mean())
        print("mean for ", n_col, " is ", df[n_col].std())
        df.hist(n_col, bins=10, color=color)
    return


def question1(df):

    cols = ["variance", "skewness", "curtosis", "entropy"]

    df_0 = df[df["class"] == 0]
    plot_histograms(df_0, cols, color="green")

    df_1 = df[df["class"] == 1]
    plot_histograms(df_1, cols, color="red")

    colors = ["green"]
    sns.set_palette(sns.color_palette(colors))
    pair_plot_0 = sns.pairplot(df_0, vars=cols)
    plt.show()
    pair_plot_0.savefig(os.path.join(plot_dir, "good_bills.pdf"))

    colors = ["red"]
    sns.set_palette(sns.color_palette(colors))
    print("pairwise relationships for class 1")
    pair_plot_1 = sns.pairplot(df_1, vars=cols)
    plt.show()
    pair_plot_1.savefig(os.path.join(plot_dir, "fake_bills.pdf"))


def question3(df):
    # apply simple classifier
    color = []
    true_color = df['class'].tolist()
    data = np.array(df).tolist()
    for row in data:
        if row[0] > 2 and row[1] > 5 and row[2] < 8:
            color.append('green')
        else:
            color.append('red')

    color = le.fit_transform(color)
    true_color = le.fit_transform(true_color)

    # question 4
    print(confusion_matrix(true_color, color))

    # question 5
    print(np.mean(true_color == color))


main()
