from copy import deepcopy
from bot import *
import tictactoe as ttt
import reach15 as r15

def tictactoeStart():
    startBoard = []
    for i in range(3):
        startBoard.append([""]*3)  

    return ttt.State("p1",startBoard)

def tictactoeTrace(startState,aiPlayer):
    trace = obtainTrace(
        evaluator=ttt.evaluator,
        nextStates=ttt.nextStates,
        player=aiPlayer,
        state=startState)
    return trace

def reach15Start():
    return r15.State("p1",1)

def reach15Trace(startState,aiPlayer):
    trace = obtainTrace(
        evaluator=r15.evaluator,
        player=aiPlayer,
        nextStates=r15.nextStates,
        state=startState)
    return trace

def playGame(aiplayer,start,trace,statePrinter,moveParser,switchPlayer):
    curTrace = trace(start(),aiplayer)
    while curTrace.traceMap:
        statePrinter(curTrace.state)
        if curTrace.state.player == aiplayer:
            curTrace = next(iter(curTrace.traceMap.values()))
        else:
            nstate = moveParser(curTrace.state,switchPlayer)
            try:
                curTrace = curTrace.traceMap[nstate]
            except KeyError:
                # for stt in curTrace.traceMap.keys():
                #     print("-----.....------")
                #     ttt.statePrinter(stt)
                #     print("-----.....------")
                print("Move doesn't result in a valid state!")
                print("Try again")
    return curTrace.state
    
def tictactoeParser(state,switchPlayer):
    c1c2 = input("Input space-separated coordinate: ")
    c1c2 = c1c2.split()
    c1 = int(c1c2[0])
    c2 = int(c1c2[1])
    nstate = deepcopy(state)
    nstate.board[c2][c1] = nstate.player
    nstate.player = switchPlayer(nstate.player)
    # print("-----!!!!!------")
    # ttt.statePrinter(nstate)
    # print("-----!!!!!------")
    return nstate


def playTictactoe():
    player = ""
    while player != "p1" and player != "p2":
        player = input("Choose player (p1 or p2): ")
    print("Board coordinates go from 0 0 to 2 2")
    print("0 0 is top left corner")
    print("In x y, x is horizontal position and y vertical position")
    endState = playGame(
        ttt.switchPlayer(player),
        tictactoeStart,
        tictactoeTrace,
        ttt.statePrinter,
        tictactoeParser,
        ttt.switchPlayer)
    print("Game over")
    print("Final state:")
    ttt.statePrinter(endState)
    won = ttt.won(endState.board) 
    if won:
        print("Congratulations to our winner: " + won)
    else:
        print("Game tied!")

playTictactoe()    