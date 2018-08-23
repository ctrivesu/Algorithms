__author__ = 'Sushant'
# #################### Q1. COUNT PYRAMID ##################################

'''
def cas(N):
    List = [1]
    i = 0
    while i < N-1:
        count = 0
        Temp = []
        L = len(List)
        j = 0
        while j < L:
            if j == L - 1:
                count += 1
                Temp.append(count)
                Temp.append(List[j])
                break
            elif List[j] == List[j + 1]:
                count += 1
                j += 1
            else:
                Temp.append(count+1)
                Temp.append(List[j])
                count = 0
                j += 1
        List.clear()
        List = Temp
        i += 1
    print("".join(map(str, List)))

no = int(input())
cas(no)
'''

# ################## Q2. LARGEST SUB ARRAY ###############################

'''
def mcs(a, low1, mid1, high1):
    maxleft = -10000000000000000000000000
    maxright = -1000000000000000000000000
    leftsum1 = -1000000000000000000000000

    neginf = -10000000000
    sum1 = 0
    for i in range(mid1, low1-1, -1):
        sum1 += a[i]
        if sum1 > neginf:
            neginf = sum1
            maxleft = i
        leftsum1 = neginf

    neginf = -10000000000

    sum1 = 0
    for j in range(mid1+1, high1+1):
        sum1 = sum1 + a[j]
        if sum1 > neginf:
            neginf = sum1
            maxright = j
        rightsum1 = neginf
    return maxleft, maxright, (leftsum1 + rightsum1)


def ms(a, low2, high2):
    if high2 == low2:
        return low2, high2, a[low2]
    else:
        mid2 = int((low2 + high2)/2)
        leftlow2, lefthigh2, leftsum2 = ms(a, low2, mid2)
        rightlow2, righthigh2, rightsum2 = ms(a, mid2+1, high2)
        clow2, chigh2, csum2 = mcs(a, low2, mid2, high2)

        if leftsum2 >= rightsum2 and leftsum2 >= csum2:
            return leftlow2, lefthigh2, leftsum2
        elif rightsum2 >= leftsum2 and rightsum2 >= csum2:
            return rightlow2, righthigh2, rightsum2
        else:
            return clow2, chigh2, csum2

List = list(map(int, input().split()))
low, high, sum3 = ms(List, 0, len(List)-1)
print("Largest Sum: ", sum3)
print("Subarray is: ", List[low:high+1])
'''

# ############## Q3. LENGTH OF THE LAST WORD ##################

# --------------- SHORT METHOD -------------------
'''
def lol(s):
        List = s.split()
        L = len(List)
        if L != 0:
            return len(List[L-1])
        else:
            return 0
List = input()
print(lol(List))
'''
# --------------- LONG METHOD -------------------
'''
def lol(List):
    count = 0
    LastWord = []
    wtrack = 0
    t = 0
    if len(List) == 0:
        return 0
    for i in List[::-1]:
        t += 1
        if len(List) == 1 and i != ' ':
            count += 1
            return count
        elif len(List) == 1:
            return 0
        if i == ' ' and wtrack == 0:
            continue
        else:
            wtrack = 1
            if i == ' ':
                return count
            count += 1
            if t == len(List):
                return count
            LastWord.append(i)
    return 0
List = input()
print(lol(List))
'''
# #################### Q4. MESSAGE DECODED #################
'''
# -------------- RECURSION ----------------------------
def cou(n):
    ct = 0
    if n == 0 or n == 1:
        return 1
    if List[n-1] > 0:
        ct = cou(n-1)
    if (List[n-2] == 1) or ((List[n-2] == 2) and (List[n-1] < 7)):
        ct += cou(n-2)
    return ct

List = list(map(int, input()))
N = len(List)
if N != 0 and List[0] != 0:
    print("Method 1: ", cou(N))
else:
    print("Method 1: 0")
    print("Method 2: 0")
    exit()

# ---------------DYNAMIC PROGRAMMING-------------------
count = [1, 1] + [0]*(N-1)
for i in range(2, N+1):
    count[i] = 0
    if List[i-1] > 0:
        count[i] = count[i-1]
    if (List[i-2] == 1) or ((List[i-2] == 2) and (List[i-1] < 7)):
        count[i] += count[i-2]

print("Method 2: ", count[N])
'''


# #################### Q5. MIN IN A PYRAMID ####################################

'''
def triangleminsumpath(tria):
    levels = len(tria)
    dp = [x[:] for x in [[0] * levels] * levels]
    dp[levels-1] = tria[levels-1]
    for l in range(levels-2, -1, -1):
        for i in range(0, l+1):
            dp[l][i] = min(dp[l+1][i], dp[l+1][i+1]) + tria[l][i]
    return dp[0][0]
List = []
while True:
    i = list(map(int, input().split()))
    if len(i) == 0:
        break
    List.append(i)
print(List)
print("Minimum sum: ", triangleminsumpath(List))
'''

###############################################################################



