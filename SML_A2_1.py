__author__ = 'Sushant'

import os
import struct

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot


Data_Samples = 1000
# SIGMOID FUNCTION
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


# READ DATA FUNCTION
def read(dataset="training", path="."):
    if dataset is "training":
        fname_img = os.path.join(path, 'train-images.idx3-ubyte')
        fname_lbl = os.path.join(path, 'train-labels.idx1-ubyte')
    elif dataset is "testing":
        fname_img = os.path.join(path, 't10k-images.idx3-ubyte')
        fname_lbl = os.path.join(path, 't10k-labels.idx1-ubyte')
    else:
        raise ValueError("dataset must be 'testing' or 'training'")

    # Load everything in some numpy arrays
    with open(fname_lbl, 'rb') as flbl:
        _, _ = struct.unpack(">II", flbl.read(8))
        lbl = np.fromfile(flbl, dtype=np.int8)

    with open(fname_img, 'rb') as fimg:
        _, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
        img = np.fromfile(fimg, dtype=np.uint8).reshape(len(lbl), rows, cols)

    return (lbl, img)


# SHOW SINGLE IMAGE - takes a numpy array
def show(image):
    """
    Render a given numpy.uint8 2D array of pixel data.
    """
    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    imgplot = ax.imshow(image, cmap=mpl.cm.Greys)
    imgplot.set_interpolation('nearest')
    ax.xaxis.set_ticks_position('top')
    ax.yaxis.set_ticks_position('left')
    pyplot.show()


# //////////////////COMMENTED CODE////////////////
# mylist = list(set(L))
# for i in range(5):
# print(L[i])
# show(I[i])

# for i in range(3):
#     show(temp[i].reshape((28, 28)))


# Label array update in comparison with given Label
def label_found(a, given_label):
    if a == given_label:
        return 1
    else:
        return 0


# LR+GD
# OPTIMIZE
def optimize(w, X, L, iteration_no, learning_rate, given_label):
    cost_list = []
    m = X.shape[1]

    # Label updating to 0/1
    lf_func = np.vectorize(label_found)
    L = lf_func(L, given_label)

    # Logistic Regression + Gradient Descent code
    for i in range(iteration_no):
        z = np.dot(w.T, X)
        p_est = sigmoid(z)
        # cost = -1.0 / (m * np.sum((L * np.log(p_est)) + ((1.0 - L) * np.log(1.0 - p_est))))
        temp = np.sum(L * np.log(p_est) + (1.0 - L) * np.log(1.0 - p_est))
        cost = (-1.0 / m) * (temp)

        cost_list.append(cost)
        dw = 1.0 / m * np.dot(X, (p_est - L).T)
        w -= learning_rate * dw
        print(i + 1, " Cost: ", cost, m, "P_EST: ", p_est.shape, "Temp: ", temp)
    pyplot.plot(cost_list)
    pyplot.show()
    return w

# MAIN FUNCTION
[L, I] = read("training",
              r"C:\Users\Sushant\Desktop\ASU Courses\CSE575 - Statistical Machine Learning\Assignment - 2\MNIST")


# GET X Images, X Labels from the given dataset L,I
X = np.zeros((1, 784))
for i in range(Data_Samples):
    X = np.concatenate((X, I[i].reshape((1, 784))), axis=0)
X = np.delete(X, 0, 0)
X = X.T
# print(X.shape, L[0:Data_Samples].reshape((Data_Samples, 1)).shape)
L = L[0:Data_Samples].reshape((1, Data_Samples))
print("Data Samples Used: ", X.shape[1])
# show_choice = input("Show label count?(0/1)")
show_choice = 0
# LISTING COUNT FOR EACH LABEL
if show_choice == "1":
    for i in range(10):
        print("digit", i, "appear", np.count_nonzero(L == i), "times")

# input("Press Enter to continue")
dim = X.shape[0]  # no of features
# Single Classifier
w = np.zeros((dim, 1))
w = optimize(w, X, L, 100, 0.0001, 3)
print("W: \n", w.shape)

# Multi Classifier
# w = np.zeros((dim, 1))
# for i in range(10):
#     ret = optimize(np.zeros((dim, 1)), X, L, 100, 0.0001, i)
#     w = np.concatenate((w, ret), axis=1)
# w = np.delete(w, 0, 1)
# print("W_multiclass: ", w.shape)

# Store the weight matrix in a file
fp = open(r"C:\Users\Sushant\Desktop\ASU Courses\CSE575 - Statistical Machine Learning\Assignment - 2\Weight.txt", 'w')
np.savetxt(r"C:\Users\Sushant\Desktop\ASU Courses\CSE575 - Statistical Machine Learning\Assignment - 2\Weight.csv", w, delimiter = ',') # , fmt='%.3e')





#PREDICT
# Predict the Label - 0/1
# w - Weight Matrix
# X - Training Data
def predict(w, X):
    m = X.shape[1]
    z = np.dot(w.T, X)
    p_est = sigmoid(z)
