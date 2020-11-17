# -*- coding: utf-8 -*-
"""
Created on 2020/11/16 6:51 下午
@Author  : Donghang He
@FileName: svm.py
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
        df = pd.read_csv(input_file)
        x = df[['mean_return', 'volatility']].values

    except Exception as e:
        print(e)
        print(traceback.format_exc())


main()
