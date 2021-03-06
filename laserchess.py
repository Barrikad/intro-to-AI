#GENERAL NOTES
#I use immutable datatypes, since the states will be used as keys in maps
#I avoid indexing these tuples directly so that representation can be changed
#Board is 9x9 tiles, unlike chess
#Simplifications compared to https://archive.org/details/1987-06-compute-magazine/page/n27/mode/2up?view=theater:
# just one action per turn, instead of two
# instead, the action performed by one piece can always be preceded by a rotation
# no hypercube, hypersquare, straight mirror
# might replace hypersquare in middle of board with immovable block

#REPRESENTING THE GAME IN PYTHON
#Piece represented by tuple where 
# first value is horizontal coordinate (increases eastwards)
# second value is vertical coordinate (increases northwards)
# third value is orientation of piece
# fourth value is name of piece
# fifth value is player owning the piece
#Name of player is some character ("1" for p1, "2" for p2)
#Name of piece is one of 
# "k":king, 
# "l":laser cannon, 
# "b":block, 
# "s":splitter, 
# "d":diagonal, 
# "t":triangular
#Orientation is one of 
# 0:North, 1:East, 2:South, 3:West
#Coordinates is integer between 0 and 8

#p1's laser cannon at south-east corner pointing east:
#(0,8,1,"l","1")

#State represented by tuple where first value is player to make a turn 
#second value is board
#Board is sorted tuple of pieces
#important that it's sorted so that same states are represented in the same way

#p1's turn and there exists just two kings:
#(
#   "1",
#   (
#       (4,5,3,"k","1"),
#       (2,0,1,"k","2")
#   )
#)

#An action is a tuple
#First element is either "f"(fire laser), "m"(move piece), "c"(capture piece), or "r" (rotate piece)
#If first element is "f" 
# then second element is an integer representing new orientation of laser (before firing)
#If first element is "m"
# then second and third element is position of chosen piece
# fourth element is new orientation of chosen piece
# fifth element is direction in which piece moves by one
#If first element is "c"
# same as "m"
#If first element is "r"
# then second and third element is position of chosen piece
# fourth element is new orientation of chosen piece

# (4 * 81 * 4 * 80) + (4 * 81 * 4 * 80 * 4 * 79)
#move piece at 3,4 to 3,5 and change orientation to south:
#("m",3,4,2,0)

#BEHAVIOUR OF PIECES
#All pieces can rotate to any orientation as part of their move
#All pieces can move 1 position either horizontally or vertically
#A valid move is one where either orientation or position (or both) is changed
#Only king and block can move into a position occupied by another piece, 
# the other piece will then be captured
#Laser cannon can fire a laser in the direction it is pointing (after rotation)
# it is vulnerable from all directions
# the laser can destroy pieces belonging to any player (and also itself)
#King can capture opponents pieces by moving onto them
# it is vulnerable from all directions
# if it dies the player owning it loses the game
#block can capture opponents pieces by moving onto them
# if it is hit by laser from direction it is pointing then laser is reflected 
# if hit by laser form any other side it is destroyed
#splitter cannot capture
# if hit by laser from front, then the laser splits into two beams going left and right
# if hit from left or right it redirects laser in direction it is pointing
# if hit from back the splitter is destroyed
#diagonal mirror cannot capture
# if hit from front, redirects to the right and vice versa
# if hit from back, redirects to the left and vice versa
# can therefore not be destroyed by lasers
#triangular mirror cannot capture
# if hit from front redirects to the right and vice versa
# destroyed if hit from back or left 

#Every piece destroyed by laser is destroyed at end of turn
#So if triangular mirror is hit from front and back it will both reflect and get destroyed

#START POSITION
#each side has the below setup as seen from their POV (i.e. the sides are not mirrored as in chess)
#the pieces are represented by a letter and a number, 
# where the letter is the name of the piece as defined above
# and the number is its orientation as defined above
#
# t3 b0 b0 b0 b0 s2 b0 b0 t0
# t0 t0 d3 b0 k0 l0 t0 d3 d3

from util import binarySearch


#Some abbreviations for more readable code
#Change these if representation changes
#PIECE
def pieceCoords(piece):
    return (piece[0],piece[1])

def pieceOrient(piece):
    return piece[2]

def pieceName(piece):
    return piece[3]

def pieceOwner(piece):
    return piece[4]

def movePiece(piece,coords):
    return (coords[0],coords[1],piece[2],piece[3],piece[4])

def rotatePiece(piece,orient):
    return (piece[0],piece[1],orient,piece[3],piece[4])

def mrPiece(piece,coords,orient):
    return (coords[0],coords[1],orient,piece[3],piece[4])

def outOfBounds(coords):
    if coords[0] < 0 or coords[1] < 0 or coords[0] > 8 or coords[1] > 8:
        return True
    else:
        return False

#STATE
def curPlayer(state):
    return state[0]

def board(state):
    return state[1]

#ACTION
def actionName(action):
    return action[0]

def actionOrient(action):
    if actionName(action) == "f":
        return action[1]
    else:
        return action[3]
    
def actionCoords(action):
    if actionName(action) == "f":
        return None
    else:
        return (action[1],action[2])

def actionMove(action):
    if actionName(action) == "m" or actionName(action) == "c":
        return action[4]
    else:
        return None

#Return next player
#Defines the number of players
def nextPlayer(player):
    if player == "1":
        return "2"
    else:
        return "1"

#Searches for piece at the given coordinates
#Returns name and owner of piece and index in board tuple if present
#Returns None otherwise
def tryFindPiece(board,coords):
    sup = binarySearch(board,coords,"sup")
    if sup != None and pieceCoords(sup[0]) == coords:
        return sup
    else:
        return None

#Searches for laser belonging to a given player
#Returns coords and orientation and index in board tuple if present
#Returns None otherwise
def tryFindLaser(board,player):
    for i in range(len(board)):
        piece = board[i]
        if pieceName(piece) == "l" and pieceOwner(piece) == player:
            return (piece,i)
    return None

#Coordinate addition
def addCoords(xy1,xy2):
    return (xy1[0] + xy2[0],xy1[1] + xy2[1])

#translates orientation integer to direction vector
def dirVector(orient):
    return [(0,1),(1,0),(0,-1),(-1,0)][orient]

def hitResult(piece,beamOrient):
    #defines which side the piece is hit from
    #0=back, 1=left, 2=front, 3=right
    #there is probably an easier way to calculate this
    if pieceOrient(piece) == beamOrient:
        hitSide = 0
    elif (pieceOrient(piece) + 1) % 4 == beamOrient:
        hitSide = 1
    elif abs(pieceOrient(piece)-beamOrient) == 2:
        hitSide = 2
    elif (pieceOrient(piece) + 3) % 4 == beamOrient:
        hitSide = 3

    if pieceName(piece) == "k" or pieceName(piece) == "l":
        #king and laser are always captured by laser
        return ("c",)
    elif pieceName(piece) == "b":
        #is block and laser are pointing in opposite direction?
        if hitSide == 2:
            return ("r",pieceOrient(piece))
        else:
            return ("c",)
    elif pieceName(piece) == "s":
        if hitSide == 1 or hitSide == 3:
            return ("r",pieceOrient(piece))
        elif hitSide == 2:
            return ("s",(pieceOrient(piece) + 1) % 4, (pieceOrient(piece) - 1) % 4)
        else:
            return ("c",)
    elif pieceName(piece) == "d":
        if hitSide == 0 or hitSide == 2:
            return ("r",(beamOrient - 1) % 4)
        elif hitSide == 1 or hitSide == 3:
            return ("r",(beamOrient + 1) % 4)
    elif pieceName(piece) == "t":
        if hitSide == 2:
            return ("r",(beamOrient - 1) % 4)
        elif hitSide == 3:
            return ("r",(beamOrient + 1) % 4)
        else:
            return ("c",)

def beamHits(board,origin,orient):
    visited = []
    hits = []
    toVisit = [(origin,orient)]
    while toVisit != []:
        orig,ornt = toVisit.pop()
        visited.append((orig,ornt))
        newPosition = addCoords(orig,dirVector(ornt))

        if outOfBounds(newPosition) or ((newPosition,ornt) in visited):
            continue
        
        hit = tryFindPiece(board,newPosition)
        if hit == None:
            toVisit.append((newPosition,ornt))
        else:
            hr = hitResult(hit[0],ornt)
            if hr[0] == "c":
                hits.append(hit)
            elif hr[0] == "r":
                toVisit.append((newPosition,hr[1]))
            elif hr[0] == "s":
                toVisit.append((newPosition,hr[1]))
                toVisit.append((newPosition,hr[2]))
        
    return hits

def beamVisits(state,action):
    if action[0] != "f":
        return []
    mutBoard = list(board(state))

    laser, lindex = tryFindLaser(board(state),curPlayer(state))
    lorient = actionOrient(action)
    
    #rotate laser 
    mutBoard[lindex] = rotatePiece(mutBoard[lindex],lorient)
    
    board = mutBoard
    origin = pieceCoords(laser)
    orient = lorient

    visited = []
    hits = []
    toVisit = [(origin,orient)]
    while toVisit != []:
        orig,ornt = toVisit.pop()
        visited.append((orig[0],orig[1],ornt))
        newPosition = addCoords(orig,dirVector(ornt))

        if outOfBounds(newPosition) or ((newPosition[0],newPosition[1],ornt) in visited):
            continue
        
        hit = tryFindPiece(board,newPosition)
        if hit == None:
            toVisit.append((newPosition,ornt))
        else:
            hr = hitResult(hit[0],ornt)
            if hr[0] == "c":
                hits.append(hit)
            elif hr[0] == "r":
                toVisit.append((newPosition,hr[1]))
            elif hr[0] == "s":
                toVisit.append((newPosition,hr[1]))
                toVisit.append((newPosition,hr[2]))
        
    return visited


#Assumes that the action is valid
#Checks for this should be made before calling the function
def performAction(state,action):
    mutBoard = list(board(state))

    if actionName(action) == "f":
        #find position, index and new orientation of laser
        laser, lindex = tryFindLaser(board(state),curPlayer(state))
        lorient = actionOrient(action)
        
        #rotate laser 
        mutBoard[lindex] = rotatePiece(mutBoard[lindex],lorient)

        #calculate hit pieces and remove from board
        bh = beamHits(mutBoard,pieceCoords(laser),lorient)
        for p,_ in bh:
            try:
                mutBoard.remove(p)
            except ValueError:
                pass
    elif actionName(action) == "m" or actionName(action) == "c":
        #find piece
        piece, pindex = tryFindPiece(board(state),actionCoords(action))
        #new coordinates
        newCoords = addCoords(actionCoords(action),dirVector(actionMove(action)))
        #mark piece for capture
        if actionName(action) == "c":
            _,cindex = tryFindPiece(board(state),newCoords)
        #move and rotate piece
        mutBoard[pindex] = mrPiece(piece,newCoords,actionOrient(action))
        #capture marked piece
        if actionName(action) == "c":
            mutBoard.pop(cindex)
    elif actionName(action) == "r":
        #find piece
        piece,pindex = tryFindPiece(board(state),actionCoords(action))
        #rotate piece
        mutBoard[pindex] = rotatePiece(piece,actionOrient(action))
    mutBoard.sort()
    return (nextPlayer(curPlayer(state)),tuple(mutBoard))

def getActions(state):
    kings = 0
    actions = []
    for i in range(len(board(state))):
        piece = board(state)[i]
        #register king if king
        if pieceName(piece) == "k":
            kings += 1

        #skip if opponents piece
        if pieceOwner(piece) != curPlayer(state):
            continue

        #fire laser if laser
        if pieceName(piece) == "l":
            for r in range(4):
                actions.append(("f",r))
        
        #calculate types of moves 
        moved = addCoords(pieceCoords(piece),(0,1))
        if (i < len(board(state)) - 1 and 
                pieceCoords(board(state)[i + 1]) == moved and
                pieceOwner(board(state)[i + 1]) != curPlayer(state)):
            north = "c"
        elif (moved[1] <= 8 and (
                i >= len(board(state)) - 1 or
                pieceCoords(board(state)[i + 1]) != moved)):
            north = "m"
        else:
            north = "x"
        moved = addCoords(pieceCoords(piece),(1,0))
        hit = tryFindPiece(board(state),moved)
        if hit != None and pieceOwner(hit[0]) != curPlayer(state):
            east = "c"
        elif moved[0] <= 8 and hit == None:
            east = "m"
        else:
            east = "x"
        moved = addCoords(pieceCoords(piece),(0,-1))
        if (i > 1 and pieceCoords(board(state)[i - 1]) == moved and
                pieceOwner(board(state)[i - 1]) != curPlayer(state)):
            south = "c"
        elif (moved[1] >= 0 and (
                i <= 0 or
                pieceCoords(board(state)[i - 1]) != moved)):
            south = "m"
        else:
            south = "x"
        moved = addCoords(pieceCoords(piece),(-1,0))
        hit = tryFindPiece(board(state),moved)
        if hit != None and pieceOwner(hit[0]) != curPlayer(state):
            west = "c"
        elif moved[0] >= 0 and hit == None:
            west = "m"
        else:
            west = "x"
        
        #add moves
        moves = [north,east,south,west]
        for m in range(4):
            for r in range(4):
                if moves[m] == "m":
                    actions.append(
                        ("m",pieceCoords(piece)[0],pieceCoords(piece)[1],r,m))
                if moves[m] == "c" and pieceName(piece) in ["k","b"]:
                    actions.append(
                        ("c",pieceCoords(piece)[0],pieceCoords(piece)[1],r,m))
        
        #add rotations
        for r in range(4):
            if r != pieceOrient(piece):
                actions.append(
                    ("r",pieceCoords(piece)[0],pieceCoords(piece)[1],r))

    #return actions if not endstate
    if kings != 2:
        return []
    return actions


#hardcoded for "1" and "2"
def won(board):
    players = ["1","2"]
    for piece in board:
        if pieceName(piece) == "k":
            players.remove(pieceOwner(piece))
    if players == []:
        return ""
    elif players == ["1","2"]:
        return "tie"
    else:
        return nextPlayer(players[0])

def startState():
    p1_board = [
        (0,0,0,"t","1"),
        (1,0,0,"t","1"),
        (2,0,3,"d","1"),
        (3,0,0,"b","1"),
        (4,0,0,"k","1"),
        (5,0,0,"l","1"),
        (6,0,0,"t","1"),
        (7,0,3,"d","1"),
        (8,0,3,"d","1"),
        (0,1,3,"t","1"),
        (1,1,0,"b","1"),
        (2,1,0,"b","1"),
        (3,1,0,"b","1"),
        (4,1,0,"b","1"),
        (5,1,2,"s","1"),
        (6,1,0,"b","1"),
        (7,1,0,"b","1"),
        (8,1,0,"t","1"),
    ]

    p2_board = []
    for piece in p1_board:
        newOrient = (pieceOrient(piece) + 2) % 4
        newX = 8 - pieceCoords(piece)[0]
        newY = 8 - pieceCoords(piece)[1]
        p2_board.append((newX,newY,newOrient,pieceName(piece),"2"))

    board = p1_board + p2_board
    board.sort()
    return ("1",tuple(board))


def printBoard(state):
    p1TextFormat = "\033[1;31;40m"
    board = state[1]
    A = [["  ","  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  ","  "]]
    for i in board:
        # 0:North, 1:East, 2:South, 3:West
        if i[2] == 0:
            if i[4] == "1":
                A[i[1]][i[0]] = p1TextFormat + i[3] + "N" + "\033[1;37;40m"   
            else: 
                A[i[1]][i[0]] = i[3] + "N"
        elif i[2] == 1:
            if i[4] == "1":
                A[i[1]][i[0]] = p1TextFormat + i[3] + "E" + "\033[1;37;40m"   
            else: 
                A[i[1]][i[0]] = i[3] + "E"
        elif i[2] == 2:
            if i[4] == "1":
                A[i[1]][i[0]] = p1TextFormat + i[3] + "S" + "\033[1;37;40m"   
            else: 
                A[i[1]][i[0]] = i[3] + "S"
        elif i[2] == 3:
            if i[4] == "1":
                A[i[1]][i[0]] = p1TextFormat + i[3] + "W" + "\033[1;37;40m"   
            else: 
                A[i[1]][i[0]] = i[3] + "W"
        
    print(
        " -- -- -- -- -- -- -- -- -- \n"+
        "|"+A[8][0] +"|"+A[8][1] +"|"+A[8][2] +"|"+A[8][3] +"|"+A[8][4] +"|"+A[8][5] +"|"+A[8][6] +"|"+A[8][7] +"|"+A[8][8] +"|\n"+
        " -- -- -- -- -- -- -- -- -- \n"+   
         "|"+A[7][0] +"|"+A[7][1] +"|"+A[7][2] +"|"+A[7][3] +"|"+A[7][4] +"|"+A[7][5] +"|"+A[7][6] +"|"+A[7][7] +"|"+A[7][8] +"|\n"+
        " -- -- -- -- -- -- -- -- -- \n"+
         "|"+A[6][0] +"|"+A[6][1] +"|"+A[6][2] +"|"+A[6][3] +"|"+A[6][4] +"|"+A[6][5] +"|"+A[6][6] +"|"+A[6][7] +"|"+A[6][8] +"|\n"+
        " -- -- -- -- -- -- -- -- -- \n"+
        "|"+A[5][0] +"|"+A[5][1] +"|"+A[5][2] +"|"+A[5][3] +"|"+A[5][4] +"|"+A[5][5] +"|"+A[5][6] +"|"+A[5][7] +"|"+A[5][8] +"|\n"+
        " -- -- -- -- -- -- -- -- -- \n"+
        "|"+A[4][0] +"|"+A[4][1] +"|"+A[4][2] +"|"+A[4][3] +"|"+A[4][4] +"|"+A[4][5] +"|"+A[4][6] +"|"+A[4][7] +"|"+A[4][8] +"|\n"+
        " -- -- -- -- -- -- -- -- -- \n"+
        "|"+A[3][0] +"|"+A[3][1] +"|"+A[3][2] +"|"+A[3][3] +"|"+A[3][4] +"|"+A[3][5] +"|"+A[3][6] +"|"+A[3][7] +"|"+A[3][8] +"|\n"+
        " -- -- -- -- -- -- -- -- -- \n"+
        "|"+A[2][0] +"|"+A[2][1] +"|"+A[2][2] +"|"+A[2][3] +"|"+A[2][4] +"|"+A[2][5] +"|"+A[2][6] +"|"+A[2][7] +"|"+A[2][8] +"|\n"+
        " -- -- -- -- -- -- -- -- -- \n"+
        "|"+A[1][0] +"|"+A[1][1] +"|"+A[1][2] +"|"+A[1][3] +"|"+A[1][4] +"|"+A[1][5] +"|"+A[1][6] +"|"+A[1][7] +"|"+A[1][8] +"|\n"+
        " -- -- -- -- -- -- -- -- -- \n"+
        "|"+A[0][0] +"|"+A[0][1] +"|"+A[0][2] +"|"+A[0][3] +"|"+A[0][4] +"|"+A[0][5] +"|"+A[0][6] +"|"+A[0][7] +"|"+A[0][8] +"|\n"+
        " -- -- -- -- -- -- -- -- -- \n"
        )