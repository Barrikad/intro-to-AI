from bot import Agent
from laserchess import getActions, performAction, pieceCoords, pieceOwner, won, nextPlayer, board, pieceName

def eval_piece(piece_name):
        # king
        if piece_name == "k":
            return 0
        # lazor
        elif piece_name == "l":
            return 300
        # splitter
        elif piece_name == "s":
            return 90
        # diagonal mirror
        elif piece_name == "d":
            return 70
        # block
        elif piece_name == "b":
            return 60
        # triangular mirror
        return 40

#TWEAK AREA:
# problem: agents choose rotation way too often
# fix: add points for moving upwards
def evaluator(state, perspective):
    kings = [perspective,nextPlayer(perspective)]

    score = 0

    for piece in board(state):
        pscore = eval_piece(pieceName(piece))
        if pscore == 0:
            kings.remove(pieceOwner(piece))
        else:
            if pieceOwner(piece) == perspective:
                score += pscore
                #hardcoded for standard board:
                if pieceName(piece) == "b":
                    if perspective == "1":
                        score += 14 * pieceCoords(piece)[1]
                    else:
                        score += 14 * (8 - pieceCoords(piece)[1])
            else:
                score -= pscore

    if kings == [perspective]:
        return -10000
    elif kings == [nextPlayer(perspective)]:
        return 10000
    elif kings == [perspective,nextPlayer(perspective)]:
        return 0
    else:
        return score


def makeLaserChessBot(botPlayer, frontier, startState):
    ourTurn = lambda state: state[0] == botPlayer
    evaluator_ = lambda state: evaluator(state, botPlayer)
    bot = Agent(evaluator_, getActions, performAction, ourTurn, frontier, startState)
    return bot
