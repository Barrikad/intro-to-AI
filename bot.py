#IMPROVEMENTS
#search heuristics
#agent running concurrently with game
#better frontier algorithm
#don't choose looping actions if avoidable
#randomize choice of near equal actions
#try monte carlo
#alpha-beta pruning (this might not actually influence performance as we almost never have nodes with static value)
#test bot with much datapower against bot with little

#PROPERTIES OF A GOOD AI
#quality of solution should be proportional to provided computational-power:
#-a somewhat sensical action should be chosen even if goal has not been found
#-something like breadth first search is preferable
#

#Type variables:
#   action - should be immutable, equalityable, and hashable
#   state  - should be immutable, equalityable, and hashable

from collections import deque
import random

from util import MAX_INT


class Node:
    def __init__(self,state,children,parents,value):
        self.state = state 
        self.children = children #map: action -> Node
        self.parents = parents #Node list
        self.value = value #int
        self.heapIndex = None

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
        self.evaluator = evaluator #fun: state -> int
        self.frontier = emptyFrontier
        
        self.tree = Node(startState,{},[],evaluator(startState))
        self.tree.steps = 0 #number of steps from root
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
                if self.stateMap[actState].steps > node.steps + 1:
                    self.stateMap[actState].steps = node.steps + 1
                    if self.stateMap[actState].heapIndex != None:
                        self.frontier.reevaluate(self.stateMap[actState])
            else:
                node.children[act] = Node(
                    actState,{}, [node], self.evaluator(actState))
                node.children[act].steps = node.steps + 1
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
            bestActs = []
            bestValue = None
            for act in self.tree.children:
                if bestValue == None or self.tree.children[act].value > bestValue + 10:
                    bestActs = [act]
                    bestValue = self.tree.children[act].value
                elif abs(self.tree.children[act].value - bestValue) <= 10:
                    bestActs.append(act)
            if bestActs == []:
                return None
            return random.choice(bestActs)

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
        self.redoSteps()
        
    def redoSteps(self):
        for state in self.stateMap:
            node = self.stateMap[state]
            node.steps = MAX_INT
            if node.heapIndex != None:
                #reaching directly into the frontier, not good
                self.frontier.nodes[node.heapIndex] = (0,node)
        self.setSteps(self.tree,0)

    def setSteps(self,node,level):
        node.steps = level
        if node.heapIndex != None:
            self.frontier.reevaluate(node)
        for act in node.children:
            if node.children[act].steps > level + 1:
                self.setSteps(node.children[act],level + 1)

    def printTree(self):
        printNode(self.tree,0)