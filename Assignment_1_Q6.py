__author__ = 'Sushant'

import fnmatch
import os
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer



#nltk.download('punkt')
#nltk.download('stopwords')
stemmer = PorterStemmer()

# FUNCTION DEFINITIONS
def process_review(filename, mypath):
    #print("-------------------------------------------------------")
    #print(filename, " ",)
    fp = open(mypath+filename, 'r', encoding='utf-8')
    data = fp.read()
    #print(data)
    datap = re.sub('[^A-Za-z]', ' ', data)
    #print(datap)
    datal = datap.lower()
    #print(datal)

    # Data has been read, lowercased and special symbols removed

    datat = word_tokenize(datal)
    #print(datat)
    #print(len(datat))
    for word in datat:
        if word in stopwords.words('english'):
            datat.remove(word)

    #print(datat)
    #print(len(datat))

    for i in range(len(datat)):
        datat[i] = stemmer.stem(datat[i])
    #print(datat)
    #print(len(datat))

    dfreq = {x: datat.count(x) for x in datat}
    #print(dfreq)
    #print(len(dfreq))
    #print(sum(dfreq.values()))
    fp.close()
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
splitRatio = 0.9
#N = 100
#dir_pos, dir_pos_test = train_test_split(dir_pos_complete[0:N], train_size=splitRatio)
#dir_neg, dir_neg_test = train_test_split(dir_neg_complete[0:N], train_size=splitRatio)

#dir_pos, dir_pos_test = train_test_split(dir_pos_complete, train_size=splitRatio)
#dir_neg, dir_neg_test = train_test_split(dir_neg_complete, train_size=splitRatio)
dir_pos = dir_pos_complete
dir_neg = dir_neg_complete

# PRE PROCESSING DATA TO CREATE MATRIX
# POSITIVE
positive_key = []
positive_data = []
fop = open(mypath+'set_positive.txt', 'w+')

list_positive = {}
cp = 0
for i in range(len(dir_pos)):
    temp = process_review(dir_pos[i], mypath+'pos/')
    t = temp.keys()
    not_found = set(t) - set(positive_key)
    found = set(t) - not_found
    # converting to list
    not_found = list(not_found)
    found = list(found)
    positive_key = positive_key + not_found

    for k,v in temp.items():
        wordno = positive_key.index(k)
        fop.write(str(wordno)+' '+str(cp)+' '+str(v)+"\n")
    cp += 1
fop.close()
foi = open(mypath+'elem_positive.txt', 'w+')
    #list_positive = {x: temp.get(x, 0) + list_positive.get(x, 0) for x in set(temp).union(list_positive)}
te = ' '.join(positive_key)
print(te)
foi.write(str(te))
foi.close()
#print(list_positive)
#print(len(list_positive))
'''
# Writing Positive Output to a file
fop = open(mypath+'list_positive.txt', 'w')
for key in list_positive.keys():
    #fop.write(str(key)+'--'+str(list_positive[key])+
fop.close()
'''
print("--------------------------------------------------")
# NEGATIVE
negative_key = []
negative_data = []
fop = open(mypath+'set_negative.txt', 'w+')

list_negative = {}
cp = 0
for i in range(len(dir_pos)):
    temp = process_review(dir_pos[i], mypath+'pos/')
    t = temp.keys()
    not_found = set(t) - set(negative_key)
    found = set(t) - not_found
    # converting to list
    not_found = list(not_found)
    found = list(found)
    negative_key = negative_key + not_found

    for k,v in temp.items():
        wordno = negative_key.index(k)
        fop.write(str(wordno)+' '+str(cp)+' '+str(v)+"\n")
    cp += 1
fop.close()
foi = open(mypath+'elem_negative.txt', 'w+')
    #list_positive = {x: temp.get(x, 0) + list_positive.get(x, 0) for x in set(temp).union(list_positive)}
te = ' '.join(negative_key)
print(te)
foi.write(str(te))
foi.close()
#print(list_positive)
#print(len(list_positive))
'''
# Writing Positive Output to a file
fop = open(mypath+'list_positive.txt', 'w')
for key in list_positive.keys():
    #fop.write(str(key)+'--'+str(list_positive[key])+
fop.close()
'''
print("--------------------------------------------------")

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
#print(P_y_0, P_y_1, count_0, count_1)

#Calculate likelihood for all words
t = list(list_total.keys())
t.sort()
#print(t)
print(len(t))
P_w_y_0 = {}
P_w_y_1 = {}
for i in t:
    #print(i)
    if i in list_negative.keys():
        P_w_y_0[i] = (list_negative[i] / count_0)
    else:
        P_w_y_0[i] = 0

    if i in list_positive.keys():
        P_w_y_1[i] = (list_positive[i] / count_1)
    else:
        P_w_y_1[i] = 0
print("REACHED")
print("3. Probability Calculated")
# predict function calculation

#vocab_list = ['vomit', 'zodiac']
def predict(vocab_list):
    P_y_w_0 = P_y_0
    P_y_w_1 = P_y_1
    #print(vocab_list)
    for word in vocab_list:
        if word in list_total.keys():
            P_y_w_0 *= P_w_y_0[word]
            P_y_w_1 *= P_w_y_1[word]
        else:
            pass
            #print("New Word in Test data: ", word)

    #print(P_y_w_0, P_y_w_1)
    if P_y_w_0 > P_y_w_1:
        #print("Label - 0")
        return 0
    elif P_y_w_0 < P_y_w_1:
        #print("Label - 1")
        return 1
    else:
        #print("Tie")
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



