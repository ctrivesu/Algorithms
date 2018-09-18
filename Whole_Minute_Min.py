__author__ = 'Sushant'


''' WHOLE MIN DILEMA: Find pair of minutes in the given array of seconds that sum up to whole minutes '''
#TEST CASES
array = [10, 50, 90, 30] #2
#array = [30, 20, 150, 100, 40] #3
#array = [60, 60, 60] #3


#CODE
dict = {}
print(array)
for i in array:
    mod = i % 60
    if mod in dict.keys():
        dict[mod] = (dict[mod]) + [i]
    else:
        dict[mod] = [i]

count = 0
read = []
print(dict)
for i in array:
    if i != 60:
        mod = i % 60
        rem = 60 - mod
    else:
        mod = i
        rem = 0
    if i in read:
        continue
    if rem not in read and rem != mod:
        count += len(dict[rem])
        read.append(mod)
    elif rem not in read and rem == mod:
        t = len(dict[mod]) - 1
        count += (t*(t+1))/2
        read.append(mod)
    else:
        pass
print(count)






