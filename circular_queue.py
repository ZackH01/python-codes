"""
Class for a circular queue data structure

Data is only added to the rear and removed from the front

Construct: identifier = Queue(size) #size is an integer

enqueue(item) adds input value to the back of the queue if it is not full
dequeue() removes and returns the value at the front of the queue if it is not empty
peek() returns the value at the front of the queue if it is not empty
view() returns the queue's contents
"""

class Queue:
    #Attributes
    data = []
    size = 0
    front_pointer = 0
    rear_pointer = 0

    #Methods
    def __init__(self, size):
        #Constructor
        self.size = size

        #Validate input and initialise queue
        try:
            int(self.size)
        except ValueError:
            raise ValueError("Size parameter must be an integer") from None
        else:
            if self.size < 0:
                raise ValueError("Size parameter must be 0 or greater") from None
            else:
                self.data = [None]*self.size

    def enqueue(self, item):
        #Adds item to the rear of the queue if the queue is not full
        try:
            self.data[self.rear_pointer]
        except IndexError:
            raise IndexError("Queue size is zero") from None

        if self.data[self.rear_pointer] == None:
            self.data[self.rear_pointer] = item
            self.rear_pointer += 1

            if self.rear_pointer > self.size-1:
                self.rear_pointer = 0
        else:
            raise IndexError("Queue is full") from None

    def dequeue(self):
        #Removes and returns front item if the queue is not empty
        if self.front_pointer == self.rear_pointer:
            raise IndexError("Queue is empty") from None
            return
        else:
            result = self.data[self.front_pointer]
            self.data[self.front_pointer] = None
            self.front_pointer += 1

            if self.front_pointer > self.size-1:
                self.front_pointer = 0
                
        return result

    def peek(self):
        #Returns the front item if the queue is not empty
        if self.front_pointer == self.rear_pointer:
            raise IndexError("Queue is empty") from None
            return
        else:
            return self.data[self.front_pointer]

    def view(self):
        #Returns the queue's contents
        return self.data


