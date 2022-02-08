#state = (player,counter): string * int
#action = steps: int
from bot import Agent
from games import UnReachableState

#GAME DEFINITION
def switchPlayer(player):
    if player == "p1":
        return "p2"
    elif player == "p2":
        return "p1"

def getActions(state):
    counter = state[1]
    if counter <= 12:
        actions = [1,2,3]
    elif counter == 13:
        actions = [1,2]
    elif counter == 14:
        actions = [1]
    else:
        actions = []
    return actions

def performAction(state,action):
    if state[1] + action > 15:
        raise UnReachableState("From state:" + str(state) + " action:" + str(action) + " was attempted")
    else:
        return (switchPlayer(state[0]), state[1] + action)

#---------------

#BOT RELATED
def evaluator(state,perspective):
    player, counter = state
    if counter == 15:
        #if it is p2's turn then p1 just made the winning move
        if player == perspective:
            return -100
        else:
            return 100
    else:
        return 0

def makeReach15Bot(botPlayer,frontier):
    startState = ("p1",1)
    ourTurn = lambda state : state[0] == botPlayer
    evaluator_ = lambda state : evaluator(state,botPlayer)
    bot = Agent(evaluator_,getActions,performAction,ourTurn,frontier,startState)
    return bot
#-----------