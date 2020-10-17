import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from method import x_bank, y_bank, sc, lr


def question(x, y):

    # question 1
    x = sc.fit(x).transform(x)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=0)

    prediction = lr.fit(x_train, y_train).predict(x_test)
    accuracy = np.mean(prediction == y_test)

    print("accuracy: " + str(accuracy))

    # question 2
    print("confusion matrix: ")
    print(confusion_matrix(y_test, prediction))

    # question 5
    buid = [9, 1, 1, 3]
    print("label with my BUID as feature:")
    print(lr.predict([np.array(buid)]))


def main():

    # question
    question(x_bank, y_bank)


main()
