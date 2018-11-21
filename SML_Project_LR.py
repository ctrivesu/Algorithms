__author__ = 'Sushant'
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

# READ TRAIN DATA
data = pd.read_csv(r"C:\Users\Sushant\Desktop\ASU Courses\CSE575 - Statistical Machine Learning\Final Project/"
                   r"/\3. Implementation\aps_failure_training_set.csv", skiprows=20)
print("Data Read", data.shape)
data = data.replace(['na'], [np.NaN])
X = data.drop(['class'], axis=1)
temp = X.convert_objects(convert_numeric=True)
# temp.fillna(value=0, inplace=True)
temp = temp.fillna(temp.mean()).dropna(axis=1, how='all')
Y = data['class']

# TRAINING
print("Training Started\n")
LogReg = LogisticRegression()
print(LogReg.fit(temp, Y))
print("Training Complete\n")

# TEST DATA
test_data = pd.read_csv(r"C:\Users\Sushant\Desktop\ASU Courses\CSE575 - Statistical Machine Learning\Final Project/"
                        r"/\3. Implementation\aps_failure_test_set.csv", skiprows=20)
test_data = data.replace(['na'], [np.NaN])
X_test = test_data.drop(['class'], axis=1)
X_test = X_test.convert_objects(convert_numeric=True)
X_test.fillna(value=0, inplace=True)
# X_test = X_test.fillna(X_test.median().dropna(axis=1, how='all')
X_test = X_test.fillna(X_test.mean()).dropna(axis=1, how='all')

Y_test = test_data['class']

# THRESHOLD CODE
'''
Threshold_List = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

for val in Threshold_List:
    Y_pred_prob = pd.DataFrame(LogReg.predict_proba(X_test))
    Y_pred = Y_pred_prob.applymap(lambda x: 1 if x > val else 0)
    fp = 0
    fn = 0
    n = 0
    for i in Y_pred[0]:
        if i == 1 and Y_test[n] == 'pos':
            fn += 1
        if i == 0 and Y_test[n] == 'neg':
            fp += 1
        n += 1
    print(val, "FP: ", fp, "FN: ", fn, "Cost: ", fn * 500 + fp * 10)
'''

# STANDARDIZATION
# scaler = StandardScaler()
# scaler.fit(temp)
# temp = scaler.transform


# CONFUSION MATRIX + SCORE
print(LogReg.score(X_test, Y_test))
Y_pred = LogReg.predict(X_test)
print("Y_PRED: ", np.count_nonzero(Y_pred == 'pos'))
confusion_matrix = confusion_matrix(Y_test, Y_pred)
print(confusion_matrix)

# WEIGHTS
w = LogReg.coef_[0]
print(w)


'''
# CODE FOR ITERATIVE FEATURE REDUCTION
rfe = RFE(LogReg, 165)
rfe = rfe.fit(temp, Y)
fs = rfe.support_
print(rfe.support_)

n = 0
for i in fs:
    if not i:
        print(test_data.columns[n])
        X_test = test_data.drop([str(test_data.columns[n])], axis=1)
    n += 1

print(X_test.shape)
# export_csv = temp.to_csv(.csv', index=None, header=True)


'''