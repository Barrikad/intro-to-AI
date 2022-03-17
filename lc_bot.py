from bot import Agent
from laserchess import getActions, performAction, won, nextPlayer

#really bad evaluator
#will only be able to avoid dying in next few turns, at best
def evaluator(state,perspective):
    pwon = won(state[1])
    if pwon == perspective:
        return 1000
    elif pwon == nextPlayer(perspective):
        return 0
    else:
        return 500

def makeLaserChessBot(botPlayer,frontier,startState):
    ourTurn = lambda state : state[0] == botPlayer
    evaluator_ = lambda state : evaluator(state,botPlayer)
    bot = Agent(evaluator_,getActions,performAction,ourTurn,frontier,startState)
    return bot