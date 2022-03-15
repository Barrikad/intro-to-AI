from copy import deepcopy
from tracemalloc import start
from bot import *
import laserchess as lc
import lc_bot as lcb
import tictactoe as ttt
import reach15 as r15
from frontiers import *

BOT_TICKS = 10000

def playGame(
        bot, botPlayer,
        startState, getActions, performAction,
        statePrinter, moveParser, getPlayer):
    curState = startState
    actions = getActions(curState)
    while actions:
        #let bot calculate
        for i in range(BOT_TICKS):
            bot.calculate()
        # for act in bot.tree.children:
        #     print("--")
        #     print(act)
        #     print(bot.tree.children[act].value)
        #     statePrinter(bot.tree.children[act].state)

        statePrinter(curState)
        if getPlayer(curState) == botPlayer:
            botAction = bot.bestAction()
            curState = performAction(curState,botAction)
        else:
            playerAction = moveParser()
            curState = performAction(curState,playerAction)

        #update bot on new state
        bot.updateState(curState)
        actions = getActions(curState)
    return curState
    
def tictactoeParser():
    c1c2 = input("Input space-separated coordinate: ")
    c1c2 = c1c2.split()
    c1 = int(c1c2[0])
    c2 = int(c1c2[1])
    return (c1,c2)

def reach15Parser():
    c = input("Input the number to add: ")
    return int(c)

def playTictactoe():
    player = ""
    while player != "p1" and player != "p2":
        player = input("Choose player (p1 or p2): ")

    board = []
    for i in range(3):
        board.append([""]*3)
    startState = ttt.State("p1",board)

    bot = ttt.makeTicTacToeBot(ttt.switchPlayer(player),Queue(),startState)

    getPlayer = lambda state : state.player

    print("Board coordinates go from 0 0 to 2 2")
    print("0 0 is top left corner")
    print("In x y, x is horizontal position and y vertical position")
    endState = playGame(
        bot,ttt.switchPlayer(player),startState,ttt.getActions,
        ttt.performAction,ttt.statePrinter,tictactoeParser,getPlayer
    )
    print("Game over")
    print("Final state:")
    ttt.statePrinter(endState)
    won = ttt.won(endState.board) 
    if won:
        print("Congratulations to our winner: " + won)
    else:
        print("Game tied!")

def playReach15():
    player = ""
    while player != "p1" and player != "p2":
        player = input("Choose player (p1 or p2): ")

    startState = ("p1",1)

    bot = r15.makeReach15Bot(r15.switchPlayer(player),Queue())

    getPlayer = lambda state : state[0]

    print("Counter goes from 1 to 15")
    print("Add 1, 2, or 3 to counter in each turn")
    print("The player to get the counter to 15 wins")
    endState = playGame(
        bot,r15.switchPlayer(player),startState,r15.getActions,
        r15.performAction,print,reach15Parser,getPlayer
    )
    print("Game over")
    print("Final state:")
    print(endState)

#OPTIONS
#printMode: "a" for all states, "e" for only end-state, "n" for none
def botBattleLaserchess(printMode = "n"):
    state = lc.startState()
    bot1 = lcb.makeLaserChessBot("1",Queue(),state)
    bot1.calculate()
    bot1.calculate()
    bot2 = lcb.makeLaserChessBot("2",Queue(),state)
    bot2.calculate()
    bot2.calculate()
    for i in range(40):
        for j in range(1000):
            bot1.calculate()
        act = bot1.bestAction()
        print(act)
        state = lc.performAction(state,act)
        bot1.updateState(state)
        bot1.calculate()
        bot1.calculate()
        bot2.updateState(state)
        bot2.calculate()
        bot2.calculate()
        if lc.won(state[1]):
            break

        for j in range(1000):
            bot2.calculate()
        act = bot2.bestAction()
        print(act)
        if act == None:
            print(bot2.tree.state)
        state = lc.performAction(state,act)
        bot1.updateState(state)
        bot1.calculate()
        bot1.calculate()
        bot2.updateState(state)
        bot2.calculate()
        bot2.calculate()
        if lc.won(state[1]):
            break

        if i % 5 == 0:
            print(state)
    print(state)


botBattleLaserchess()