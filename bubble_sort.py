"""
Bubble sort algorithm on a list
Take list as an input
Compare each pair of adjacent items in the list
Swap if needed
End when a pass is made with no swaps in it
Returns the sorted list
"""

data = [2,7,3,8,9,4,5,6,1]

def bubbleSort(data):
    swapped = True
    #Repeats until a pass with no swaps is made
    while swapped:
        swapped = False
        #Compares each adjacent pair of items in the list
        for i in range(0,len(data)-1):
            if data[i] > data[i+1]:
                #Swaps the values
                buffer = data[i]
                data[i] = data[i+1]
                data[i+1] = buffer
                swapped = True
    return data

print(bubbleSort(data))
