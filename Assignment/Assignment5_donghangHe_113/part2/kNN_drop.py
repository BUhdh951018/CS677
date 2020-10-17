import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from method import df_banknote, y_bank, cols


def question1(data, y, col):
    # question 1
    for i in range(0, 4):
        col.pop(i)

        x = data[col].values

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=0)
        knn_classifier = KNeighborsClassifier(n_neighbors=7)
        knn_classifier.fit(x_train, y_train)
        pred_k = knn_classifier.predict(x_test)
        accuracy = np.mean(pred_k == y_test)
    
        print("Drop f" + str(i + 1) + " accuracy: " + str(accuracy))

        col = ["variance", "skewness", "curtosis", "entropy"]


def main():
    data = df_banknote

    # question 1
    question1(data, y_bank, cols)


main()
