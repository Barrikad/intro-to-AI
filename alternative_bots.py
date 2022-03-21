from cmath import log, sqrt
import bot 
import frontiers

#heap with lower punishment for steps
class Heap2(frontiers.Heap):
    def evaluate(self, node):
        iv = super().evaluate(node)
        iv += 1000 * node.steps
        return iv

class MCNode:
    def __init__(self,state,children,parents):
        self.state = state
        self.children = children
        self.parents = parents
        self.plays = 0
        self.wins = 0

#monte carlo frontier
class MCHeap(frontiers.Heap):
    def evaluate(self, node):
        ucb = 0
        winRatio = node.wins / node.plays
        #calculate average UCB based on the different parents
        for parent in node.parents:
            exploration = sqrt(2 * log(parent.plays) / node.plays)
            ucb += winRatio + exploration
        ucb /= len(node.parents)
        return ucb

#monte carlo bot
class MCBot():
    def __init__(
            self,
            won,getActions,simulator,ourTurn,
            startState,
            rolloutLimit):
        self.ourTurn = ourTurn
        self.getActions = getActions #fun: state -> action list
        self.simulator = simulator #fun: state -> action -> state
        self.won = won #won should give None if nonterminal, 0 for loss, 0.5 for tie, and 1 for win
        self.frontier = MCHeap(ourTurn) #this has to be MCHeap for the algorithm to work
        self.rolloutLimit = rolloutLimit
        
        self.tree = MCNode(startState,{},[])
        self.stateMap = {startState : self.tree}
        self.frontier.insert(self.tree)
    
    def rollout(self,node):
        for _ in range(self.rolloutLimit):
            w = self.won(node.state)
            if w:
                pass
