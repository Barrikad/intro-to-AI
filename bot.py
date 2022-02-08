#IMPROVEMENTS
#depth-search limit
#search heuristics
#hash-table of considered states to avoid redoing work
#remove recursion
#replace state traces with move traces
#agent running concurrently with game
#better frontier algorithm

#datatype trace: state -> (next state -> trace) map

#Type variables:
#   action - should be immutable, equalityable, and hashable
#   state  - should be immutable, equalityable, and hashable

class Node:
    def __init__(self,state,children,parents,value):
        self.state = state
        self.children = children #map: action -> Node
        self.parents = parents
        self.value = value
        #value

class Frontier:
    def __init__(self):
        self.nodes = []

    def insert(self,node):
        self.nodes.append(node)

    def extract(self):
        return self.nodes.pop()

class Agent:
    def __init__(
            self,
            evaluator,getActions,simulator,ourTurn,
            emptyFrontier,
            startState):
        self.ourTurn = ourTurn
        self.getActions = getActions #fun: state -> action list
        self.simulator = simulator #fun: state -> action -> state
        self.evaluator = evaluator #fun: 
        self.frontier = emptyFrontier
        
        self.tree = Node(startState,{},[],evaluator(startState))
        self.stateMap = {startState : self.tree}
        self.frontier.insert(self.tree)

    def updateBranchValue(self,node):
        value = node.value
        curNodes = [node]
        while curNodes != []:
            curNode = curNodes.pop()
            for parent in curNode.parents:
                parentTooLow = (
                    self.ourTurn(parent.state) and parent.value < value)
                parentTooHigh = (
                    not self.ourTurn(parent.state) and parent.value > value)
                if parentTooLow or parentTooHigh:
                    parent.value = value
                    curNodes.append(parent)

    def expandNode(self,node):
        cmp = None
        valueChild = None
        if self.ourTurn(node.state):
            cmp = lambda a,b : a < b
        else:
            cmp = lambda a,b : a > b

        for act in self.getActions(node.state):
            actState = self.simulator(node.state,act)
            if actState in self.stateMap:
                node.children[act] = self.stateMap[actState]
                node.children[act].parents.append(node)
            else:
                node.children[act] = Node(
                    actState,{}, node, self.evaluator(actState))
                self.frontier.insert(node.children[act])
            if (valueChild == None or 
                cmp(valueChild.value,node.children[act].value)):
                valueChild = node.children[act]
        self.updateBranchValue(valueChild)

    def calculate(self):
        node = self.frontier.extract()
        self.expandNode(node)

    def printTree(self):
        print("TODO")