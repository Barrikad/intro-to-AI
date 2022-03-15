from collections import deque

class Stack:
    def __init__(self):
        self.nodes = deque()

    def insert(self,node):
        self.nodes.append(node)

    def extract(self):
        return self.nodes.pop()

    def empty(self):
        return not self.nodes

    #ad hoc functions, should be replaced
    def contains(self,node):
        return (node in self.nodes)

    def prioritize(self,node):
        self.nodes.remove(node)
        self.nodes.append(node)

class Queue:
    def __init__(self):
        self.nodes = deque()

    def insert(self,node):
        self.nodes.append(node)

    def extract(self):
        return self.nodes.popleft()

    def empty(self):
        return False if self.nodes else True
        
    #ad hoc functions, should be replaced
    def contains(self,node):
        return (node in self.nodes)

    def prioritize(self,node):
        self.nodes.remove(node)
        self.nodes.appendleft(node)