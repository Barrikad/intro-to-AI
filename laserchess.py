#GENERAL NOTES
#I use immutable datatypes, since the states will be used as keys in maps
#Board is 9x9 tiles, unlike chess
#Simplifications compared to https://archive.org/details/1987-06-compute-magazine/page/n27/mode/2up?view=theater:
# just one action per turn, instead of two
# instead, the action performed by one piece can always be preceded by a rotation
# no hypercube, hypersquare, straight mirror
# might replace hypersquare in middle of board with immovable block

#REPRESENTING THE GAME IN PYTHON
#Piece represented by tuple where 
# first value is player owning the piece
# second value is name of piece
# third value is orientation of piece
# fourth value is horizontal coordinate (increases eastwards)
# fifth value is vertical coordinate (increases northwards)
#Name of player is some character ("1" for p1, "2" for p2)
#Name of piece is one of 
# "k":king, "l":laser cannon, "b":block, "s":splitter, "d":diagonal, "t":triangular
#Orientation is one of 
# 0:North, 1:East, 2:South, 3:West
#Coordinates is integer between 0 and 8

#p1's laser cannon at south-east corner pointing east:
#("1","l",1,0,8)

#State represented by tuple where first value is player to make a turn 
#second value is board
#Board is sorted tuple of pieces
#important that it's sorted so that same states are represented in the same way

#p1's turn and there exists just two kings:
#(
#   "1",
#   (
#       ("1","k",3,4,5),
#       ("2","k",1,2,0)
#   )
#)

#An action is a tuple
#First element is either "f"(fire laser), "m"(move piece), or "r" (rotate piece)
#If first element is "f" 
# then second element is an integer representing new orientation of laser (before firing)
#If first element is "m"
# then second and third element is position of chosen piece
# fourth element is new orientation of chosen piece
# fifth element is direction in which piece moves by one
#If first element is "r"
# then second and third element is position of chosen piece
# fourth element is new orientation of chosen piece

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
# can therefore not be destroyed be lasers
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


def mutableState(state):
    mstate = list(state)
    mstate[1] = [
        [
            (None if tile == None else list(tile)) 
            for tile in list(column)
        ] 
        for column in list(mstate[1])]
    return mstate

#potentially destructive of input state
def immutableState(state):
    for i in len(state[1]):
        for j in len(state[1][i]):
            if state[1][i][j] != None:
                state[1][i][j] = tuple(state[1][i][j])
        state[1][i] = tuple(state[1][i])
    return tuple(state)

