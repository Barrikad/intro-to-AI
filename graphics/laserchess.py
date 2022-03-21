import matplotlib.pyplot as plt
import numpy as np
from time import sleep
import json

pieces_tuple = (
       (0,0,0,'t','1'),
       (1,0,0,'t','1'),
       (2,0,3,'d','1'),
       (3,0,0,'b','1'),
       (4,0,0,'k','1'),
       (5,0,0,'l','1'),
       (6,0,0,'d','1'),
       (7,0,3,'t','1'),
       (8,0,3,'t','1'),
       (0,1,3,'t','1'),
       (1,1,0,'b','1'),
       (2,1,0,'b','1'),
       (3,1,0,'b','1'),
       (4,1,0,'b','1'),
       (5,1,2,'s','1'),
       (6,1,0,'b','1'),
       (7,1,0,'b','1'),
       (8,1,0,'t','1'),

       (0,8,1,'t','2'),
       (1,8,1,'t','2'),
       (2,8,0,'d','2'),
       (3,8,2,'l','2'),
       (4,8,2,'k','2'),
       (5,8,2,'b','2'),
       (6,8,3,'d','2'),
       (7,8,2,'t','2'),
       (8,8,2,'t','2'),
       (0,7,2,'t','2'),
       (1,7,2,'b','2'),
       (2,7,2,'b','2'),
       (3,7,0,'s','2'),
       (4,7,2,'b','2'),
       (5,7,2,'b','2'),
       (6,7,2,'b','2'),
       (7,7,2,'b','2'),
       (8,7,1,'t','2'),
)

pieces = [list(p) for p in pieces_tuple]
dead_list = []
beams = [] #If beams are not needed this may cancel

#Visualization Function is below decrease time variable to make it faster
#If fire action is a loop or recursive, by adding each beam to beams make them visual
#Add display function at end of each loop or recursive in the fire action to make it work
fig, ax = plt.subplots()

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

def ok2fire(player, pieces):
    for p in pieces:
        if p[3] == 'l' and p[4] == player:
            return True
    return False

def move_location(x,y,direction):
    if direction == 0:
        y += 1
    if direction == 1:
        x += 1
    if direction == 2:
        y += -1
    if direction == 3:
        x += -1
    return x, y

def owner_from_location(player, x, y, pieces):
    for p in pieces:
        if p[0] == x and p[1] == y and p[4] == player:
            return True
    return False
    
def is_free(x, y, pieces):
    for p in pieces:
        if p[0] == x and p[1] == y:
            return False 
    return True
    
def in_boundaries(x ,y):
    if (0 <= x <= 8) and (0 <= y <= 8):
        return True
    return False

def ok2move(player, act, pieces):
    if owner_from_location(player, act[1], act[2], pieces):
        target_x, target_y = move_location(act[1], act[2], act[4])
        if is_free(target_x, target_y, pieces):
            if in_boundaries(target_x, target_y):
                return True
            else:
                print("Target location is not in the chess board")
                return False
        else:
            print("Target location is not free")
            return False
    else:
        print("Player doesn't have a or the piece in given location")
        return False
    
def move(x, y, d, target_x, target_y, pieces):
    for i in range(len(pieces)):
        if pieces[i][0] == x and pieces[i][1] == y:
            pieces[i][0] = target_x
            pieces[i][1] = target_y
            pieces[i][2] = d
            return

def piece_type(x, y, pieces):
    for p in pieces:
        if p[0] == x and p[1] == y:
            return p[3]
    print("Error piece type couldn't found no piece in that location")
    return
    
def is_enemy(player, x, y, pieces):
    for p in pieces:
        if p[0] == x and p[1] == y and p[4] != player:
            return True
    return False

def ok2capture(player, act, pieces):
    if owner_from_location(player, act[1], act[2], pieces):
        piecetype = piece_type(act[1], act[2], pieces) 
        if piecetype == 'k' or piecetype == 'b':
            target_x, target_y = move_location(act[1], act[2], act[4])
            if is_enemy(player, target_x, target_y, pieces):
                if in_boundaries(target_x, target_y):
                    return True
                else:
                    print("Target location is not on the chess board")
                    return False
            else:
                print("Target location is not enemy")
                return False
        else:
            print("This piece cannot capture other pieces")
            return False
    else:
        print("Player doesn't have a or the piece in given location")
        return False

def capture(act, pieces, dead_list):
    target_x, target_y = move_location(act[1], act[2], act[4])
    for p in pieces:
        if p[0] == target_x and p[1] == target_y:
            dead_list.append(p)
            break
    move(act[1], act[2], act[3], target_x, target_y, pieces)
 
def getpiece(x, y, pieces):
    for p in pieces:
        if p[0] == x and p[1] == y:
            return p

def ok2rotate(player, act, pieces):
    if owner_from_location(player, act[1], act[2], pieces):
        orient = getpiece(act[1], act[2], pieces)[2]
        if orient != act[3]:
            return True
        else:
            print("Piece is already in that orientation")
            return False
    else:
        print("Player doesn't have a or the piece in given location")
        return False

def rotate(x, y, d, pieces):
    for i in range(len(pieces)):
        if pieces[i][0] == x and pieces[i][1] == y:
            pieces[i][2] = d
            return

def findlaser(player,pieces):
    for p in pieces:
        if p[3] == 'l' and p[4] == player:
            return p[0], p[1] 

def reverse_dir(direction):
    if direction == 0:
        return 2
    elif direction == 2:
        return 0
    elif direction == 1:
        return 3
    elif direction == 3:
        return 1

def hitside(hitdirect, orient):
    return (hitdirect - orient) % 4

def fire(laser_x, laser_y, d, pieces, dead_list, beams):
    beam_direction = d
    next_x, next_y = move_location(laser_x, laser_y, beam_direction)
    while True:
        if not in_boundaries(next_x, next_y):
            break
        if is_free(next_x, next_y, pieces):
            beams.append([next_x, next_y, beam_direction])   
            next_x, next_y = move_location(next_x, next_y, beam_direction)
        else:
            piece = getpiece(next_x, next_y, pieces)
            hit_direction = reverse_dir(beam_direction)
            hit_side = hitside(hit_direction, piece[2])
            if piece[3] == 't':
                if hit_side == 2 or hit_side == 3:
                    dead_list.append(piece)
                    break
                elif hit_side == 0:
                    beam_direction = (beam_direction - 1) % 4
                    next_x, next_y = move_location(piece[0], piece[1], beam_direction)
                elif hit_side == 1:
                    beam_direction = (beam_direction + 1) % 4
                    next_x, next_y = move_location(piece[0], piece[1], beam_direction)
            elif piece[3] == 'd':
                if hit_side == 0:
                    beam_direction = (beam_direction - 1) % 4
                    next_x, next_y = move_location(piece[0], piece[1], beam_direction)
                elif hit_side == 1:
                    beam_direction = (beam_direction + 1) % 4
                    next_x, next_y = move_location(piece[0], piece[1], beam_direction)
                elif hit_side == 2:
                    beam_direction = (beam_direction - 1) % 4
                    next_x, next_y = move_location(piece[0], piece[1], beam_direction)
                elif hit_side == 3:
                    beam_direction = (beam_direction + 1) % 4
                    next_x, next_y = move_location(piece[0], piece[1], beam_direction)
            elif piece[3] == 'b':
                if hit_side == 0:
                    beam_direction = reverse_dir(beam_direction)
                    next_x, next_y = move_location(piece[0], piece[1], beam_direction)
                else:
                    dead_list.append(piece)
                    break
            elif piece[3] == 'k' or piece[3] == 'l':
                dead_list.append(piece)
                break
            elif piece[3] == 's':
                if hit_side == 2:
                    dead_list.append(piece)
                    break
                elif hit_side == 1:
                    beam_direction = (beam_direction + 1) % 4
                    next_x, next_y = move_location(piece[0], piece[1], beam_direction)
                elif hit_side == 3:
                    beam_direction = (beam_direction - 1) % 4
                    next_x, next_y = move_location(piece[0], piece[1], beam_direction)
                elif hit_side == 0:
                    beam_direction1 = (beam_direction - 1) % 4
                    beam_direction2 = (beam_direction + 1) % 4
                    fire(piece[0], piece[1], beam_direction1, pieces, dead_list, beams)
                    fire(piece[0], piece[1], beam_direction2, pieces, dead_list, beams)
                    break
        display(fig, ax, pieces, beams, 0.01)

def action(player, act, pieces, dead_list, beams):
    if act[0] == 'f':
        if ok2fire(player, pieces):
            laser_x, laser_y = findlaser(player, pieces)
            rotate(laser_x, laser_y, act[1], pieces)
            fire(laser_x, laser_y, act[1], pieces, dead_list, beams)
            return True
        else:
            print("Player unable to fire, player doesn't have laser.")
            print("Try another action!")
            return False
    elif act[0] == 'm':
        if ok2move(player, act, pieces):
            target_x, target_y = move_location(act[1], act[2], act[4])
            move(act[1], act[2], act[3], target_x, target_y, pieces)
            return True
        else:
            print("Player unable to move.")
            print("Try another action!")
            return False
    elif act[0] == 'c':
        if ok2capture(player, act, pieces):
            capture(act, pieces, dead_list)
            return True
        else:
            print("Player unable to capture.")
            print("Try another action!")
            return False
    elif act[0] == 'r':
        if ok2rotate(player, act, pieces):
            rotate(act[1], act[2], act[3], pieces)
            return True
        else:
            print("Player unable to rotate.")
            print("Try another action!")
            return False
    else:
        print("Wrong input for action.")
        return False
 

def changeplayer(player):
    if player == '1':
        return '2'
    return '1'

def end_condition(pieces):
    kings = []
    for p in pieces:
        if p[3] == 'k':
            kings.append(p)
    return kings

raund = 1
player = '1'

display(fig, ax, pieces, beams, 2)

while True:
    state = [raund, player, pieces]
    with open('state.txt', 'w') as f:
        json.dump(state, f)
    sleep(0.25)
    print('Raund: ', raund)
    
    while True: 
        with open('action' + player + '.txt') as f:
            data = json.load(f)
        if len(data) == 2:
            if data[0] == raund:
                act = data[1]
                break
            else:
                sleep(1)
        else:
            sleep(1)

    if act == 'koral': #TEST to break
        break

    if not action(player, act, pieces, dead_list, beams):
        continue

    for d in dead_list:
        if d in pieces:
            pieces.remove(d)
    dead_list = []
    beams = []

    display(fig, ax, pieces, beams, 1)

    kings = end_condition(pieces)
    if len(kings) == 0:
        print("Both kings are dead! Draw!")
        break
    elif len(kings) == 1:
        print("Player " + kings[0][4] + " wins!")
        break
    
    player = changeplayer(player)
    raund += 1








