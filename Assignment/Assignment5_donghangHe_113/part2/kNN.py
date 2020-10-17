import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from method import sc, le, lr, x_bank, y_bank


def question1_2(x, y):

    # question 1
    # separate to 50/50
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=0)

    # calculate for accuracy of each k
    accuracy = []
    for k in range(3, 13, 2):
        knn_classifier = KNeighborsClassifier(n_neighbors=k)
        knn_classifier.fit(x_train, y_train)
        pred_k = knn_classifier.predict(x_test)
        accuracy.append(np.mean(pred_k == y_test))

    # question 2
    plt.figure(figsize=(10, 4))
    plt.plot(range(3, 13, 2), accuracy, color='red', linestyle='dashed', marker='o', markerfacecolor='black',
             markersize=10)
    plt.title('Accuracy vs k for banknotes')
    plt.xlabel('number of neighbors: k')
    plt.ylabel('Accuracy')
    plt.show()


def question3_5(x, y):

    # learn and predict the label
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=0)
    knn_classifier = KNeighborsClassifier(n_neighbors=7)
    knn_classifier.fit(x_train, y_train)
    pred_k = knn_classifier.predict(x_test)

    # calculate the accuracy
    accuracy = np.mean(pred_k == y_test)

    # question 3
    print("accuracy: " + str(accuracy))
    print("confusion matrix: ")
    print(confusion_matrix(y_test, pred_k))

    # question 5
    print("label with my BUID as feature:")
    buid = [9, 1, 1, 3]
    print(knn_classifier.predict([np.array(buid)]))


def main():

    # question 1&2
    question1_2(x_bank, y_bank)

    # question 3&5
    question3_5(x_bank, y_bank)


main()
