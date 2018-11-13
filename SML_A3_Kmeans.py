__author__ = 'Sushant'

import csv
import random

import numpy as np
from numpy import linalg as LA


with open(r"C:\Users\Sushant\Desktop\ASU Courses\CSE575 - Statistical Machine Learning\Assignment - 3\audioData.csv", 'r') \
        as fp:
    data_iter = csv.reader(fp, delimiter=',', quotechar='"')
    data = [data for data in data_iter]

data_array = np.asarray(data)
print(data_array.shape[0])
Kmeans = np.zeros(10)
print("KMeans")

# K-Means Algorithm

def Kmeans(data, k):

    delta = 999999
    K = np.zeros((10, 13))

    # K = np.random.rand(10, 13)   # Cluster means
    # K = np.zeros((10, 13))
    # print("K:", K)
    cond = np.zeros((10, 1))
    print(cond[0:k], np.count_nonzero(cond[0:k]), k)

    while (K[0:k].size - np.count_nonzero(K[0:k])) != 0:
        print("Restart KMeans: ", K[0:k].size, np.count_nonzero(K[0:k]))

        # Initializing the means
        for i in range(k):
            K[i] = data[random.randint(0, 10)]

        k_count = np.zeros((10, 1))
        k_count_old = np.random.rand(10, 1)

        # Kmeans Algorithm
        while not np.array_equal(k_count_old, k_count):
            k_count_old = k_count
            k_sum = np.zeros((10, 13))
            k_count = np.empty((10, 1))
            temp = np.zeros((10, 13))
            k_count = np.zeros((10, 1))
            for i in range(data.shape[0]):   # Run it for all points
                # print("DATA: ", data[i])
                temp[0:k] = K[0:k] - np.tile(data.astype('float')[i], (k, 1))    # Distance from each mean
                t = LA.norm(temp, axis=1)
                # print("T", t)
                k_index = np.argmin(t[0:k])
                k_sum[k_index] += data[i].astype('float')
                k_count[k_index] += 1
                # print("K_Index: ", k_index, "\nK_SUM: ", k_sum, "\nK_Count: ", k_count)
                # print("K_Index: ", k_index)
            # print("Iteration Complete")
            K = np.divide(k_sum, k_count, out=np.zeros_like(k_sum), where=k_count != 0)
            # print("Final K_Sum: ", k_sum, "\nFinal K_Count: ", k_count, "\nFinal K_div: ", k_ncent)
            # print("Final K_Count: ", k_count, "\nK_mean: ", k_ncent.shape)
            # print("Final K_Count: ", k_count[0:k])
            # print("Final Mean: ", K[0:k])
        k_count[0:k].sort(axis=0)
        print("Final K_Count: ", k_count[0:k])


        cond = LA.norm(K[0:k], axis=1)
        print(cond)
Kmeans(data_array, 7)