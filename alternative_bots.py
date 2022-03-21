from cmath import log, sqrt
from collections import deque
import bot 
import frontiers
from util import MIN_INT
import random
import laserchess as lc
import math

#heap with lower punishment for steps
class Heap2(frontiers.Heap):
    def evaluate(self, node):
        iv = super().evaluate(node)
        iv += 1000 * node.steps
        return iv

#MONTE CARLO BOT-------------------------------

#ucb
def ucb(node):
    if not node.parent:
        parentPlays = node.plays
    else:
        parentPlays = node.parent.plays
    winRatio = (node.plays - node.wins) / node.plays 
    exploration = math.sqrt(2*math.log(parentPlays) / node.plays)
    return winRatio + exploration

def deleteTree(node):
    toDelete = deque()
    toDelete.append(node)
    while toDelete:
        node = toDelete.popleft()
        for act in node.children:
            if node.children[act]:
                toDelete.append(node.children[act])
        del node

class MCNode:
    def __init__(self,state,parent):
        self.state = state
        self.children = {}
        self.parent = parent
        self.plays = 0
        self.wins = 0
        self.ucb = 0

#monte carlo bot
class MCBot():
    def __init__(
            self,
            won,getActions,simulator,
            startState,
            rolloutLimit):
        self.getActions = getActions #fun: state -> action list
        self.simulator = simulator #fun: state -> action -> state
        self.won = won #won should give None if nonterminal, 0 for loss, 0.5 for tie, and 1 for win
        self.rolloutLimit = rolloutLimit
        
        self.tree = MCNode(startState,None)
    
    def select(self):
        node = self.tree
        while True:
            maxChild = None
            maxUCB = MIN_INT
            noneChildren = False
            for child in node.children:
                if not node.children[child]:
                    noneChildren = True
                else:
                    childUCB = ucb(node.children[child])
                    if childUCB > maxUCB:
                        maxChild = node.children[child]
                        maxUCB = childUCB
            if not maxChild or (noneChildren and maxUCB <= ucb(node)):
                break
            else:
                node = maxChild
        return node
                
    def expand(self,node):
        if not node.children:
            for act in self.getActions(node.state):
                node.children[act] = None
        rotationExpansions = []
        otherExpansions = []
        for act in node.children:
            if not node.children[act]:
                if act[0] == "r":
                    rotationExpansions.append(act)
                else:
                    otherExpansions.append(act)
        if rotationExpansions == [] and otherExpansions == []:
            result = self.rollout(node)
            self.backPropogate(node,result)
            return
        
        pickRot = random.random() #random number between 0 and 1
        pickRot += 0.2 #reduce chance that rotation is picked by 20%
        pickRot = max(pickRot,1)
        rotRatio = len(rotationExpansions)/(len(rotationExpansions) + len(otherExpansions))
        if pickRot <= rotRatio or not otherExpansions: #if there are only rots this will always be true
            act = random.choice(rotationExpansions)
        else:
            act = random.choice(otherExpansions)
        node.children[act] = MCNode(self.simulator(node.state,act),node)
        result = self.rollout(node.children[act])
        self.backPropogate(node.children[act],result)

    
    def rollout(self,node):
        state = node.state
        for _ in range(self.rolloutLimit):
            acts = self.getActions(state)
            if not acts:
                break
            rotationExpansions = []
            otherExpansions = []
            #get actions preferably not rotation
            for act in acts:
                if act[0] == "r":
                    rotationExpansions.append(act)
                else:
                    otherExpansions.append(act)
            if rotationExpansions == [] and otherExpansions == []:
                return 
            pickRot = random.random() #random number between 0 and 1
            pickRot += 0.2 #reduce chance that rotation is picked by 20%
            pickRot = max(pickRot,1)
            rotRatio = len(rotationExpansions)/(len(rotationExpansions) + len(otherExpansions))
            if pickRot <= rotRatio or not otherExpansions:
                act = random.choice(rotationExpansions)
            else:
                act = random.choice(otherExpansions)
            
            state = self.simulator(state,act)
        w = self.won(state[1])  
        if w:
            return w
        return "tie"

    def backPropogate(self,node,result):
        while node:
            if result == "tie": 
                node.wins += 0.5
            elif result == lc.curPlayer(node.state):
                node.wins += 1
            node.plays += 1
            node = node.parent

    def calculate(self):
        node = self.select()
        self.expand(node)

    def updateState(self,state):
        node = None
        for act in self.tree.children:
            if self.tree.children[act] and self.tree.children[act].state == state:
                node = self.tree.children[act]
                break
            elif self.tree.children[act]:
                deleteTree(self.tree.children[act]) #delete non-chosen subtrees
        if node == None:
            print("Warning: impossible transition")
            deleteTree(self.tree)
            self.tree = MCNode(state,None)
            return
        
        del self.tree
        self.tree = node
        self.tree.parent = None
    
    def bestAction(self,playingLaserchess = True):
        maxAct = None
        maxPlays = 0
        for act in self.tree.children:
            if self.tree.children[act]:
                if self.tree.children[act].plays > maxPlays:
                    maxAct = act
                    maxPlays = self.tree.children[act].plays
        return maxAct

def makeLaserChessMCBot(startState):
    bot = MCBot(lc.won,lc.getActions,lc.performAction,startState,100000)
    return bot


#------------------------------------------------
# king1 = (4,4,0,"k","1")
# king2 = (4,5,0,"k","2")
# board = [king1,king2]
# board.sort()
# board = tuple(board)
# state = ("1",board)
# bot1 = makeLaserChessMCBot(state)
# for i in range(5000):
#     bot1.calculate()
# for act in bot1.tree.children:
#     print(act)
#     if bot1.tree.children[act]:
#         print(bot1.tree.children[act].wins)
#         print(bot1.tree.children[act].plays)
#     else:
#         print("NONE")
