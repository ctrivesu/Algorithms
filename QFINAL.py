__author__ = 'Sushant'
import fnmatch
import os
import re

from sklearn.cross_validation import train_test_split

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer



#nltk.download('punkt')
#nltk.download('stopwords')
stemmer = PorterStemmer()

# FUNCTION DEFINITIONS
def process_review(filename, mypath):
    #print("-------------------------------------------------------")

    fp = open(mypath+filename, 'r', encoding='utf-8')
    data = fp.read()
    datap = re.sub('[^A-Za-z]', ' ', data)
    datal = datap.lower()


    # Data has been read, lowercased and special symbols removed
    datat = word_tokenize(datal)
    for word in datat:
        if word in stopwords.words('english'):
            datat.remove(word)

    for i in range(len(datat)):
        datat[i] = stemmer.stem(datat[i])

    dfreq = {x: datat.count(x) for x in datat}
    return dfreq

#MAIN FUNCTION
# READING THE LIST OF FILES IN FOLDER
dir_neg_complete = []
dir_pos_complete = []
mypath = '''C:/Users/Sushant/Desktop/Movie Review Dataset/movie review data/'''

for root, dirs, files in os.walk(mypath+'neg'):
    dir_neg_complete += fnmatch.filter(files, '*.txt')
for root, dirs, files in os.walk(mypath+'pos'):
    dir_pos_complete += fnmatch.filter(files, '*.txt')
print(len(dir_pos_complete))
print(len(dir_neg_complete))
print("1. List of files created")

# DEPENDING ON PERCENTAGE NEEDS TO EDIT THE LIST OF TEXT FILES BEING USED
splitRatio = 0.1

dir_pos, dir_pos_test = train_test_split(dir_pos_complete, train_size=splitRatio)
dir_neg, dir_neg_test = train_test_split(dir_neg_complete, train_size=splitRatio)


# PRE PROCESSING DATA TO CREATE MATRIX
# POSITIVE
list_positive = {}
for i in range(len(dir_pos)):
    temp = process_review(dir_pos[i], mypath+'pos/')
    list_positive = {x: temp.get(x, 0) + list_positive.get(x, 0) for x in set(temp).union(list_positive)}

# Writing Positive Output to a file
fop = open(mypath+'list_positive.txt', 'w')
for key in list_positive.keys():
    fop.write(str(key)+'--'+str(list_positive[key])+'\n\n')
fop.close()

print("--------------------------------------------------")
# NEGATIVE
list_negative = {}
for i in range(len(dir_neg)):
    temp = process_review(dir_neg[i], mypath+'neg/')
    list_negative = {x: temp.get(x, 0) + list_negative.get(x, 0) for x in set(temp).union(list_negative)}

# Writing Positive Output to a file
fop = open(mypath+'list_negative.txt', 'w')
for key in list_negative.keys():
    fop.write(str(key)+'--'+str(list_negative[key])+'\n\n')
fop.close()

print("2. Processing Files Completed")
# 2nd PART OF THE CODE

# combining the two lists
list_total = {x: list_positive.get(x, 0) + list_negative.get(x, 0) for x in set(list_positive).union(list_negative)}
print(len(list_total))

# Calculate priors
count_1 = len(dir_pos)  #CHANGED
count_0 = len(dir_neg)  #CHANGED
P_y_1 = count_1 / (count_0+count_1)
P_y_0 = count_0 / (count_0+count_1)

#Calculate likelihood for all words
t = list(list_total.keys())
t.sort()
total_word = len(t)
print(total_word)
P_w_y_0 = {}
P_w_y_1 = {}
for i in t:
    if i in list_negative.keys():
        P_w_y_0[i] = (list_negative[i] / count_0)
    else:
        P_w_y_0[i] = 1/(count_0 + total_word)

    if i in list_positive.keys():
        P_w_y_1[i] = (list_positive[i] / count_1)
    else:
        P_w_y_1[i] = 1/(count_1 + total_word)
print("REACHED")
print("3. Probability Calculated")
# predict function calculation

def predict(vocab_list):
    P_y_w_0 = P_y_0
    P_y_w_1 = P_y_1
    for word in vocab_list:
        if word in list_total.keys():
            P_y_w_0 *= P_w_y_0[word]
            P_y_w_1 *= P_w_y_1[word]
        else:
            pass
    if P_y_w_0 > P_y_w_1:
        return 0
    elif P_y_w_0 < P_y_w_1:
        return 1
    else:
        return 2

count = 0
test_total = len(dir_pos_test) + len(dir_neg_test)
for file in dir_pos_test:
    test_dict = process_review(file, mypath+'pos/')
    ret = predict(list(test_dict.keys()))
    if ret == 1:
        count += 1

for file in dir_neg_test:
    test_dict = process_review(file, mypath+'neg/')
    ret = predict(list(test_dict.keys()))
    if ret == 0:
        count += 1

print("Accuracy: ", count/test_total)