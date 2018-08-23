__author__ = 'Sushant'

for i in range(int(input())):
    Count1 = {}
    Count2 = {}
    Len1 = {}
    Len2 = {}
    A = (input())
    B = (input())
    for j in A:
        c1 = A.count(j)
        L1 = [i for i in range(len(A)) if A.startswith(j, i)]
        Count1[j] = L1
        Len1[j] = len(L1)
    for k in B:
        c2 = B.count(k)
        L2 = [lk for lk in range(len(B)) if B.startswith(k, lk)]
        Count2[k] = L2
        Len2[k] = len(L2)
    print(Count1, Count2, Len1, Len2)
