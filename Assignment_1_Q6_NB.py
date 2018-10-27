
mypath = '''C:/Users/Sushant/Desktop/Movie Review Dataset/movie review data/'''

fp = open(mypath+'list_negative.txt', 'r', encoding='utf-8')
read = fp.read()
list_negative = read.split('\n')
list_negative = [x for x in list_negative if x]
list_negative = {x.split('--')[0]: int(x.split('--')[1]) for x in list_negative}
print(len(list_negative))
print("------------------")

fp = open(mypath+'list_positive.txt', 'r', encoding='utf-8')
read = fp.read()
list_positive = read.split('\n')
list_positive = [x for x in list_positive if x]
list_positive = {x.split('--')[0]: int(x.split('--')[1]) for x in list_positive}
print(len(list_positive))


#combining the two lists
list_total = {x: list_positive.get(x, 0) + list_negative.get(x, 0) for x in set(list_positive).union(list_negative)}
print(len(list_total))



#Calculate priors
count_1 = sum(list_positive.values())
count_0 = sum(list_negative.values())
P_y_1 = count_1 / (count_0+count_1)
P_y_0 = count_0 / (count_0+count_1)
print(P_y_0, P_y_1, count_0, count_1)

#Calculate likelihood for all words
t = list(list_total.keys())
t.sort()
print(t)
print(len(t))
P_w_y_0 = {}
P_w_y_1 = {}
for i in t:
    print(i)
    if i in list_negative.keys():
        P_w_y_0[i] = (list_negative[i] / count_0)
    else:
        P_w_y_0[i] = 0

    if i in list_positive.keys():
        P_w_y_1[i] = (list_positive[i] / count_1)
    else:
        P_w_y_1[i] = 0

# predict function calculation
vocab_list = ['vomit', 'zodiac']
P_y_w_0 = P_y_0
P_y_w_1 = P_y_1
for word in vocab_list:
    P_y_w_0 *= P_w_y_0[word]
    P_y_w_1 *= P_w_y_1[word]

print(P_y_w_0, P_y_w_1)
if P_y_w_0 > P_y_w_1:
    print("Label - 0")
elif P_y_w_0 < P_y_w_1:
    print("Label - 1")
else:
    print("Tie")


#print(P_w_y_0['you'])
#print(P_w_y_1['you'])
