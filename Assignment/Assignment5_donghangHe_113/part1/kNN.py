import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from method import sc, le, x_2018, y_2018, x_2019, y_2019, draw_portfolio


def question1(x, y):
    # question 1

    # optional standard scaler
    x = sc.fit(x).transform(x)
    y = le.fit_transform(y)

    # split 50/50
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=0)

    # accuracy list
    accuracy = []
    # loop for calculate accuracy for each k
    for k in range(3, 13, 2):
        # set k
        knn_classifier = KNeighborsClassifier(n_neighbors=k)
        # train
        knn_classifier.fit(x_train, y_train)
        # predict label
        pred_k = knn_classifier.predict(x_test)
        # calculate accuracy
        accuracy.append(np.mean(pred_k == y_test))

    # draw the chart
    plt.figure(figsize=(10, 4))
    plt.plot(range(3, 13, 2), accuracy, color='red', linestyle='dashed', marker='o', markerfacecolor='black',
             markersize=10)

    plt.title('Accuracy vs k for HSBC (with standard scaler)')
    plt.xlabel('number of neighbors: k')
    plt.ylabel('Accuracy')

    plt.show()


def question2(x_train, y_train, x_test, y_test):

    knn_classifier = KNeighborsClassifier(n_neighbors=7)
    knn_classifier.fit(x_train, y_train)
    pred_k = knn_classifier.predict(x_test)
    accuracy = np.mean(pred_k == y_test)
    # question 2
    print("accuracy: " + str(accuracy))
    # question 3
    print("confusion matrix: ")
    print(confusion_matrix(y_test, pred_k))

    # question 5
    print(pred_k)

    draw_portfolio(pred_k, 'kNN')


def main():

    # question 1
    question1(x_2018, y_2018)

    # question 2&3&5
    question2(x_2018, y_2018, x_2019, y_2019)


main()
