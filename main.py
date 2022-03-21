import queue
from subprocess import BELOW_NORMAL_PRIORITY_CLASS
from threading import Thread
import time
from bot import *
import laserchess as lc
import lc_bot as lcb
from frontiers import *
import alternative_bots as ab
import matplotlib.pyplot as plt
import numpy as np

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

class botThread(Thread):
    def __init__(self, threadID, name, inQueue, outQueue, startState, player, botType = "minimax"):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.inQueue = inQueue
        self.outQueue = outQueue
        if botType == "minimax":
            self.bot = lcb.makeLaserChessBot(player,Heap(lambda s : s[0] == player),startState)
        elif botType == "montecarlo":
            self.bot = ab.makeLaserChessMCBot(startState)

    def run(self):
        while True:
            self.bot.calculate()
            if not self.inQueue.empty():
                m = self.inQueue.get()
                if m[0] == "action":
                    self.outQueue.put(self.bot.bestAction(playingLaserChess=True))
                elif m[0] == "update":
                    self.bot.updateState(m[1])
                elif m[0] == "quit":
                    break

def display(fig, ax, pieces, beams, time):
    board = np.zeros((9,9,3))
    board += 0.5 
    board[::2, ::2] = 1 
    board[1::2, 1::2] = 1 

    ax.imshow(board, interpolation='nearest')

    extent = np.array([-0.4, 0.4, -0.4, 0.4]) 
    for p in pieces:
        ax.imshow(np.rot90(plt.imread('graphics/' + p[3] + p[4] + '.png'), -p[2]), extent=extent + [p[0], p[0], p[1], p[1]])

    for b in beams:
        ax.imshow(np.rot90(plt.imread('graphics/laser_beam.png'), b[2]), extent=extent + [b[0], b[0], b[1], b[1]])

    ax.set(xticks=[], yticks=[])
    ax.axis('image')
    plt.pause(time)
    ax.clear()

def botBattleLaserchess(pyPlot = False,monteCarlo = False):
    state = lc.startState()

    b1in = queue.Queue()
    b1out = queue.Queue()
    b2in = queue.Queue()
    b2out = queue.Queue()

    if monteCarlo:
        bot1 = botThread(1,"bot1",b1in,b1out,state,"1",botType="montecarlo")
    else:
        bot1 = botThread(1,"bot1",b1in,b1out,state,"1")
    bot2 = botThread(2,"bot2",b2in,b2out,state,"2")
    bot1.daemon = True
    bot2.daemon = True
    bot1.start()
    bot2.start()

    if pyPlot:
        fig, ax = plt.subplots()
        display(fig, ax, state[1], [], 0.5)

    time.sleep(2)

    #lc.printBoard(state)
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
        
        if pyPlot:
            beam = lc.beamVisits(state,act)
            display(fig,ax,state[1],beam,2)
        else:
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

        if pyPlot:
            beam = lc.beamVisits(state,act)
            display(fig,ax,state[1],beam,2)
        else:
            lc.printBoard(state)
        time.sleep(4)
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
    print("Player has move options of fire(f), move(m), capture(c) and rotate(r).")
    print("The coordinates of the board goes from 0 to 8 in each direction. \nThey should be input like \"0 1\" The first being the column and the second being the row.")
    print("The directions options are North(0), East(1), South(2) and West(3).")
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
            #time.sleep(4)

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
            #time.sleep(4)
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
        pyplot = input("Do you want pyplot visualization? [y/N] ")
        montecarlo = input("Do you want bot1 to be monte carlo? [y/N] ")
        if pyplot[0].lower() == "y":
            pyplot = True
        else:
            pyplot = False
        if montecarlo[0].lower() == "y":
            montecarlo = True
        else:
            montecarlo = False
        botBattleLaserchess(pyPlot=pyplot,monteCarlo=montecarlo)
            
    elif gameMode == "pvb":
        playerVsBotLaserChess()


laserChessMain()
