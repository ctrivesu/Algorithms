mypath = '''C:/Users/Sushant/Desktop/ASU Courses/CSE575 - Statistical Machine Learning/Assignment - 1/Movie Review Dataset/'''
val = 0.1
# NEGATIVE
# Create a dictionary - {'Word': count}
fp = open(mypath + str(val) + '_elem_negative.txt', 'r', encoding='utf-8')
neg_word_list = fp.readline().split(' ')
print("NEG: ", len(neg_word_list), neg_word_list[0])
fp.close()

# combining the 2 files for each class
neg_dict = {}
fp = open(mypath + str(val) + '_set_negative.txt', 'r', encoding='utf-8')
for line in fp:
    line = line.split()
    # ----------------------------
    word = neg_word_list[int(line[0])]
    if word in neg_dict:
        neg_dict[word] += 1
    else:
        neg_dict.update({word: 1})
    # ----------------------------
fp.close()

# POSITIVE
# Create a dictionary - {'Word': count}
fp = open(mypath + str(val) + '_elem_positive.txt', 'r', encoding='utf-8')
pos_word_list = fp.readline().split(' ')
print("POS: ", len(pos_word_list), pos_word_list[0])
fp.close()

# combining the 2 files for each class
pos_dict = {}
fp = open(mypath + str(val) + '_set_positive.txt', 'r', encoding='utf-8')
for line in fp:
    line = line.split()
    # ----------------------------
    word = pos_word_list[int(line[0])]
    if word in pos_dict:
        pos_dict[word] += 1
    else:
        pos_dict.update({word: 1})
    # ----------------------------
fp.close()

# creating feature list
U = list(set(neg_word_list).union(set(pos_word_list)))

# NAIVE BAYES CALCULATION
Accuracy = 0


fp.close()
# Calculate Priors
# UPDATE NEEDED
count_1 = 14015
count_0 = 14364
P_y_1 = count_1 / (count_0 + count_1)
P_y_0 = count_0 / (count_0 + count_1)
print(P_y_0, P_y_1, count_0, count_1)

# Calculate likelihood for all words
t = U
t.sort()
print(len(t))
P_w_y_0 = {}
P_w_y_1 = {}
for i in t:
    if i in neg_word_list:
        P_w_y_0[i] = (neg_dict[i] / count_0)
    else:
        P_w_y_0[i] = 0

    if i in pos_word_list:
        P_w_y_1[i] = (pos_dict[i] / count_1)
    else:
        P_w_y_1[i] = 0

# PREDICTION CODE
# predict function calculation


#
# vocab_list = ['vomit', 'zodiac']
# P_y_w_0 = P_y_0
# P_y_w_1 = P_y_1
# for word in vocab_list:
#     P_y_w_0 *= P_w_y_0[word]
#     P_y_w_1 *= P_w_y_1[word]
#
# print(P_y_w_0, P_y_w_1)
# if P_y_w_0 > P_y_w_1:
#     print("Label - 0")
# elif P_y_w_0 < P_y_w_1:
#     print("Label - 1")
# else:
#     print("Tie")
