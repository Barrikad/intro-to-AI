class State:
    def __init__(self,player,counter):
        self.player = player
        self.counter = counter

def evaluator(state):
    if state.counter == 15:
        #if it is p2's turn p1 just made the winning move
        if state.player == "p2":
            return 100
        else:
            return -100
    else:
        return 0

def switchPlayer(player):
    if player == "p1":
        return "p2"
    elif player == "p2":
        return "p1"

def nextStates(state):
    states = []
    for i in range(1,4):
        if state.counter + i <= 15:
            states.append(State(switchPlayer(state.player),state.counter + i))
    return states

def statePrinter(state):
    print(state.player + " " + str(state.counter))