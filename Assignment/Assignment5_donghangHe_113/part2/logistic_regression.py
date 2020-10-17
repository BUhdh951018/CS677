import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression

url = r'../datasets/data_banknote_authentication.csv'


def question(data):
    # question 1
    cols = ["variance", "skewness", "curtosis", "entropy"]
    y = data[["class"]].values.ravel()
    x = data[cols].values

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=0)
    log_reg_classifier = LogisticRegression()
    log_reg_classifier.fit(x_train, y_train)

    prediction = log_reg_classifier.predict(x_test)
    accuracy = np.mean(prediction == y_test)

    print("accuracy: " + str(accuracy))

    # question 2
    print("confusion matrix: ")
    print(confusion_matrix(y_test, prediction))

    # question 5
    buid = [9, 1, 1, 3]
    print("label with my BUID as feature:")
    print(log_reg_classifier.predict([np.array(buid)]))


def main():
    data = pd.read_csv(url)

    # question
    question(data)


main()
