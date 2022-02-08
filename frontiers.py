from collections import deque

class Stack:
    def __init__(self):
        self.nodes = deque()

    def insert(self,node):
        self.nodes.append(node)

    def extract(self):
        return self.nodes.pop()
    
    def empty(self):
        return False if self.nodes else True

class Queue:
    def __init__(self):
        self.nodes = deque()

    def insert(self,node):
        self.nodes.append(node)

    def extract(self):
        return self.nodes.popleft()
    
    def empty(self):
        return False if self.nodes else True