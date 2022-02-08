from copy import deepcopy

from bot import Agent

#GAME DEFINITION
class State:
    def __init__(self,player,board):
        self.player = player
        self.board = board
    
    def board_id(self):
        b_string = ""
        for i in range(3):
            for j in range(3):
                if self.board[i][j]:
                    b_string += self.board[i][j]
                else:
                    b_string += "  "
        return hash(b_string)
    
    def __eq__(self,other):
        return self.board_id() == other.board_id() and self.player == other.player
    
    def __hash__(self):
        return hash(hash(self.player) + self.board_id())

def won(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2]
    return ""

def switchPlayer(player):
    if player == "p1":
        return "p2"
    elif player == "p2":
        return "p1"

def getActions(state):
    if won(state.board):
        return []
    else:
        actions = []
        for i in range(3):
            for j in range(3):
                if state.board[i][j] == "":
                    actions.append((i,j))
        return actions

def performAction(state,action):
    nboard = deepcopy(state.board)
    nboard[action[0]][action[1]] = state.player
    nstate = State(switchPlayer(state.player),nboard)
    return nstate

#---------------


#BOT RELATED

def evaluator(state,perspective):
    #if it is p2's turn p1 just made the winning move
    pwon = won(state.board)
    if pwon == perspective:
        return 100
    elif pwon:
        return -100
    else:
        return 0

def makeTicTacToeBot(botPlayer,frontier,startState):
    ourTurn = lambda state : state.player == botPlayer
    evaluator_ = lambda state : evaluator(state,botPlayer)
    bot = Agent(evaluator_,getActions,performAction,ourTurn,frontier,startState)
    return bot
#-----------

def printBoard(board):
    print("..........")
    for i in range(3):
        line = "|"
        for j in range(3):
            if board[i][j] == "":
                line += "  |"
            else:
                line += board[i][j] + "|"
        print(line)
    print("..........")

def statePrinter(state):
    print(state.player + ":")
    printBoard(state.board)