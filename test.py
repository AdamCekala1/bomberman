from random import randint
import random
import time
from time import sleep
import math
import os


class Player(object):
    def move(self, sym):
        if sym == 'w':
            self.y = self.y - 1

        if sym == 's':
            self.y = self.y + 1

        if sym == 'a':
            self.x = self.x - 1

        if sym == 'd':
            self.x = self.x + 1

    def __init__(self,x,y,char):
        # self.level = level
        # self.health = health
        self.x = x
        self.y = y
        self.char=char
        self.level = 1
    def set_position(self,x,y):
        self.x=x
        self.y=y
    def get_position(self):
        return [self.x,self.y]
    def atack(self):
        B = Bomb(self.level,self.x,self.y,3)
        board[self.x][self.y] = B.char



class Monster(object):
    def __init__(self, power,health):
        self.power = power
        self.health = health

class Bomb(object):
    def __init__(self, power,x,y,time):
        self.power = power
        self.x = x
        self.y = y
        self.time = time
        self.char = '!'


class Wall(object):
    def set_health(self):
        if (self.type == 0):
            self.health = 100000
            self.char = '.'
        elif(self.type!=1):
            self.health = 100000
            self.char='#'
        else:
            self.health=1
            self.char = '0'
    def atacked(self):
        if (self.type != 1):
            self.health = 100000
        else:
            self.health=self.health-1
    def __init__(self, type,x,y):
        self.type = type
        self.set_health()
        self.x=x
        self.y=y


# objectWall = Wall(1,1,1)
# Player2 = Player(0,0,'A')
# print(Player2.x)
# Player2.move('w')
# print('wspol')
# print(Player2.y)
# print(Player2.x)
# print('type:')
# print(objectWall.type)




# generowanie planszy

board = []
walls = []
dimension = 40
# create walls

class empty(object):
    char='.'
    def __init__(self):
        self.char='.'


for x in range(dimension):
    board.append(["."] * dimension)
    walls.append(["."] * dimension)

for x in range(dimension):
    for i in range(dimension):
        for j in range(dimension):
             board[i][j] = empty
             walls[i][j] = empty

def board_with_walls(board,walls):
    for i in range(dimension):
        for j in range(dimension):
            if(walls[i][j].char != '.' ):
                board[i][j] = walls[i][j]

def print_board(board):
    for i in range(dimension):
        for j in range(dimension):
            print(board[i][j].char)



def randomPos(board):
    randomInt = random.randrange(2, dimension-2,1)
    return randomInt

ship_row=[]
ship_col=[]

def walls_create(walls_to_use,board,type,how_much):
    i=0
    while (i<dimension*how_much):
        random_row = randomPos(walls_to_use)
        random_col = randomPos(walls_to_use)
        walls_row = random_row
        walls_col = random_col
        if(type==1):
            if(walls[walls_row][walls_col]!= '.'):
                # print('smutek')
                i=i-1
            else:
                walls_to_use[walls_row][walls_col] = Wall(type,walls_row,walls_col)
                # board[walls_row][walls_col] = walls_to_use[walls_row][walls_col].char
        elif(type!=1):
            wrong = 0
            if (walls[walls_row][walls_col] != '.'):
                wrong=1
            if(i>0):
                if(0<walls_col-1):
                    if(walls[walls_row][walls_col-1] != '.'):
                        wrong = 1

                if(walls_col+1<dimension):
                    if (walls_row + 1 < dimension):
                        if (walls[walls_row+1][walls_col + 1] != '.'):
                            wrong = 1
                    if(walls[walls_row][walls_col+1] != '.'):
                        wrong = 1

                if(walls_row+1<dimension ):
                    if (0 < walls_col - 1):
                        if (walls[walls_row+1][walls_col - 1] != '.'):
                            wrong = 1
                    if(walls[walls_row+1][walls_col] != '.'):
                        wrong = 1

                if(0<walls_row-1):
                    if (walls_col + 1 < dimension):
                        if (walls[walls_row - 1][walls_col +1 ] != '.'):
                            wrong = 1
                    if (walls_col - 1 < dimension):
                        if (walls[walls_row - 1][walls_col -1 ] != '.'):
                            wrong = 1
                    if(walls[walls_row-1][walls_col] != '.'):
                        wrong = 1

            if(wrong!=0):
                i=i-1
                # print('smutek')
            else:
                walls_to_use[walls_row][walls_col] = Wall(type,walls_row,walls_col);
                # board[walls_row][walls_col] = walls_to_use[walls_row][walls_col].char


        i=i+1
        # print(i)
Player1 = Player(0,0,'A')
def createPlayers(Player1):
    walls_row,walls_col = Player1.get_position()
    board[walls_row][walls_col] =Player1.char


walls_create(walls,board,1,3)
walls_create(walls,board,2,1)
print(walls)
print(board)
createPlayers(Player1)
board_with_walls(board,walls)
print_board(board)
# print('OK')
# for i in range(0,dimension):
#     for j in range(0,dimension):
#         print(board[i][j])

# print(ship_row)
# print(ship_col)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


# gra

#
# for i in range(400):
#     print("Turn ", i + 1)
#     guess_row = int(input("Guess Row:"))
#     guess_col = int(input("Guess Col:"))
#
#     if guess_row == ship_row and guess_col == ship_col:
#         print("Congratulations! You sunk my battleship!")
#         break
#     else:
#         if (guess_row < 0 or guess_row > dimension-1) or (guess_col < 0 or guess_col > dimension-1):
#             print("Oops, that's not even in the ocean.")
#             board[guess_row][guess_col] = "X"
#         else:
#             print("You missed my battleship!")
#             board[guess_row][guess_col] = "X"
#         # cls()
#         print_board(board)

#
# def main():
#     looperCPU = 1000000000000000000000
#     myStart = time.time()
#     while (looperCPU != 0):
#         sleep(0.5)
#         print("total time taken this loop: ", time.time() - myStart)
#         # print("Turn ", i + 1)
#         # guess_row = int(input("Guess Row:"))
#         # guess_col = int(input("Guess Col:"))
#         guess_row = randint(0, len(board[0]) - 1)
#         guess_col = randint(0, len(board[0]) - 1)
#
#         if guess_row == ship_row and guess_col == ship_col:
#             print("Congratulations! You sunk my battleship!")
#             break
#         else:
#             if (guess_row < 0 or guess_row > dimension - 1) or (guess_col < 0 or guess_col > dimension - 1):
#                 print("Oops, that's not even in the ocean.")
#                 board[guess_row][guess_col] = "X"
#             else:
#                 print("You missed my battleship!")
#                 board[guess_row][guess_col] = "X"
#             cls()
#             print_board(board)
#
#
# main()