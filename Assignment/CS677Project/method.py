# -*- coding: utf-8 -*-
"""
Created on 2020/11/16 9:48 下午
@Author  : Donghang He
@FileName: method.py
@Software: PyCharm
"""
import os
import pandas as pd
import numpy as np
import traceback

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm, tree
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA

sc = StandardScaler()
le = LabelEncoder()

knn_classifier = KNeighborsClassifier(n_neighbors=7)
logistic_classifier = LogisticRegression()
nb_classifier = GaussianNB()
clf = tree.DecisionTreeClassifier(criterion='entropy')
model = RandomForestClassifier(n_estimators=9, max_depth=5, random_state=1, criterion='entropy')
lda_classifier = LDA()
qda_classifier = QDA()
svm_classifier = svm.SVC(kernel='linear')

ticker = 'nba'
input_dir = r'datasets'
input_file = os.path.join(input_dir, ticker + '.csv')
output_dir = r'plots'

score_col = ['FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'PTS']
other_col = ['G', 'MP', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF']
pred_score = ['FG%', '3P%', '2P%', 'eFG%', 'FT%']
pred_other = ['G', 'ORB', 'TRB', 'AST', 'BLK']

x_train = [0, 0]
x_train_sc = [0, 0]
y_train = [0, 0]

x_test = [0, 0]
x_test_sc = [0, 0]
y_test = [0, 0]

title_list = ['score', 'other']
method = ['kNN', 'Logistic', 'Naive', 'Decision Tree', 'Random Forest',
          'LDA', 'QDA', 'SVM']

try:
    df_new = pd.read_csv('datasets/NBA_label.csv')
    df_score = df_new[score_col]
    df_other = df_new[other_col]
    df_corr = [df_score, df_other]

    x1 = df_new[pred_score].values
    y = df_new['Label'].values
    x_train[0], x_test[0], y_train[0], y_test[0] = train_test_split(x1, y, test_size=0.5, random_state=0)

    x2 = df_new[pred_other].values
    x_train[1], x_test[1], y_train[1], y_test[1] = train_test_split(x2, y, test_size=0.5, random_state=0)

    x_train_sc[0] = sc.fit_transform(x_train[0])
    x_train_sc[1] = sc.fit_transform(x_train[1])
    x_test_sc[0] = sc.fit_transform(x_test[0])
    x_test_sc[1] = sc.fit_transform(x_test[1])


except Exception as e:
    print(e)
    print(traceback.format_exc())


def acc(predict, name, i):
    accuracy = np.mean(predict == y_test[i])
    print("Accuracy of", name, "for", title_list[i], "is", round(float(accuracy), 3))
    return round(float(accuracy), 3)


# use to get the label of age, bigger than 25 is 1 other is 0
# def generateLabel():
#     df = pd.read_csv(input_file, encoding='gbk')
#     age = df['Age'].tolist()
#     label = []
#     for i in range(len(age)):
#         if age[i] > 25:
#             label.append(1)
#         else:
#             label.append(0)
#     df['Label'] = label
#     df.to_csv('datasets/NBA_label.csv', index=False)
#
#
# def main():
#     # generateLabel()


# main()
