__author__ = 'Sushant'

N = list(map(int, input().split()))
L = len(N)
print(L)
def get_node_children(pos):
    left = (2*pos)+1
    right = (2*pos)+2
    if L < left or L < right:
        print("Solution found: ", pos, N[pos])
        exit()
    print(pos, left, right)
    if N[pos] < N[left] and N[pos] < N[right]:
        print("Solution found: ", pos, N[pos])
        exit()
    elif N[pos] > N[left]:
        get_node_children(left)
    elif N[pos] > N[right]:
        get_node_children(right)

get_node_children(0)




