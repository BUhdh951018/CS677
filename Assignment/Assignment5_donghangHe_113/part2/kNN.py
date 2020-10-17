import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

url = r'../datasets/data_banknote_color.csv'


def question1_2(data):
    # question 1
    x = data[["variance", "skewness", "curtosis", "entropy"]].values
    y = data[["Color"]].values.ravel()
    '''
    scaler = StandardScaler().fit(x)
    x = scaler.transform(x)
    '''
    le = LabelEncoder()
    y = le.fit_transform(y)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=0)

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


def question3(data):
    # question 3
    x = data[["variance", "skewness", "curtosis", "entropy"]].values
    y = data[["Color"]].values.ravel()

    le = LabelEncoder()
    y = le.fit_transform(y)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=0)
    knn_classifier = KNeighborsClassifier(n_neighbors=7)
    knn_classifier.fit(x_train, y_train)
    pred_k = knn_classifier.predict(x_test)
    accuracy = np.mean(pred_k == y_test)

    print("accuracy: " + str(accuracy))
    print("confusion matrix: ")
    print(confusion_matrix(y_test, pred_k))

    print("label with my BUID as feature:")
    buid = [9, 1, 1, 3]
    print(knn_classifier.predict([np.array(buid)]))


def main():
    data = pd.read_csv(url)

    # question 1&2
    question1_2(data)

    # question 3
    question3(data)


main()
