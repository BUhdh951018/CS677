import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

url = r'../datasets/data_banknote_color.csv'


def question1(data):
    # question 1
    cols = ["variance", "skewness", "curtosis", "entropy"]
    y = data[["Color"]].values.ravel()
    for i in range(0, 4):
        cols.pop(i)

        x = data[cols].values

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=0)
        knn_classifier = KNeighborsClassifier(n_neighbors=7)
        knn_classifier.fit(x_train, y_train)
        pred_k = knn_classifier.predict(x_test)
        accuracy = np.mean(pred_k == y_test)
    
        print("Drop f" + str(i + 1) + " accuracy: " + str(accuracy))

        cols = ["variance", "skewness", "curtosis", "entropy"]


def main():
    data = pd.read_csv(url)

    # question 1
    question1(data)


main()
