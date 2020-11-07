# -*- coding: utf-8 -*-
"""
Created on 2020/11/3 1:40 上午
@Author  : Donghang He
@FileName: shapley_question2.py
@Software: PyCharm
"""

import traceback
import ssl
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# ssl certificate verification
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

url = r'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
flowers = ['Iris-versicolor', 'Iris-setosa', 'Iris-virginica']
feature = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width']
# show all row
pd.options.display.max_columns = None
pd.options.display.max_rows = None
np.set_printoptions(threshold=np.inf)
le = LabelEncoder()
# save the accuracy
accuracy = [[], [], []]


# use logistic regression to predict the class
def logistic_regression(x, y, i):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=3)
    lr = LogisticRegression()
    lr.fit(x_train, y_train)
    prediction = lr.predict(x_test)
    acc = np.mean(prediction == y_test)
    accuracy[i].append(acc)


def main():
    global feature
    try:
        print('All answers are summarized in Assignment8.docx')
        df = pd.read_csv(url, names=['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class'])
        data = df.copy()
        # loop for three times for three flowers
        for i in range(3):
            # set other flowers at second class
            for index, row in data.iterrows():
                if row['Class'] != flowers[i]:
                    data.loc[index, 'Class'] = 'second'
            y = le.fit_transform(data['Class'].values)
            # loop for five times for remove each feature and all four feature
            for j in range(5):
                if j != 0:
                    feature.pop(j - 1)
                x = data[feature].values
                logistic_regression(x, y, i)

                feature = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width']
            data = df.copy()

        for i in range(3):
            print("Flower ", flowers[i])
            for j in range(4):
                print("Feature " + str(feature[j]) + " marginal contributions: " +
                      str(round((accuracy[i][0] - accuracy[i][j + 1]) * 100, 2)) + "%")

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
