#IMPROVEMENTS
#search heuristics
#replace state traces with move traces
#agent running concurrently with game
#better frontier algorithm
#make so bots can play eachother
#don't choose looping actions if avoidable
#randomize choice of near equal actions

#PROPERTIES OF A GOOD AI
#quality of solution should be proportional to provided computational-power:
#-a somewhat sensical action should be chosen even if goal has not been found
#-something like breadth first search is preferable
#

#Type variables:
#   action - should be immutable, equalityable, and hashable
#   state  - should be immutable, equalityable, and hashable

from collections import deque


class Node:
    def __init__(self,state,children,parents,value):
        self.state = state 
        self.children = children #map: action -> Node
        self.parents = parents #Node list
        self.value = value #int

def printNode(node,level):
    print(" " * level + str(node.state))
    for act in node.children:
        printNode(node.children[act],level + 1)

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
        nodes = deque()
        nodes.append(node)
        while nodes:
            curNode = nodes.pop()
            valueChild = None
            for act in curNode.children:
                childValue = curNode.children[act].value
                if (valueChild == None
                        or (self.ourTurn(curNode.state) and valueChild < childValue) 
                        or (not self.ourTurn(curNode.state) and valueChild > childValue)):
                    valueChild = childValue
            if valueChild and curNode.value != valueChild:
                curNode.value = valueChild
                for parent in curNode.parents:
                    nodes.append(parent)

    def expandNode(self,node):
        possibleActions = self.getActions(node.state)

        for act in possibleActions:
            actState = self.simulator(node.state,act)
            if actState in self.stateMap:
                node.children[act] = self.stateMap[actState]
                self.stateMap[actState].parents.append(node)
            else:
                node.children[act] = Node(
                    actState,{}, [node], self.evaluator(actState))
                self.frontier.insert(node.children[act])
                self.stateMap[actState] = node.children[act]
        
        self.updateBranchValue(node)

    def calculate(self):
        if not self.frontier.empty():
            node = self.frontier.extract()
            self.expandNode(node)

    def bestAction(self):
        if not self.ourTurn(self.tree.state):
            return None
        else:
            bestAct = None
            bestValue = None
            for act in self.tree.children:
                if bestAct == None or self.tree.children[act].value > bestValue:
                    bestAct = act
                    bestValue = self.tree.children[act].value
            return bestAct

    def updateState(self,state):
        if state in self.stateMap:
            if not self.stateMap[state] in self.tree.children.values():
                print("Warning: impossible transition")
            self.tree = self.stateMap[state]
        else:
            #new state was not considered possible
            print("Warning: moved to state outside stateMap")
            self.tree = Node(state,{},[],self.evaluator(state))
            self.stateMap[state] = self.tree
            self.frontier.insert(self.tree)

    def removeUnreachableFrontiers(self):
        pass

    def printTree(self):
        printNode(self.tree,0)