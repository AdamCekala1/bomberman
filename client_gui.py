# w self.game jest [Y][X]

# ****************************************************** znajdowanie i zamykanie klocka o x=5 y=5
# objectO = self.findChild(QWidget, "wall_type1_5_5");
# objectO.close()
# *************************************************************************************
# *************************************************************************************


import sys
import random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import math
import xml

import jsonpickle

import threading

from PyQt5.QtCore import Qt, QBasicTimer
# from wnoGame import *
dimension=40

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
        self.canControl = True
        self.x = x
        self.y = y
        self.char=char
        self.level = 1
        self.prevX = self.x
        self.prevY = self.y
        self.hp = 4
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
        self.agresor=False
        self.dead = False
        self.number = number
        if(str(self.power)==str(1)):
            self.char = 'N'
        else:
            self.char = 'M'
    def position(self):
        return  self.x,self.y

    def __del__(self):
        self.close()
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
    def get_position(self):
        return [self.x,self.y]

class Bomb(object):
    def __init__(self,x,y,type,number):
        self.x = x
        self.y = y
        self.type = type
        self.number = number
        self.char = '!'
    def explode(self):
        if (self.type==1):
            self.destroyObjectsX =[]
            self.destroyObjectsY =[]
            for i in range(-5,5,1):
                self.destroyObjectsX.append(self.x+i)
                self.destroyObjectsY.append(self.y+i)

            return [self.destroyObjectsX,self.destroyObjectsY]

def print_board(board):
    # cls()
    # refresPlayerPos(Player1)
    for row in board:
        print(" ".join(row))

Player1 = Player(0,0,'A')


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.countBomb = 0
        self.Bombs = []
        self.BombIsPlant = False
        self.BombIsPlantBOT = False
        self.connect_to_socket()
        self.click_bomb=0
        self.Bot_Bombs = [object,object,object,object,object]
        self.click_bomb_Bot=0
        self.initUI()
    def paintEvent(self, *args, **kwargs):
        try:

            print("refresh")
            if(Player1):
                if (Player1.killed() == True):
                    # self.game[self.B.y][self.B.x] = '.'
                    print("#####MARTWY######")
                    objectO = self.findChild(QWidget, "user")
                    objectO.close()
            # print(str(self.game[3][3]) == str(Player1.char))
            for i in range(0, dimension):
                for j in range(0, dimension):
                    if (str(self.game[i][j]) == str(Player1.char)):
                        if(Player1):
                            # Player1.set_position((i,j))
                            self.user.setGeometry(QtCore.QRect(j * 21, i * 21, 21, 21))
                    elif (str(self.game[i][j]) == str("M") or str(self.game[i][j]) == str("N")):
                        for Monster in self.Monsters:
                            if(Monster.x==i):
                                if(Monster.y==j):
                                    print("czo to za stwor?")

        except:
            pass


    def initMap(self):
        self.labels = []
        monsterNumber = 0
        self.Monsters = []
        for i in range(0, dimension):
            for j in range(0, dimension):
                if (self.game[i][j] == '#'):
                    self.wall_type2 = QtWidgets.QPushButton(self.frame)
                    self.wall_type2.setGeometry(QtCore.QRect(j * 21, i * 21, 21, 21))
                    self.wall_type2.setText("")
                    icon3 = QtGui.QIcon()
                    icon3.addPixmap(QtGui.QPixmap(":/wall2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.wall_type2.setIcon(icon3)
                    self.wall_type2.setIconSize(QtCore.QSize(21, 21))
                    self.wall_type2.setObjectName("wall_type2_" + str(i) + '_' + str(j))
                    self.labels.append(self.wall_type2)
                    # print(self.wall_type2.objectName())
                if (self.game[i][j] == '0'):
                    self.wall_type1 = QtWidgets.QPushButton(self.frame)
                    self.wall_type1.setGeometry(QtCore.QRect(j * 21, i * 21, 21, 21))
                    self.wall_type1.setText("")
                    icon2 = QtGui.QIcon()
                    icon2.addPixmap(QtGui.QPixmap(":/wall1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.wall_type1.setIcon(icon2)
                    self.wall_type1.setIconSize(QtCore.QSize(21, 21))
                    self.wall_type1.setObjectName("wall_type1_" + str(i) + '_' + str(j))
                    self.labels.append(self.wall_type1)
                if(self.game[i][j] == 'N' or self.game[i][j] == 'M'):

                    if(self.game[i][j] == 'N'):
                        self.Monsters.append(Monster(1,j,i,monsterNumber))
                        self.monster = QtWidgets.QPushButton(self.frame)
                        self.monster.setGeometry(QtCore.QRect(j * 21, i * 21, 21, 21))
                        self.monster.setText("")
                        icon1 = QtGui.QIcon()
                        icon1.addPixmap(QtGui.QPixmap(":/soldier.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        self.monster.setIcon(icon1)
                        self.monster.setIconSize(QtCore.QSize(21, 21))
                        self.monster.setObjectName("Monster" + str(monsterNumber))

                    elif(self.game[i][j] == 'M'):
                        self.Monsters.append(Monster(0, j, i, monsterNumber))
                        self.monster2 = QtWidgets.QPushButton(self.frame)
                        self.monster2.setGeometry(QtCore.QRect(j * 21, i * 21, 21, 21))
                        self.monster2.setText("")
                        icon1 = QtGui.QIcon()
                        icon1.addPixmap(QtGui.QPixmap(":/thief.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        self.monster2.setIcon(icon1)
                        self.monster2.setIconSize(QtCore.QSize(21, 21))
                        self.monster2.setObjectName("Monster" + str(monsterNumber))
                    print("Monster" + str(monsterNumber))
                    monsterNumber = monsterNumber +1



    def initUI(self):
        self.setGeometry(100, 100, 994, 905)
        self.setWindowTitle('Event handler')

        self.setStyleSheet("QWidget{\n"
                                 " background-color:#2980b9;\n"
                                 "}\n"
                                 "QFrame{\n"
                                 "background-color:#ecf0f1;\n"
                                 "}\n"
                                   "QPushButton{\n"
                                 "background-color:white;\n"
                                 "}\n"
                                 "QLabel{\n"
                                 " background-color:#2980b9;\n"
                                 "}")
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(70, 20, 840, 840))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        enemyList = []



        self.initMap()


        # user
        userx, usery = 0,0;
        self.user = QtWidgets.QPushButton(self.frame)
        self.user.setGeometry(QtCore.QRect(userx*21, usery*21, 21, 21))
        self.user.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.user.setIcon(icon1)
        self.user.setIconSize(QtCore.QSize(21, 21))
        self.user.setObjectName("user")

        # bomb

        self.bomb = QtWidgets.QPushButton(self.frame)
        self.bomb.setGeometry(QtCore.QRect(-21,  -21, 21, 21))
        self.bomb.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/enemy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bomb.setIcon(icon1)
        self.bomb.setIconSize(QtCore.QSize(21, 21))
        self.bomb.setObjectName("bomb")
        for i in range(0,len(self.Monsters),1):
            self.bombBot = QtWidgets.QPushButton(self.frame)
            self.bombBot.setGeometry(QtCore.QRect(-21, -21, 21, 21))
            self.bombBot.setText("")
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap(":/enemy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.bombBot.setIcon(icon1)
            self.bombBot.setIconSize(QtCore.QSize(21, 21))
            self.bombBot.setObjectName("bomb"+str(i))
            self.Bot_Bombs[i] = self.bombBot
            print(i)





        self.show()

    # def paintEvent(self, *args, **kwargs):
    #     qp = QtGui.QPainter()
    #     self.initMap()




    # ////////////////////////////////////




    def recieve(self, socket):
        while True:
            try:
                resp = self.clientsocket.recv(64920).decode('utf-8')
                map = jsonpickle.decode(resp)
                self.prevMap = self.game
                self.game = map
                # print_board(self.game)
                print("otrzymalem")
                self.repaint()
            except:
                print("error")


    def send(self, map):
        self.clientsocket.send(jsonpickle.encode(map).encode('utf-8'))


    def connect_to_socket(self):
        try:
            self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientsocket.connect(('Pc_Adam', 8070))
            resp = self.clientsocket.recv(64920).decode('utf-8')
            map = jsonpickle.decode(resp)
            self.game = map
            print_board(self.game)
            # threading.Thread(target=self.recieve, args=(self.clientsocket,)).start()
            threading.Thread(target = self.recieve, args = (self.clientsocket,)).start()
        except:
            print("error")




    # //////////////////////////////////////////////
    def destroy_by_bom(self):
        # print(self.explX)
        for i in self.explX:
            # print('Punkt:'+str(i)+"_"+str(self.positiony))
            if (self.game[self.positiony][i] == 'N' or self.game[self.positiony][i] == 'M'):
                for Monster in self.Monsters:
                    if Monster.x == i:
                        if self.positiony == Monster.y:
                            self.game[self.positiony][i] = '.'
                            objectO = self.findChild(QWidget, "Monster" + str(Monster.number))
                            objectO.close()
                            Monster.dead = True


            #     self.game[self.positiony][i] = '.'
            if(self.game[self.positiony][i]=='0'):
                self.game[self.positiony][i] = '.'
                objectO = self.findChild(QWidget, "wall_type1_"+str(self.positiony)+"_"+str(i))
                if(objectO):
                    objectO.close()
            if(str(self.game[self.positiony][i])==str(Player1.char)):
                Player1.hp = Player1.hp - 1
                print("8888888888888888888888888888888888888")
                print("OBERWALEM")
                print("8888888888888888888888888888888888888")
                if(Player1.killed() == True):
                    self.game[Player1.y][Player1.x]= '.'
                    objectO = self.findChild(QWidget, "user")
                    objectO.close()
                    self.send(self.game)
        if(self.B.x == Player1.x and self.B.y == Player1.y):
            Player1.hp = Player1.hp - 1
            print("8888888888888888888888888888888888888")
            print("OBERWALEM")
            print("8888888888888888888888888888888888888")
            if (Player1.killed() == True):
                self.game[Player1.y][Player1.x] = '.'
                objectO = self.findChild(QWidget, "user")
                objectO.close()
                self.send(self.game)

        for i in self.explY:
            if (self.game[i][self.positionx] == 'N' or self.game[i][self.positionx] == 'M'):
                for Monster in self.Monsters:
                    if Monster.y == i:
                        if self.positionx == Monster.x:
                            self.game[i][self.positionx] = '.'
                            objectO = self.findChild(QWidget, "Monster" + str(Monster.number))
                            objectO.close()
                            Monster.dead = True
            if (self.game[i][self.positionx] == '0'):
                self.game[i][self.positionx] = '.'
                objectO = self.findChild(QWidget, "wall_type1_"+str(i)+"_"+str(self.positionx))
                if(objectO):
                    objectO.close()
            if (str(self.game[i][self.positionx]) == str(Player1.char)):
                Player1.hp = Player1.hp - 1
                print("8888888888888888888888888888888888888")
                print("OBERWALEM")
                print("8888888888888888888888888888888888888")
                if (Player1.killed() == True):
                    self.game[Player1.y][Player1.x] = '.'
                    objectO = self.findChild(QWidget, "user")
                    objectO.close()
                    self.send(self.game)

        if (self.game[self.positiony][self.positionx]=='!'):
            self.game[self.positiony][self.positionx]='.'
        self.click_bomb=0
        self.bomb.setGeometry(QtCore.QRect(-self.positionx * 21, -self.positiony * 21, 21, 21))
        self.send(self.game)
        del self.B
        self.timer.stop()
        print("Booom")
        self.BombIsPlant = False

    def destroy_by_Bot(self):
        # print(self.explX)
        for i in self.explXBot1:
            # print('Punkt:'+str(i)+"_"+str(self.positiony))
            if (self.game[self.positiony][i] == 'N' or self.game[self.positiony][i] == 'M'):
                for Monster in self.Monsters:
                    if Monster.x == i:
                        if self.positiony == Monster.y:
                            self.game[self.positiony][i] = '.'
                            objectO = self.findChild(QWidget, "Monster" + str(Monster.number))
                            objectO.close()
                            Monster.dead = True


            #     self.game[self.positiony][i] = '.'
            if(self.game[self.positiony][i]=='0'):
                self.game[self.positiony][i] = '.'
                objectO = self.findChild(QWidget, "wall_type1_"+str(self.positiony)+"_"+str(i))
                if(objectO):
                    objectO.close()
            if(str(self.game[self.positiony][i])==str(Player1.char)):
                Player1.hp = Player1.hp - 1
                print("8888888888888888888888888888888888888")
                print("OBERWALEM")
                print("8888888888888888888888888888888888888")
                if(Player1.killed() == True):
                    self.game[Player1.y][Player1.x]= '.'
                    objectO = self.findChild(QWidget, "user")
                    objectO.close()
                    self.send(self.game)



        for i in self.explYBot1:
            if (self.game[i][self.positionx] == 'N' or self.game[i][self.positionx] == 'M'):
                for Monster in self.Monsters:
                    if Monster.y == i:
                        if self.positionx == Monster.x:
                            self.game[i][self.positionx] = '.'
                            objectO = self.findChild(QWidget, "Monster" + str(Monster.number))
                            objectO.close()
                            Monster.dead = True
            if (self.game[i][self.positionx] == '0'):
                self.game[i][self.positionx] = '.'
                objectO = self.findChild(QWidget, "wall_type1_"+str(i)+"_"+str(self.positionx))
                if(objectO):
                    objectO.close()
            if (str(self.game[i][self.positionx]) == str(Player1.char)):
                print("8888888888888888888888888888888888888")
                print("OBERWALEM")
                print("8888888888888888888888888888888888888")
                Player1.hp = Player1.hp - 1
                if (Player1.killed() == True):
                    self.game[Player1.y][Player1.x] = '.'
                    objectO = self.findChild(QWidget, "user")
                    objectO.close()
                    self.send(self.game)

        if (self.game[self.positiony][self.positionx]=='!'):
            self.game[self.positiony][self.positionx]='.'
        for Monster in self.Monsters:
            if Monster.agresor == True:
                self.bombBot.setGeometry(QtCore.QRect(-self.positionx * 21, -self.positiony * 21, 21, 21))
                Monster.agresor = False
        # self.bomb.setGeometry(QtCore.QRect(-self.positionx * 21, -self.positiony * 21, 21, 21))
        self.send(self.game)
        self.click_bomb_Bot = self.click_bomb_Bot - 1
        self.timerBombBot.stop()
        print("Booom")
        self.BombIsPlantBOT = False


    def botAI(self):
        for Monster in self.Monsters:
            if Monster.dead==False:
                print("Bot poza kontrola!")
                nearestEnemey= math.sqrt(math.pow(Monster.x - Player1.x, 2) + math.pow(Monster.y - Player1.y, 2))
                choosenEnemey = Player1

                xP = Monster.x
                yP = Monster.y


                move = False
                cantGoUp = False
                cantGoLeft = False
                cantGoRight = False
                cantGoDown = False
                if  (choosenEnemey.x != Monster.x or choosenEnemey.y != Monster.y):
                    if self.BombIsPlant == True or self.BombIsPlantBOT==True:
                        if self.BombIsPlant == True:
                            if (self.B):
                                BombDist = math.sqrt(math.pow(self.B.x - Monster.x, 2) + math.pow(self.B.y - Monster.y, 2))
                                X = self.B.x
                                Y = self.B.y
                        if self.BombIsPlantBOT == True:
                            BombDist = math.sqrt(math.pow(self.BBomb.x - Monster.x, 2) + math.pow(self.BBomb.y - Monster.y, 2))
                            X = self.BBomb.x
                            Y = self.BBomb.y

                        if(BombDist<6 and (X == Monster.x or Y == Monster.y) ):

                                if (X == Monster.x):
                                    randchoose3 = random.randrange(0, 2, 1)
                                    if (randchoose3 == 1):

                                        self.botMoveD(Monster)
                                        xP2= Monster.x
                                        yP2 = Monster.y
                                        if (xP2 - xP != 0):
                                            move = True

                                    else:
                                        self.botMoveA(Monster)
                                        xP2, yP2 = Monster.get_position()
                                        if (xP2 - xP != 0):
                                            move = True

                                if (Y == Monster.y):
                                    randchoose3 = random.randrange(0, 2, 1)
                                    if (randchoose3 == 1):
                                        self.botMoveS(Monster)
                                        xP2, yP2 = Monster.get_position()
                                        if (yP2 - yP != 0):
                                            move = True

                                    else:
                                        self.botMoveW(Monster)
                                        xP2, yP2 = Monster.get_position()
                                        if (yP2 - yP != 0):
                                            move = True
                                else:
                                    move = True

                    if(nearestEnemey>4):
                        while(move == False):
                            randchoose = random.randrange(0, 2, 1)

                            if(randchoose==1):
                                if(xP < choosenEnemey.x):
                                    self.botMoveD(Monster)
                                    xP2, yP2 = Monster.get_position()
                                    if(xP2 - xP != 0):
                                        move =True

                                    else:
                                        cantGoRight = True
                                elif(xP > choosenEnemey.x):
                                    self.botMoveA(Monster)
                                    xP2, yP2 = Monster.get_position()
                                    if (xP2 - xP != 0):
                                        move = True

                                    else:
                                        cantGoLeft = True
                            elif (randchoose == 0):
                                if(yP < choosenEnemey.y):
                                    self.botMoveS(Monster)
                                    xP2, yP2 = Monster.get_position()
                                    if(yP2 - yP != 0):
                                        move =True

                                    else:
                                        cantGoDown = True
                                elif(yP > choosenEnemey.y):
                                    self.botMoveW(Monster)
                                    xP2, yP2 = Monster.get_position()
                                    if (yP2 - yP != 0):
                                        move = True

                                    else:
                                        cantGoUp = True

                            if(move == False):
                                while (move == False):
                                    randchoose2 = random.randrange(1, 5, 1)
                                    if (randchoose2 == 1):

                                        self.botMoveS(Monster)
                                        xP2, yP2 = Monster.get_position()
                                        if (yP2 - yP != 0):
                                            move = True
                                    if (randchoose2 == 2):

                                        self.botMoveW(Monster)
                                        xP2, yP2 = Monster.get_position()
                                        if (yP2 - yP != 0):
                                            move = True
                                    if (randchoose2 == 3):

                                        self.botMoveD(Monster)
                                        xP2, yP2 = Monster.get_position()
                                        if (xP2 - xP != 0):
                                            move = True
                                    if (randchoose2 == 4):

                                        self.botMoveA(Monster)
                                        xP2, yP2 = Monster.get_position()
                                        if (xP2 - xP != 0):
                                            move = True
                            cantGoUp = False
                            cantGoLeft = False
                            cantGoRight = False
                            cantGoDown = False


                if nearestEnemey > 0 and nearestEnemey < 8 and (choosenEnemey.x==Monster.x or Monster.y == choosenEnemey.y):
                    print("**************************************")
                    print("BOT stawia bombe!")
                    print("**************************************")
                    Monster.agresor = True
                    self.BotBomb()
                    # self.playerBomb()
        self.send(self.game)
    def playerAI(self):
        if Player1.killed()==False:
            print("gracz poza kontrola!")
            nearestEnemey= dimension
            choosenEnemey = object
            for Monster in self.Monsters:
                distance = math.sqrt(math.pow(Monster.x - Player1.x, 2) + math.pow(Monster.y - Player1.y, 2))
                if(distance<nearestEnemey and Monster.dead==False ):
                    nearestEnemey = distance
                    choosenEnemey = Monster
            xP,yP = Player1.get_position()

            move = False
            cantGoUp = False
            cantGoLeft = False
            cantGoRight = False
            cantGoDown = False
            if self.BombIsPlant == True or self.BombIsPlantBOT== True:
                if self.BombIsPlant == True:
                    BombDist = math.sqrt(math.pow(self.B.x - Player1.x, 2) + math.pow(self.B.y - Player1.y, 2))
                    X = self.B.x
                    Y = self.B.y
                if self.BombIsPlantBOT== True:
                    BombDist = math.sqrt(math.pow(self.BBomb.x - Player1.x, 2) + math.pow(self.BBomb.y - Player1.y, 2))
                    X= self.BBomb.x
                    Y= self.BBomb.y
                if (BombDist < 6 and (X == Player1.x or Y == Player1.y)):
                    while (move == False):

                        if (X == Player1.x):
                            randchoose3 = random.randrange(0, 2, 1)
                            if (randchoose3 == 1):

                                self.playerMoveD()
                                xP2, yP2 = Player1.get_position()
                                if (xP2 - xP != 0):
                                    move = True

                            else:
                                self.playerMoveA()
                                xP2, yP2 = Player1.get_position()
                                if (xP2 - xP != 0):
                                    move = True

                        if (Y == Player1.y):
                            randchoose3 = random.randrange(0, 2, 1)
                            if (randchoose3 == 1):
                                self.playerMoveS()
                                xP2, yP2 = Player1.get_position()
                                if (yP2 - yP != 0):
                                    move = True

                            else:
                                self.playerMoveW()
                                xP2, yP2 = Player1.get_position()
                                if (yP2 - yP != 0):
                                    move = True
                        else:
                            move = True

                # if self.BombIsPlant == True:
                #     print("o=pierdzielenuie")


            else:
                while(move == False):
                    randchoose = random.randrange(0, 2, 1)

                    if(randchoose==1):
                        if(xP < choosenEnemey.x):
                            self.playerMoveD()
                            xP2, yP2 = Player1.get_position()
                            if(xP2 - xP != 0):
                                move =True

                            else:
                                cantGoRight = True
                        elif(xP > choosenEnemey.x):
                            self.playerMoveA()
                            xP2, yP2 = Player1.get_position()
                            if (xP2 - xP != 0):
                                move = True

                            else:
                                cantGoLeft = True
                    elif (randchoose == 0):
                        if(yP < choosenEnemey.y):
                            self.playerMoveS()
                            xP2, yP2 = Player1.get_position()
                            if(yP2 - yP != 0):
                                move =True

                            else:
                                cantGoDown = True
                        elif(yP > choosenEnemey.y):
                            self.playerMoveW()
                            xP2, yP2 = Player1.get_position()
                            if (yP2 - yP != 0):
                                move = True

                            else:
                                cantGoUp = True

                    if(move == False):
                        while (move == False):
                            randchoose2 = random.randrange(1, 5, 1)
                            if (randchoose2 == 1):

                                self.playerMoveS()
                                xP2, yP2 = Player1.get_position()
                                if (yP2 - yP != 0):
                                    move = True
                            if (randchoose2 == 2):

                                self.playerMoveW()
                                xP2, yP2 = Player1.get_position()
                                if (yP2 - yP != 0):
                                    move = True
                            if (randchoose2 == 3):

                                self.playerMoveD()
                                xP2, yP2 = Player1.get_position()
                                if (xP2 - xP != 0):
                                    move = True
                            if (randchoose2 == 4):

                                self.playerMoveA()
                                xP2, yP2 = Player1.get_position()
                                if (xP2 - xP != 0):
                                    move = True
                    cantGoUp = False
                    cantGoLeft = False
                    cantGoRight = False
                    cantGoDown = False

            if nearestEnemey > 0 and nearestEnemey < 6 and (abs(choosenEnemey.x-Player1.x)<1 or abs(choosenEnemey.y-Player1.y)<1):
                print("************************")
                print("stawiam pake")
                print("************************")
                self.playerBomb()
                # self.escape(Player1)

    def updateGuiBot(self,bot):
        objectO = self.findChild(QWidget, "Monster" + str(bot.number))
        objectO.setGeometry(QtCore.QRect(bot.x * 21, bot.y * 21, 21, 21))

    def botMoveD(self,bot):
        positionx = bot.x
        positiony = bot.y
        if (positionx + 1 < dimension):
            nextPosition = self.game[positiony][positionx + 1]
            if (nextPosition == '.'):
                self.game[positiony][positionx] = '.'
                bot.move('d')
                self.game[bot.y][bot.x] = bot.char


                # print_board(self.game)
                self.send(self.game)
                self.updateGuiBot(bot)
                # self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))

    def botMoveA(self,bot):
        positionx = bot.x
        positiony = bot.y
        if (positionx - 1 >= 0):
            nextPosition = self.game[positiony][positionx - 1]
            if (nextPosition == '.'):
                self.game[positiony][positionx] = '.'
                bot.move('a')
                self.game[bot.y][bot.x] = bot.char

                # print_board(self.game)
                self.send(self.game)
                self.updateGuiBot(bot)
                # self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))

    def botMoveS(self,bot):
        positionx = bot.x
        positiony = bot.y
        if (positiony + 1 <= dimension - 1):
            nextPosition = self.game[positiony + 1][positionx]
            if (nextPosition == '.'):
                self.game[positiony][positionx] = '.'
                bot.move('s')
                self.game[bot.y][bot.x] = bot.char

                # print_board(self.game)
                self.send(self.game)
                self.updateGuiBot(bot)
                # self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))

    def botMoveW(self,bot):
        positionx = bot.x
        positiony = bot.y
        if (positiony - 1 >= 0):
            nextPosition = self.game[positiony - 1][positionx]
            if (nextPosition == '.'):
                self.game[positiony][positionx] = '.'
                bot.move('w')
                self.game[bot.y][bot.x] =bot.char

                # print_board(self.game)
                self.send(self.game)
                self.updateGuiBot(bot)
                # self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))




    def playerMoveD(self):
        positionx, positiony = Player1.get_position()
        if (positionx + 1 < dimension):
            nextPosition = self.game[positiony][positionx + 1]
            if (nextPosition == '.'):
                self.game[positiony][positionx] = '.'
                Player1.move('d')
                self.game[Player1.y][Player1.x] = 'A'

                # print_board(self.game)
                self.send(self.game)
                self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))

    def playerMoveA(self):
        positionx, positiony = Player1.get_position()
        if (positionx - 1 >= 0):
            nextPosition = self.game[positiony][positionx - 1]
            if (nextPosition == '.'):
                self.game[positiony][positionx] = '.'
                Player1.move('a')
                self.game[Player1.y][Player1.x] = 'A'

                # print_board(self.game)
                self.send(self.game)
                self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))

    def playerMoveS(self):
        positionx, positiony = Player1.get_position()
        if (positiony + 1 <= dimension - 1):
            nextPosition = self.game[positiony + 1][positionx]
            if (nextPosition == '.'):
                self.game[positiony][positionx] = '.'
                Player1.move('s')
                self.game[Player1.y][Player1.x] = 'A'

                # print_board(self.game)
                self.send(self.game)
                self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))
    def playerMoveW(self):
        positionx, positiony = Player1.get_position()
        if (positiony - 1 >= 0):
            nextPosition = self.game[positiony - 1][positionx]
            if (nextPosition == '.'):
                self.game[positiony][positionx] = '.'
                Player1.move('w')
                self.game[Player1.y][Player1.x] = 'A'

                # print_board(self.game)
                self.send(self.game)
                self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))



    def playerBomb(self):
        if (self.click_bomb == 0):
            self.BombIsPlant = True
            self.click_bomb = 1
            self.positionx, self.positiony = Player1.get_position()

            self.bomb.setGeometry(QtCore.QRect(self.positionx * 21, self.positiony * 21, 21, 21))
            self.B = Bomb(self.positionx, self.positiony, 1,self.countBomb)
            self.Bombs.append(self.B)
            # print(self.B.char)
            # print(self.positionx, self.positiony)
            self.game[self.positiony][self.positionx] = self.B.char
            self.explX, self.explY = self.B.explode()

            self.timer = QtCore.QTimer()

            self.timer.timeout.connect(self.update)
            self.timer.start(2000)
            self.var = 'b'
            self.timer.timeout.connect(self.destroy_by_bom)

            self.send(self.game)
    def BotBomb(self):
        if (self.click_bomb_Bot < 1):
            self.BombIsPlantBOT = True
            self.click_bomb_Bot = self.click_bomb_Bot + 1
            self.positionx, self.positiony = 0 ,0
            for Monster in self.Monsters:
                if Monster.agresor == True:
                    self.positionx, self.positiony = Monster.get_position()

                    self.bombBot.setGeometry(QtCore.QRect(self.positionx * 21, self.positiony * 21, 21, 21))
                    self.BBomb = Bomb(self.positionx, self.positiony, 1,Monster.number)
                    # self.Bombs.append(self.BBomb)
                    # print(self.B.char)
                    # print(self.positionx, self.positiony)
                    self.game[self.positiony][self.positionx] = self.BBomb.char
                    self.explXBot1, self.explYBot1 = self.BBomb.explode()

                    self.timerBombBot = QtCore.QTimer()

                    self.timerBombBot.timeout.connect(self.update)
                    self.timerBombBot.start(2000)
                    self.var = 'b'
                    self.timerBombBot.timeout.connect(self.destroy_by_Bot)

                    self.send(self.game)

    def keyPressEvent(self, e):
        if(Player1.killed()==False):
            if e.key() == Qt.Key_Q:
                self.bot = QtCore.QTimer()
                self.bot.timeout.connect(self.update)
                self.bot.start(500)
                self.bot.timeout.connect(self.botAI)
            if e.key() == Qt.Key_1:

                self.bot.stop()
            if e.key() == Qt.Key_E:

                Player1.canControl = False
                self.playerAItimer = QtCore.QTimer()
                self.playerAItimer.timeout.connect(self.update)
                self.playerAItimer.start(500)
                self.playerAItimer.timeout.connect(self.playerAI)
            if e.key() == Qt.Key_3:

                self.playerAItimer.stop()
                Player1.canControl = True

            # STEROWANIE
            if Player1.canControl == True:
                if e.key() == Qt.Key_W:
                    self.playerMoveW()

                if e.key() == Qt.Key_S:
                    self.playerMoveS()

                if e.key() == Qt.Key_A:
                    self.playerMoveA()


                if e.key() == Qt.Key_D:
                    self.playerMoveD()

                if e.key() == Qt.Key_Escape:
                    print(self.click_bomb)
                    self.playerBomb()







import icon_rc
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())



