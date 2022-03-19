from collections import deque
from bot import Node
from util import MIN_INT

#TWEAK AREA:
MAX_VALUE = 10000

class Stack:
    def __init__(self):
        self.nodes = deque()

    def insert(self,node):
        self.nodes.append(node)

    def extract(self):
        return self.nodes.pop()

    def empty(self):
        return not self.nodes
    
    def contains(self,node):
        return node in self.nodes

    def reprioritize(self,newRoot):
        if newRoot in self.nodes:
            self.nodes.remove(newRoot)
            self.nodes.append(newRoot)

class Queue:
    def __init__(self):
        self.nodes = deque()

    def insert(self,node):
        self.nodes.append(node)

    def extract(self):
        return self.nodes.popleft()

    def empty(self):
        return not self.nodes
    
    def contains(self,node):
        return node in self.nodes
        
    def reprioritize(self,newRoot):
        if newRoot in self.nodes:
            self.nodes.remove(newRoot)
            self.nodes.appendleft(newRoot)

#Scheme for heap frontier
#each node in the frontier will be given a value based on how interesting they are to expand
#keep track of nodes in frontier in a max-heap
#reevaluate all nodes when root changes, 
# if root is unreachable drop them from the frontier

#problems
#if a state is found in an inefficient way (or considered unreachable), it might later be found in a quicker way
#it would then have to be reprioritized in the frontiers

#reprioritation is something we should anticipate actually, since it kinda is the point of max heap
#make reprioritation easy be storing heap index in node :)

#thoughts on interest value
#nodes close to root are interesting as they are more likely to be relevant
#actions can have intrinsic interest-values (requires knowing which action lead to the state)
#high value states after our actions are interesting because we should search for negative results of seemingly good decisions
#low value states after opponents turn are interesting because they are more likely to be picked by opponent


class Heap:
    def __init__(self,ourTurn):
        self.nodes = [] #contains pairs of (value,node) where first element is interest value
        self.ourTurn = ourTurn
    
    def empty(self):
        return self.nodes == []

    def insert(self,node):
        v = self.evaluate(node)
        self.nodes.append((v,node))
        self.nodes[len(self.nodes) - 1][1].heapIndex = len(self.nodes) - 1
        self.bubbleUp(len(self.nodes) - 1)
    
    def extract(self):
        head = self.nodes[0]
        if len(self.nodes) > 1:
            self.nodes[0] = self.nodes[len(self.nodes) - 1]
            self.nodes[0][1].heapIndex = 0
        self.nodes.pop()
        if len(self.nodes) > 1:
            self.bubbleDown(0)
        head[1].heapIndex = None
        return head[1] #return just node and not value
    
    def bubbleUp(self,i):
        p = i // 2 #parent index
        while i > 0 and self.nodes[i][0] > self.nodes[p][0]:
            temp = self.nodes[p]
            self.nodes[p] = self.nodes[i]
            self.nodes[i] = temp
            self.nodes[i][1].heapIndex = i
            self.nodes[p][1].heapIndex = p
            i = p
            p = i // 2

    def bubbleDown(self,i):
        maxc = i #use self to quit loop if no child exists
        if i * 2 < len(self.nodes):
            maxc = i * 2 #use left child
            if maxc + 1 < len(self.nodes) and self.nodes[maxc + 1][0] > self.nodes[maxc][0]:
                maxc += 1 #use right child if bigger than left
        while self.nodes[maxc][0] > self.nodes[i][0]: #will quit if i = maxc, i.e. when there is no child
            temp = self.nodes[maxc]
            self.nodes[maxc] = self.nodes[i]
            self.nodes[i] = temp
            self.nodes[i][1].heapIndex = i
            self.nodes[maxc][1].heapIndex = maxc
            i = maxc #use self to quit loop if no child exists
            if i * 2 < len(self.nodes):
                maxc = i * 2 #use left child
                if maxc + 1 < len(self.nodes) and self.nodes[maxc + 1][0] > self.nodes[maxc][0]:
                    maxc += 1 #use right child if bigger than left

    def reevaluate(self,node):
        if node.heapIndex == None:
            return
        vnew = self.evaluate(node)
        vold = self.nodes[node.heapIndex][0]
        self.nodes[node.heapIndex] = (vnew,node)
        if vnew > vold:
            self.bubbleUp(node.heapIndex)
        else:
            self.bubbleDown(node.heapIndex)
    
    def reset(self,node):
        if node.heapIndex != None:
            self.nodes[node.heapIndex] = (MIN_INT,node)
            self.bubbleDown(node.heapIndex)
    
    #REPRIORITAZE NOTES
    #set steps of all nodes in frontier to max
    #calculate new steps
    #   When node with heapIndex is encountered add it to frontier
    
    #much quicker traversal than ordinary calculate() because we
    #don't have to use the simulator
    #also similar behaviour to iterative deepening
    #also only done once quite rarely

    #what if a node that was thought unreachable is encountered again?
    #don't remove from frontier, just make step cost extremely high
    
        
    #TWEAK AREA:
    def evaluate(self,node):
        iv = 0
        iv -= 3000 * node.steps
        for parent in node.parents: #for each state leading into this one
            #add interest for close parents
            iv += max(0,1000 - parent.steps*150)
            if self.ourTurn(parent.state):
                iv += node.value #interesting if we can choose a high-value state
            else:
                iv += -node.value #interesting if opponent can choose low-value state
        return iv

#0 1 2 3 4 5 6
#1 2 5 3 4 6 7
