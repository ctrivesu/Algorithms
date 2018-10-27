__author__ = 'Sushant'

from scipy.sparse import csr_matrix
import numpy as np
mypath = '''C:/Users/Sushant/Desktop/Movie Review Dataset/movie review data/'''
fp = open(mypath+'spmatrix.txt', 'w', encoding='utf-8')
data = np.array([1, 2, 3])
row = np.array([1, 2, 3])
col = np.array([1, 2, 3])
t = csr_matrix((data, (row, col)), shape=(4, 4))
print(t)
fp.write(str(t))
print(t.toarray())
print(t.data)
fp.close()
print("WRITE COMPLETED")
fp = open(mypath+'spmatrix.txt', 'r', encoding='utf-8')
readdata = fp.read()
print(readdata)
print("Dsf")
t = readdata.replace('(', '')

l = {'a':1, 'c':3, 'b':2, 'd':4}
k = list(l.keys())
v = list(l.values())
print(k)
print(v)

list_1 = ["a","e","d","w","s","f"]
list_2 = ["a", "f", "c", "m"]
print(list_1)
print(list_2)
print(list(set(list_2) - set(list_1)))





'''
#print(t.col())

mydict = {'carl':40,
          'alan':2,
          'bob':1,
          'danny':3}

print(sorted(mydict))
'''
