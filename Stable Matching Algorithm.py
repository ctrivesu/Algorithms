__author__ = 'Sushant'

# STABLE MATCHING ALGORITHM
# Left side is the most preferred in the array [0, 1, 2]
wp = [[0, 1, 2], [1, 0, 2], [0, 1, 2]]
mp = [[1, 0, 2], [0, 1, 2], [0, 1, 2]]

# Array with -1 if none chose and no of person if chosen
mc = [-1, -1, -1]
wc = [-1, -1, -1]

# count of people proposed
mcount = [0, 0, 0]
wcount = [0, 0, 0]


def ptay(x):
    for g in x:
        print(g)
    print("\n")

ptay(mp)
ptay(wp)
print("------------------")
# first iteration
N = 3   # matrix size
while mc.count(-1) != 0:
    for i in range(N):
        if mc[i] == -1 and (mcount[i] != N):
            womanasked = mp[i][mcount[i]]
            mcount[i] += 1
            if wc[womanasked] == -1:
                wc[womanasked] = i
                mc[i] = womanasked
                wcount[womanasked] += 1
            elif wp[womanasked].index(i) < wp[womanasked].index(wc[womanasked]):
                mc[wc[womanasked]] = -1
                wc[womanasked] = i
                mc[i] = womanasked
                wcount[womanasked] += 1
            else:
                continue
            print(" ", mc, "\n ", wc)

print("------------------")
print("male")
print(mc)
print(mcount)
print("female")
print(wc)
print(wcount)


