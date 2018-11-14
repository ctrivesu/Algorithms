__author__ = 'Sushant'

import csv

import numpy as np


with open(r"C:\Users\Sushant\Desktop\ASU Courses\CSE575 - Statistical Machine Learning\Assignment - 3\audioData.csv", 'r') \
        as fp:
    data_iter = csv.reader(fp, delimiter=',', quotechar='"')
    data = [data for data in data_iter]

data_array = np.asarray(data)
print(data_array.shape)
print("KMeans")