from bot import Agent
from laserchess import getActions, performAction, pieceOwner, won, nextPlayer, board, pieceName

# still a really bad evaluator
# will only be able to avoid dying in next few turns, at best
def evaluator(state, perspective):

    pwon = won(state[1])

    if pwon == perspective:
        return 1000
    elif pwon == nextPlayer(perspective):
        return -1000

    scores = {perspective: 0, nextPlayer(perspective): 0}

    def eval_piece(piece_name):
        # king
        if piece_name == "k":
            return 0
        # lazor
        elif piece_name == "l":
            return 100
        # splitter
        elif piece_name == "s":
            return 70
        # diagonal mirror
        elif piece_name == "d":
            return 60
        # block
        elif piece_name == "b":
            return 40
        # triangular mirror
        return 30

    for owner, piece in [(pieceOwner(piece), pieceName(piece)) for piece in board(state)]:
        scores[owner] = scores[owner] + eval_piece(piece)

    return scores[perspective] - scores[nextPlayer(perspective)]


def makeLaserChessBot(botPlayer, frontier, startState):
    ourTurn = lambda state: state[0] == botPlayer
    evaluator_ = lambda state: evaluator(state, botPlayer)
    bot = Agent(evaluator_, getActions, performAction, ourTurn, frontier, startState)
    return bot
