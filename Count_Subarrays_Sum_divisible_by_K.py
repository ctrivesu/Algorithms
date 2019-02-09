__author__ = 'Sushant'
# REF: https://www.geeksforgeeks.org/count-sub-arrays-sum-divisible-k/
# Used only to understand the concept

def count_div_arr(arr, n, k):

    # initialize an array of size k with zero
    mod = [0] * k

    # create an array of count of arrays [0,i] with mod k as index
    sum = 0
    for elem in arr:
        sum += elem
        mod[((sum % k) + k) % k] += 1

    # count the possible sum of sub arrays divisible by k
    count = 0
    for i in mod:
        if i > 1:
            count += (i * (i - 1)) // 2

    count += mod[0]
    print("SUB-ARRAY COUNT: ", count)

# EXAMPLE OUTPUT
# arr = [4, 5, 0, -2, -3, 1]
# Sample Input: 4 5 0 -2 -3 1
arr = list(map(int, (input("Enter the array of no with spaces in between: ").split(" "))))
N = len(arr)

# Sample Input:5
K = input("Enter the value of k: ")
count_div_arr(arr, N, int(K))

# Sample Output: SUB-ARRAY COUNT:  7




