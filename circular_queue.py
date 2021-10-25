"""
Class for a circular queue data structure

Data is only added to the rear and removed from the front
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
        self.data = [None]*self.size

    def enqueue(self, item):
        #Adds item to the rear of the queue if the queue is not full
        if self.data[self.rear_pointer] == None:
            self.data[self.rear_pointer] = item
            self.rear_pointer += 1

            if self.rear_pointer > self.size-1:
                self.rear_pointer = 0
        else:
            print("Queue is full")
        
        print(self.data)

    def dequeue(self):
        #Removes and returns front item if the queue is not empty
        if self.front_pointer == self.rear_pointer:
            print("Queue is empty")
            return
        else:
            result = self.data[self.front_pointer]
            self.data[self.front_pointer] = None
            self.front_pointer += 1

            if self.front_pointer > self.size-1:
                self.front_pointer = 0
                
        print(self.data)
        return result


queue = Queue(5)
queue.enqueue(1)
queue.enqueue(2)
queue.dequeue()
queue.dequeue()
queue.dequeue()
