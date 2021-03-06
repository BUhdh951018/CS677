# -*- coding: utf-8 -*-
"""
Created on 2020/11/16 6:51 下午
@Author  : Donghang He
@FileName: kmeans.py
@Software: PyCharm
"""

import os
import traceback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

input_dir = r'datasets'
title = 'HSBC'
input_file = os.path.join(input_dir, title + '_weekly_return_volatility.csv')


def main():
    try:
        print("all answer shown in the doc file assignment10.docx")
        df = pd.read_csv(input_file)
        df_test = df.copy()
        x = df[['mean_return', 'volatility']].values

        # question 1
        inertia_list = []
        for k in range(1, 9):
            kmeans_classifier = KMeans(n_clusters=k)
            y_means = kmeans_classifier.fit_predict(x)
            inertia = kmeans_classifier.inertia_
            inertia_list.append(inertia)

        fig, ax = plt.subplots(1, figsize=(7, 5))
        plt.plot(range(1, 9), inertia_list, marker='o', color='green')
        plt.xlabel('number of clusters: k')
        plt.ylabel('inertia')
        plt.tight_layout()
        plt.show()

        # question 2
        kmeans_classifier = KMeans(n_clusters=2)
        y_means = kmeans_classifier.fit_predict(x)
        df_test['cluster'] = y_means

        for i in range(2):
            df_new = df_test[df_test['cluster'] == i]
            df_label = df_new[df_new['Label'] == 'green']
            percent = len(df_label) / len(df_new)
            print(f'Percentage of "Green" in Cluster {i}: {round(percent)}')
            print(f'Percentage of "Red" in Cluster {i}: {round(1 - percent)}')
        # TODO donghang

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
