"""
Class for a stack data structure

A stack is a data structure where items are only accessed from the top and items are
only added to the top (first in last out)

Construct: identifier = Stack(size) #Size is an integer
    
push(value) adds input value to the top of the stack if it is not full
pop() removes and returns the top value if the stack is not empty
peek() returns the top value if the stack is not empty
view() returns the stack's contents
"""

class Stack:
    #Attributes
    data = []
    size = 0
    top_pointer = -1 #Set to -1 when the stack is empty

    #Methods
    def __init__(self, size):
        #Constructor
        self.size = size

        #Validate input and initialise stack
        try:
            int(self.size)
        except ValueError:
            raise ValueError("Size attribute must be an integer!") from None
        else:
            if self.size < 0:
                raise ValueError("Size attribute must be 0 or greater")
            else:
                for i in range(0,self.size):
                    self.data.append(None)

    def push(self, value):
        #Push the passed value to the top of the stack if it is not full
        try:
            self.data[self.top_pointer + 1]
        except IndexError:
            raise IndexError("Stack is full!") from None 
        else:
            self.top_pointer += 1
            self.data[self.top_pointer] = value

    def pop(self):
        #Removes top item from the stack and returns the value if the stack is not empty
        if self.top_pointer <= -1:
            raise IndexError("Stack is empty!")
        else:
            result = self.data[self.top_pointer]
            self.data[self.top_pointer] = None
            self.top_pointer -= 1
            return result

    def peek(self):
        #Return value of the top item if the stack is not empty
        if self.top_pointer <= -1:
            raise IndexError("Stack is empty!")
        else:
            return self.data[self.top_pointer]

    def view(self):
        #Returns the stack's contents
        return self.data


