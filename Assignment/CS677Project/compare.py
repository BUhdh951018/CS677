# -*- coding: utf-8 -*-
"""
Created on 2020/11/17 1:43 上午
@Author  : Donghang He
@FileName: compare.py
@Software: PyCharm
"""
import os
import traceback
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from method import output_dir, pd
# import method and list
# from method import acc
# import panda frame
from method import df_corr, title_list, method
# import training set
from method import x_train, x_train_sc, y_train
# import test set
from method import x_test, x_test_sc
# import accuracy function
from method import acc
# import model
from method import svm_classifier, knn_classifier, logistic_classifier, nb_classifier, clf, model
from method import lda_classifier, qda_classifier

# show all row
pd.options.display.max_columns = None
pd.options.display.max_rows = None
np.set_printoptions(threshold=np.inf)


def knn(i):
    knn_classifier.fit(x_train_sc[i], y_train[i])
    predicted = knn_classifier.predict(np.asmatrix(x_test_sc[i]))
    return acc(predicted, 'kNN', i)


def logistic(i):
    logistic_classifier.fit(x_train[i], y_train[i])
    predicted = logistic_classifier.predict(np.asmatrix(x_test[i]))
    return acc(predicted, 'logistic regression', i)


def naive(i):
    nb_classifier.fit(x_train[i], y_train[i])
    predicted = nb_classifier.predict(np.asmatrix(x_test[i]))
    return acc(predicted, 'naive bayesian', i)


def tree(i):
    clf.fit(x_train[i], y_train[i])
    predicted = clf.predict(np.asmatrix(x_test[i]))
    return acc(predicted, 'decision tree', i)


def forest(i):
    model.fit(x_train[i], y_train[i])
    predicted = model.predict(np.asmatrix(x_test[i]))
    return acc(predicted, 'random forest', i)


def lda(i):
    lda_classifier.fit(x_train_sc[i], y_train[i])
    predicted = lda_classifier.predict(np.asmatrix(x_test_sc[i]))
    return acc(predicted, 'LDA', i)


def qda(i):
    qda_classifier.fit(x_train_sc[i], y_train[i])
    predicted = qda_classifier.predict(np.asmatrix(x_test_sc[i]))
    return acc(predicted, 'QDA', i)


def svm(i):
    svm_classifier.fit(x_train_sc[i], y_train[i])
    predicted = svm_classifier.predict(np.asmatrix(x_test_sc[i]))
    return acc(predicted, 'SVM', i)


def visual_corr(df, title):
    # correlation matrix
    corr = df.corr()
    # absolute the result
    corr = corr.abs()
    # show by the heat map
    plt.title('correlation matrix heatmap of NBA players')
    sns.heatmap(corr)
    # save the plot as png file
    plt.savefig(os.path.join(output_dir, 'correlation_matrix_nba_' + title + '.png'))
    plt.show()


def draw(accuracy, title):
    plt.figure()
    plt.plot(method, accuracy, color='blue', linestyle='dashed', marker='o', markerfacecolor='red', markersize=10)
    plt.title('Accuracy of all model for ' + title + 'columns')
    plt.xlabel('Prediction Model')
    plt.ylabel('Accuracy')
    plt.savefig(os.path.join(output_dir, 'accuracy_nba_' + title + '.png'))
    plt.show()


def main():
    try:
        # show the correlation heat map
        # for i in range(2):
        #     visual_corr(df_corr[i], title_list[i])
        for i in range(2):
            accuracy = [knn(i), logistic(i), naive(i), tree(i), forest(i), lda(i), qda(i), svm(i)]
            draw(accuracy, title_list[i])

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
