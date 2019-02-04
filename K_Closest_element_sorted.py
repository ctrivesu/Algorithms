__author__ = 'Sushant'

def elem_X(arr, low, high, x):
    if arr[high] <= x:
        return high
    elif arr[low] > x:
        return low
    mid = int(low + ((high - low) / 2))
    if arr[mid] <= x < arr[mid + 1]:
        return mid

    if arr[mid] < x:
        return elem_X(arr, mid + 1, high, x)

    return elem_X(arr, low, mid - 1, x)

def Kclosest(arr, x, k, N):

    l = elem_X(arr, 0, N - 1, x)
    r = l + 1
    count = 0

    if arr[l] == x:
        l -= 1

    while l >= 0 and r < N and count < k:
        if x - arr[l] < arr[r] - x:
            print(arr[l], end=" ")
            l -= 1
        else:
            print(arr[r], end=" ")
            r += 1
        count += 1

    while count < k and l >= 0:
        print(arr[l], end=" ")
        l -= 1
        count += 1

    while count < k and r < N:
        print(arr[r], end=" ")
        r += 1
        count += 1

if __name__ == "__main__":
    arr = [12, 16, 22, 30, 35, 39, 42, 45, 48, 50, 53, 55, 56]
    n = len(arr)
    x = 35
    k = 4
    Kclosest(arr, x, 4, n)

