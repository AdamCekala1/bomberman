from random import randint
import random
import time
from time import sleep
import math
import os
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
#---------------------------------------------------------------------
# klasy
class Player(object):
    def getPrevPos(self):
        return [self.prevX,self.prevY]
    def move(self, sym):
        self.prevY = self.y
        self.prevX = self.x
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
        self.prevX = self.x
        self.prevY = self.y
        self.hp = 2
    def killed(self):
        if(self.hp<=0):
            return True
        else:
            return False
    def set_position(self,x,y):
        self.x=x
        self.y=y
    def get_position(self):
        return [self.x,self.y]




class Monster(object):
    def __init__(self, power,x,y,number):
        self.power = power
        self.x = x
        self.y = y
        self.number = number
        if(str(self.power)==str(1)):
            self.char = 'N'
        else:
            self.char = 'M'
    def position(self):
        return  self.x,self.y

class Bomb(object):
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.type = type
        self.char = '!'
    def explode(self):
        if (self.type==1):
            self.destroyObjectsX =[]
            self.destroyObjectsY =[]
            for i in range(-5,5,1):
                self.destroyObjectsX.append(self.x+i)
                self.destroyObjectsY.append(self.y+i)

            return [self.destroyObjectsX,self.destroyObjectsY]


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




#---------------------------------------------------------------------
# generowanie planszy

board = []

dimension = 40




# create walls




class empty(object):
    char='.'
    def __init__(self):
        self.char='.'


for x in range(dimension):
    board.append(["."] * dimension)




def print_board(board):
    # cls()
    # refresPlayerPos(Player1)
    for row in board:
        print(" ".join(row))




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
            if(walls_to_use[walls_row][walls_col]!= '.'):
                # print('smutek')
                i=i-1
            else:
                walls_to_use[walls_row][walls_col] = Wall(type,walls_row,walls_col).char
                # board[walls_row][walls_col] = walls_to_use[walls_row][walls_col].char
        elif(type!=1):
            wrong = 0
            if (walls_to_use[walls_row][walls_col] != '.'):
                wrong=1
            if(i>0):
                if(0<walls_col-1):
                    if(walls_to_use[walls_row][walls_col-1] != '.'):
                        wrong = 1

                if(walls_col+1<dimension):
                    if (walls_row + 1 < dimension):
                        if (walls_to_use[walls_row+1][walls_col + 1] != '.'):
                            wrong = 1
                    if(walls_to_use[walls_row][walls_col+1] != '.'):
                        wrong = 1

                if(walls_row+1<dimension ):
                    if (0 < walls_col - 1):
                        if (walls_to_use[walls_row+1][walls_col - 1] != '.'):
                            wrong = 1
                    if(walls_to_use[walls_row+1][walls_col] != '.'):
                        wrong = 1

                if(0<walls_row-1):
                    if (walls_col + 1 < dimension):
                        if (walls_to_use[walls_row - 1][walls_col +1 ] != '.'):
                            wrong = 1
                    if (walls_col - 1 < dimension):
                        if (walls_to_use[walls_row - 1][walls_col -1 ] != '.'):
                            wrong = 1
                    if(walls_to_use[walls_row-1][walls_col] != '.'):
                        wrong = 1

            if(wrong!=0):
                i=i-1
                # print('smutek')
            else:
                walls_to_use[walls_row][walls_col] = Wall(type,walls_row,walls_col).char;
                # board[walls_row][walls_col] = walls_to_use[walls_row][walls_col].char


        i=i+1
        # print(i)

Player1 = Player(0,0,'A')

Monsters = []

def monsterCreate(board,i):
    end = False
    while end==False:
        randomX = random.randrange(2, dimension - 20, 1)
        randomY = random.randrange(2, dimension - 20, 1)
        if(board[randomY][randomX] == '.'):
            end=True
    power = random.randrange(0,2,1)
    # print(power)
    M = Monster(power,randomX,randomY,i)
    board[randomY][randomX] = M.char
    return M



walls_create(board,board,1,3)
walls_create(board,board,2,1)
for i in range(0,5,1):
    M = monsterCreate(board,i)
    Monsters.append(M)

# board_with_walls(board,walls)



print_board(board)


