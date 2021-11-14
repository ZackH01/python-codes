"""
Insertion sort
Select value in the list
Swap with the values to the left of itself until its in the correct position
Move on to the next value
Repeat until the list is sorted
"""

data = [5,2,8,7,1,3,4,9,6]

def insertionSort(data):
    for i in range(0, len(data)):
        #Compare current item with every item before it and swap if needed
        for j in range(0, i):
            if data[i-j] < data[i-j-1]:
                buffer = data[i-j]
                data[i-j] = data[i-j-1]
                data[i-j-1] = buffer
            else:
                break
    return data

print(insertionSort(data))
            
