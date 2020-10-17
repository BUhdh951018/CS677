import numpy as np
from sklearn.model_selection import train_test_split
from method import df_banknote, cols, y_bank, lr, sc


def question1(data, col, y):

    # question 1
    for i in range(0, 4):
        col.pop(i)
        x = data[col].values

        x = sc.fit(x).transform(x)

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=0)

        prediction = lr.fit(x_train, y_train).predict(x_test)
        accuracy = np.mean(prediction == y_test)

        print("accuracy: " + str(accuracy))

        col = ["variance", "skewness", "curtosis", "entropy"]


def main():
    data = df_banknote

    # question 1
    question1(data, cols, y_bank)


main()
