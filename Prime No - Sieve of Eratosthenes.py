__author__ = 'Sushant'

def SofE(m, n):
    Result = []
    prime = [True for i in range(n+1)]
    p = 2
    while p*p <= n:
        if prime[p]:
            for j in range(p*2, n+1, p):
                prime[j] = False
        p += 1

    # Print all prime numbers
    for p in range(2, n+1):
        if prime[p] and p >= m:
            Result.append(p)
    return Result

min1 = 100000000000000000000000000000000000000000
max1 = 0
no = int(input())
Limits = []
for o in range(no):
    N = list(map(int, input().split()))
    Li = SofE(N[0], N[1])
    for p in Li:
        print(p)