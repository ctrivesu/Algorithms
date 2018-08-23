__author__ = 'Sushant'

N = list(map(int, input().split()))
L = len(N)
print(N, L)
def binsearch(left, right):
    mid = int((left+right+1)/2)
    if 0 < mid < L-1:
        if N[mid-1] < N[mid] > N[mid+1]:
            return mid
        elif N[mid-1] < N[mid] < N[mid+1]:
            return binsearch(mid+1, right)
        elif N[mid-1] > N[mid] > N[mid+1]:
            return binsearch(0, mid-1)
    elif mid == 0:
        return 0
    elif mid == L-1:
        return L-1

Ans = binsearch(0, L-1)
print("Peak Element: ", N[Ans])





