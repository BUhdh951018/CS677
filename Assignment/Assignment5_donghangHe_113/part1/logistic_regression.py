import numpy as np
from sklearn.metrics import confusion_matrix
from method import lr, x_2018, y_2018, x_2019, y_2019, draw_portfolio


def question1(x_train, y_train):

    lr.fit(x_train, y_train)
    print(lr.coef_)
    print(lr.intercept_)


def question2_3(x_train, y_train, x_test, y_test):

    # question 2
    prediction = lr.fit(x_train, y_train).predict(x_test)
    accuracy = np.mean(prediction == y_test)

    print("accuracy: " + str(accuracy))
    print("confusion matrix: ")
    print(confusion_matrix(y_test, prediction))

    draw_portfolio(prediction, 'logistic regression')


def main():

    # question 1
    question1(x_2018, y_2018)

    # question 2&3
    question2_3(x_2018, y_2018, x_2019, y_2019)


main()
