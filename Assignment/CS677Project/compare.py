# -*- coding: utf-8 -*-
"""
Created on 2020/11/17 1:43 上午
@Author  : Donghang He
@FileName: compare.py
@Software: PyCharm
"""
import traceback
import numpy as np
import matplotlib.pyplot as plt
# import method and list
from method import buy_and_hold, label_price, acc, week_number
# import panda frame
from method import df_new, x_train, y_train, x_test, x_train_sc, x_test_sc
# import model
from method import svm_classifier, knn_classifier, logistic_classifier, nb_classifier, clf, model
from method import lda_classifier, qda_classifier


# todo 哪些需要sc
def knn():
    knn_classifier.fit(x_train_sc, y_train)
    predicted = knn_classifier.predict(np.asmatrix(x_test_sc))
    acc(predicted, 'kNN')
    return predicted


def logistic():
    logistic_classifier.fit(x_train, y_train)
    predicted = logistic_classifier.predict(np.asmatrix(x_test))
    acc(predicted, 'logistic regression')
    return predicted


def naive():
    nb_classifier.fit(x_train, y_train)
    predicted = nb_classifier.predict(np.asmatrix(x_test))
    acc(predicted, 'naive bayesian')
    return predicted


def tree():
    clf.fit(x_train, y_train)
    predicted = clf.predict(np.asmatrix(x_test))
    acc(predicted, 'decision tree')
    return predicted


def forest():
    model.fit(x_train, y_train)
    predicted = model.predict(np.asmatrix(x_test))
    acc(predicted, 'random forest')
    return predicted


def lda():
    lda_classifier.fit(x_train_sc, y_train)
    predicted = lda_classifier.predict(np.asmatrix(x_test_sc))
    acc(predicted, 'LDA')
    return predicted


def qda():
    qda_classifier.fit(x_train_sc, y_train)
    predicted = qda_classifier.predict(np.asmatrix(x_test_sc))
    acc(predicted, 'QDA')
    return predicted


def svm():
    svm_classifier.fit(x_train_sc, y_train)
    predicted = svm_classifier.predict(np.asmatrix(x_test_sc))
    acc(predicted, 'SVM')
    return predicted


def main():
    try:
        # buy and hold strategy
        df_bh = df_new[['Open', 'Close', 'Week_Number']]
        data = np.array(df_bh)
        price = buy_and_hold(data.tolist())
        print("final price for buy and hold strategy", round(price[-1], 4))
        print()
        plt.plot(week_number, price, color='tab:blue', label='buy-and-hold')

        # knn strategy k=7
        predict_knn = knn()
        price = label_price(data, predict_knn)
        print("final price for KNN strategy", round(price[-1], 4))
        print()
        plt.plot(week_number, price, color='tab:orange', label='kNN')

        # logistic regression
        predict_lr = logistic()
        price = label_price(data, predict_lr)
        print("final price for logistic regression strategy", round(price[-1], 4))
        print()
        plt.plot(week_number, price, color='tab:green', label='logistic')

        # naive bayesian
        predict_nb = naive()
        price = label_price(data, predict_nb)
        print("final price for naive bayesian strategy", round(price[-1], 4))
        print()
        plt.plot(week_number, price, color='tab:red', label='naive bayesian')

        # decision tree
        predict_dt = tree()
        price = label_price(data, predict_dt)
        print("final price for decision tree strategy", round(price[-1], 4))
        print()
        plt.plot(week_number, price, color='tab:purple', label='decision tree')

        # random forest
        predict_rf = forest()
        price = label_price(data, predict_rf)
        print("final price for random forest strategy", round(price[-1], 4))
        print()
        plt.plot(week_number, price, color='tab:brown', label='random forest')

        # linear discriminant
        predict_ld = lda()
        price = label_price(data, predict_ld)
        print("final price for linear discriminant strategy", round(price[-1], 4))
        print()
        plt.plot(week_number, price, color='tab:pink', label='linear discriminant')

        # quadratic discriminant
        predict_qd = qda()
        price = label_price(data, predict_qd)
        print("final price for quadratic discriminant strategy", round(price[-1], 4))
        print()
        plt.plot(week_number, price, color='tab:olive', label='quadratic discriminant')

        # svm strategy
        predict_svm = svm()
        price = label_price(data, predict_svm)
        print("final price for SVM strategy", round(price[-1], 4))
        print()
        plt.plot(week_number, price, color='tab:gray', label='linear SVM')

        plt.title('portfolio growth')
        plt.xlabel('week number')
        plt.ylabel('portfolio value')
        plt.legend()
        plt.show()

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
