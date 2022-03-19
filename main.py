from copy import deepcopy
import queue
from shutil import move
from threading import Thread
import time
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


class botThread(Thread):
    def __init__(self, threadID, name, inQueue, outQueue, startState, player):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.inQueue = inQueue
        self.outQueue = outQueue
        self.bot = lcb.makeLaserChessBot(player,Heap(lambda s : s[0] == player),startState)

    def run(self):
        while True:
            self.bot.calculate()
            self.bot.calculate()
            self.bot.calculate()
            self.bot.calculate()
            self.bot.calculate()
            if not self.inQueue.empty():
                m = self.inQueue.get()
                if m[0] == "action":
                    self.outQueue.put(self.bot.bestAction(playingLaserChess=True))
                elif m[0] == "update":
                    self.bot.updateState(m[1])
                elif m[0] == "quit":
                    break


#OPTIONS
#printMode: "a" for all states, "e" for only end-state, "n" for none
def botBattleLaserchess(printMode = "n"):
    state = lc.startState()

    b1in = queue.Queue()
    b1out = queue.Queue()
    b2in = queue.Queue()
    b2out = queue.Queue()

    bot1 = botThread(1,"bot1",b1in,b1out,state,"1")
    bot2 = botThread(2,"bot2",b2in,b2out,state,"2")
    bot1.daemon = True
    bot2.daemon = True
    bot1.start()
    bot2.start()
    time.sleep(2)

    lc.printBoard(state)
    for i in range(100):
        time.sleep(4)
        print("ROUND " + str(i+1))
        b1in.put(("action",))
        act = b1out.get()
        print("Player 1 move: ")
        print(act)
        state = lc.performAction(state,act)
        b1in.put(("update",state))
        b2in.put(("update",state))
        if lc.won(state[1]):
            break
        
        lc.printBoard(state)
        time.sleep(4)

        b2in.put(("action",))
        act = b2out.get()
        print("Player 2 move: ")
        print(act)
        state = lc.performAction(state,act)
        b1in.put(("update",state))
        b2in.put(("update",state))
        if lc.won(state[1]):
            break

        lc.printBoard(state)
    print(state)
    b1in.put(("quit",))
    b2in.put(("quit",))
    bot1.join()
    bot2.join()
    print("done")

def playerVsBotLaserChess():
    player = ""
    while player != "p1" and player != "p2":
        player = input("Choose player (p1 or p2): ")
    
    state = lc.startState()

    lc.printBoard(state)
    print("Player has move options of fire(f), move(m), capture(c) and rotate(r)")
    print("")
    if player == "p1":

        b2in = queue.Queue()
        b2out = queue.Queue()

        bot2 = botThread(2,"bot2",b2in,b2out,state,"2")
        bot2.daemon = True
        bot2.start()

        for i in range(100):
            print("ROUND " + str(i+1))

            actions = lc.getActions(state)
            validAction = False
            while validAction != True:
                moveType = ""
                while moveType !="f" and moveType !="m" and moveType !="c" and moveType !="r":
                    moveType = input("Choose move f m c or r: ")
                if moveType == "f":
                    direction = int(input("Choose shot direction: "))
                    act = (moveType, direction)
                elif moveType == "m":
                    piece = input("Choose piece coordinates: ")
                    direction = int(input("Choose rotation direction: "))
                    movedirection = input("Choose move direction: ")
                    act = (moveType, int(piece[0]), int(piece[2]), int(direction), int(movedirection))
                elif moveType == "c":
                    piece = input("Choose piece coordinates: ")
                    direction = int(input("Choose rotation direction: "))
                    movedirection = input("Choose move direction: ")
                    act = (moveType, int(piece[0]), int(piece[2]), int(direction), int(movedirection))
                elif moveType == "r":
                    piece = input("Choose piece coordinates: ")
                    direction = int(input("Choose rotation direction: "))
                    act = (moveType, int(piece[0]), int(piece[2]), int(direction))
                validAction = act in actions 
            print("Player 1 move: ")
            print(act)
            state = lc.performAction(state,act)
            b2in.put(("update",state))
            if lc.won(state[1]):
                break
            
            lc.printBoard(state)
            time.sleep(4)

            b2in.put(("action",))
            act = b2out.get()
            print("Player 2 move: ")
            print(act)
            state = lc.performAction(state,act)
            b2in.put(("update",state))
            if lc.won(state[1]):
                break

            lc.printBoard(state)

    elif player == "p2":
        b1in = queue.Queue()
        b1out = queue.Queue()

        bot1 = botThread(1,"bot1",b1in,b1out,state,"1")
        bot1.daemon = True
        bot1.start()
        time.sleep(2)

        lc.printBoard(state)
        for i in range(100):
            time.sleep(4)
            print("ROUND " + str(i+1))
            b1in.put(("action",))
            act = b1out.get()
            print("Player 1 move: ")
            print(act)
            state = lc.performAction(state,act)
            b1in.put(("update",state))
            if lc.won(state[1]):
                break
            
            lc.printBoard(state)

            actions = lc.getActions(state)
            validAction = False
            while validAction != True:
                moveType = ""
                while moveType !="f" and moveType !="m" and moveType !="c" and moveType !="r":
                    moveType = input("Choose move f m c or r: ")
                if moveType == "f":
                    direction = int(input("Choose shot direction: "))
                    act = (moveType, direction)
                elif moveType == "m":
                    piece = input("Choose piece coordinates: ")
                    direction = int(input("Choose rotation direction: "))
                    movedirection = input("Choose move direction: ")
                    act = (moveType, int(piece[0]), int(piece[2]), int(direction), int(movedirection))
                elif moveType == "c":
                    piece = input("Choose piece coordinates: ")
                    direction = int(input("Choose rotation direction: "))
                    movedirection = input("Choose move direction: ")
                    act = (moveType, int(piece[0]), int(piece[2]), int(direction), int(movedirection))
                elif moveType == "r":
                    piece = input("Choose piece coordinates: ")
                    direction = int(input("Choose rotation direction: "))
                    act = (moveType, int(piece[0]), int(piece[2]), int(direction))
                validAction = act in actions
            print("Player 2 move: ")
            print(act)
            state = lc.performAction(state,act)
            b1in.put(("update",state))
            if lc.won(state[1]):
                break

            lc.printBoard(state)
        print(state)
        if player == "p1":
            b2in.put(("quit",)) 
            bot2.join()
        else:   
            b1in.put(("quit",))
            bot1.join()
        print("done")

def laserChessMain():
    gameMode = ""
    while gameMode != "bvb" and gameMode != "pvb":
        gameMode = input("Choose \"pvb\" for player vs bot or \"bvb\" for bot vs bot: ")
    if gameMode == "bvb":
        botBattleLaserchess()
    elif gameMode == "pvb":
        playerVsBotLaserChess()


#botBattleLaserchess()
#playerVsBotLaserChess()
laserChessMain()