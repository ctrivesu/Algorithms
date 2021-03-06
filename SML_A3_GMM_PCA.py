import csv

import numpy as np
import matplotlib.pyplot as plt


with open(r"C:\Users\Sushant\Desktop\ASU Courses\CSE575 - Statistical Machine Learning\Assignment - 3\audioData.csv",
          'r') \
        as fp:
    data_iter = csv.reader(fp, delimiter=',', quotechar='"')
    data = [data for data in data_iter]

data_array = np.asarray(data)
data_array = data_array.astype(np.float)
print(data_array.shape)
print("GMM with PCA")

# COV
cov = np.cov(data_array.T)
# print("COV: ", cov)

# DISPLAY HEATMAP
# fig, ax = plt.subplots()
# im = ax.imshow(cov)
# plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#         rotation_mode="anchor")
# plt.show()    # Display HeatMap of COV


# EIGEN VALUES AND EIGENVECTOR
val_eig, vec_eig = np.linalg.eig(cov)
# print("EIGENVAL: ", val_eig)
# print("EIGVEC: ", vec_eig)

# No of PCA Eigenvalues that are acceptable
k = 2

EInfo = [(np.abs(val_eig[i]), vec_eig[:, i]) for i in range(len(val_eig))]
EInfo.sort(key=lambda x: x[0], reverse=True)

# WMatrix = [EInfo[0][1], EInfo[1][1]]
# print("E: ", EInfo)
WMatrix = np.concatenate((EInfo[0][1].reshape(13, 1), EInfo[1][1].reshape(13, 1)), axis=1)
print("WMatrix: ", WMatrix)

data_PCA = WMatrix.T.dot(data_array.T).T
# print("PCA: \n", data_PCA)

# PCA COMPLETED

def GMM(data_array):
    # k = int(input("Enter the no of cluster: "))
    k = 2

    samples_count, dim_count = data_array.shape

    # RANDOMLY SELECT POINTS AS MEANS
    np.random.seed(10)
    mu = data_array[np.random.choice(samples_count, k, False), :]
    pim = [1.0 / k] * k  # Mixture Ratios
    R = np.zeros((samples_count, k))  # Each cluster prob
    # cov = [np.eye(dim_count)] * k  # COV
    cov = np.array(np.cov(data_array.T))

    P = lambda mu, s: np.linalg.det(s) ** -.5 * (2 * np.pi) ** (- dim_count / 2.) * np.exp(
        -.5 * np.einsum('ij, ij -> i', data_array - mu, np.dot(np.linalg.inv(s), (data_array - mu).T).T))

    Prob_List = []
    t = 0
    # for i in range(1):
    while len(Prob_List) < 100000:
        # E-Step
        for i in range(k):
            # R[:, i] = pim[i] * (P(mu[i], cov[i]))
            R[:, i] = pim[i] * (P(mu[i], cov))

        log_likelihood = np.sum(np.log(np.sum(R, axis=1)))
        Prob_List.append(log_likelihood)

        R = (R.T / np.sum(R, axis=1)).T
        K_count = np.sum(R, axis=0)  # Cluster elements count
        # input()

        # M-Step
        for i in range(k):
            # update means
            mu[i] = 1. / K_count[i] * np.sum(R[:, i] * data_array.T, axis=1).T
            x_mu = np.matrix(data_array - mu[i])

            # update pim
            pim[i] = 1. / samples_count * K_count[i]
        print(t, pim, log_likelihood)

        # check for convergence
        if len(Prob_List) < 2:
            continue
        if np.abs(log_likelihood - Prob_List[-2]) < 0.0001:
            break
        t += 1

    index = np.argmax(R, axis=1)

    KList = []
    for i in range(k):
        KList.append([])

    for i in range(128):
        KList[int(index[i])].append(data_array[i, 0:2])

    # SCATTER PLOT
    clrs = ['green', 'red', 'blue', 'yellow']
    for i in range(k):
        for j in KList[i]:
            plt.scatter(j[0], j[1], color=clrs[i])
    plt.xlabel('Feature1')
    plt.ylabel('Feature2')
    plt.show()

GMM(data_PCA)
