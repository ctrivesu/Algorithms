__author__ = 'Sushant'
Result = []
for i in range(int(input())):
    N = int(input())
    List = list(map(int, input().split()))
    count = 0
    for j in range(0, N - 1):
        for k in range(j + 1, N):
            if List[j] | List[k] <= max(List[j], List[k]):
                count += 1
    print(count)
