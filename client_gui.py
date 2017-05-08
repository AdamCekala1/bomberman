# w self.game jest [Y][X]

# ****************************************************** znajdowanie i zamykanie klocka o x=5 y=5
# objectO = self.findChild(QWidget, "wall_type1_5_5");
# objectO.close()
# *************************************************************************************
# *************************************************************************************


import sys

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
import socket

import jsonpickle

import threading

from PyQt5.QtCore import Qt, QBasicTimer
from wnoGame import *
dimension=40
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.connect_to_socket()
        self.click_bomb=0;
        self.initUI()
    def paintEvent(self, *args, **kwargs):
        try:

            print("refresh")
            # print(str(self.game[3][3]) == str(Player1.char))
            for i in range(0, dimension):
                for j in range(0, dimension):
                    if (str(self.game[i][j]) == str(Player1.char)):
                        if(Player1):
                            # Player1.set_position((i,j))
                            self.user.setGeometry(QtCore.QRect(j * 21, i * 21, 21, 21))

        except:
            pass


    def initMap(self):
        self.labels = []
        monsterNumber = 0
        Monsters = []
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
                        Monsters.append(Monster(1,i,j,monsterNumber))
                        self.monster = QtWidgets.QPushButton(self.frame)
                        self.monster.setGeometry(QtCore.QRect(j * 21, i * 21, 21, 21))
                        self.monster.setText("")
                        icon1 = QtGui.QIcon()
                        icon1.addPixmap(QtGui.QPixmap(":/soldier.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        self.monster.setIcon(icon1)
                        self.monster.setIconSize(QtCore.QSize(21, 21))
                        self.monster.setObjectName("Monster" + str(monsterNumber))

                    elif(self.game[i][j] == 'M'):
                        Monsters.append(Monster(0, i, j, monsterNumber))
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


        return self.labels


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





        self.show()

    # def paintEvent(self, *args, **kwargs):
    #     qp = QtGui.QPainter()
    #     self.initMap()




    # ////////////////////////////////////
    def recieve(self, socket):
        while True:
            resp = self.clientsocket.recv(64920).decode('utf-8')
            map = jsonpickle.decode(resp)
            self.prevMap = self.game
            self.game = map
            # print_board(self.game)
            print("otrzymalem")
            self.repaint()


    def send(self, map):
        self.clientsocket.send(jsonpickle.encode(map).encode('utf-8'))


    def connect_to_socket(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect(('Pc_Adam', 8070))
        resp = self.clientsocket.recv(64920).decode('utf-8')
        map = jsonpickle.decode(resp)
        self.game = map
        print_board(self.game)
        # threading.Thread(target=self.recieve, args=(self.clientsocket,)).start()
        threading.Thread(target = self.recieve, args = (self.clientsocket,)).start()




    # //////////////////////////////////////////////
    def destroy_by_bom(self):
        # print(self.explX)
        for i in self.explX:
            # print('Punkt:'+str(i)+"_"+str(self.positiony))
            if (self.game[self.positiony][i] == 'N' or self.game[self.positiony][i] == 'M'):
                for Monster in Monsters:
                    if Monster.x == i:
                        print('PRAWIE!')
                        print(Monster.y)
                        print(Monster.x)
                        print(self.positionx)
                        print(self.positiony)
                        print(i)
            #     self.game[self.positiony][i] = '.'
            if(self.game[self.positiony][i]=='0'):
                self.game[self.positiony][i] = '.'
                objectO = self.findChild(QWidget, "wall_type1_"+str(self.positiony)+"_"+str(i))
                objectO.close()
            if(str(self.game[self.positiony][i])==str(Player1.char)):
                Player1.hp = Player1.hp - 1
                if(Player1.killed() == True):
                    self.game[self.positiony][i]= '.'
                    print("#####oberwalem")
                    objectO = self.findChild(QWidget, "user")
                    objectO.close()

        for i in self.explY:
            # if (self.game[i][self.positionx] == 'N' or self.game[i][self.positionx] == 'M'):
                # for Monster in Monsters:
                #     if Monster.x == i:
                #         print('PRAWIE!')
                #         print(Monster.y)
                #         print(Monster.x)
                #         print(self.positionx)
                #         print(self.positiony)
                #         print(i)
                        # if Monster.y == self.positionx:
                        #     print('MAMY GO!')
                        #     objectO = self.findChild(QWidget, "Monster" + str(Monster.number))
                        #     print("Monster" + str(Monster.number))
                        #     objectO.close()
                            # self.game[i][self.positionx] = '.'
            if (self.game[i][self.positionx] == '0'):
                self.game[i][self.positionx] = '.'
                objectO = self.findChild(QWidget, "wall_type1_"+str(i)+"_"+str(self.positionx))
                objectO.close()
            if (str(self.game[i][self.positionx]) == str(Player1.char)):
                print("***********oberwalem")
                Player1.hp = Player1.hp - 1
                print(Player1.hp)
                print(Player1.killed())
                if (Player1.killed() == True):
                    self.game[self.positiony][i] = '.'
                    print("#####oberwalem")
                    objectO = self.findChild(QWidget, "user")
                    objectO.close()

        self.game[self.positiony][self.positionx]='.'
        self.click_bomb=0
        self.bomb.setGeometry(QtCore.QRect(-self.positionx * 21, -self.positiony * 21, 21, 21))
        self.send(self.game)
        self.timer.stop()



    def keyPressEvent(self, e):
        if(Player1.killed()==False):
            if e.key() == Qt.Key_W:
                positionx, positiony = Player1.get_position()
                if (positiony-1 >= 0):
                    nextPosition=self.game[positiony-1][positionx]
                    if (nextPosition == '.' ):
                        self.game[positiony][positionx] = '.'
                        Player1.move('w')
                        self.game[Player1.y][Player1.x] = 'A'
                        print('------------------')
                        # print_board(self.game)
                        self.send(self.game)
                        self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))

            if e.key() == Qt.Key_S:
                positionx, positiony = Player1.get_position()
                if(positiony + 1<=dimension-1):
                    nextPosition=self.game[positiony+1][positionx]
                    if(nextPosition=='.'):
                        self.game[positiony][positionx] = '.'
                        Player1.move('s')
                        self.game[Player1.y][Player1.x] = 'A'
                        print('------------------')
                        # print_board(self.game)
                        self.send(self.game)
                        self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))

            if e.key() == Qt.Key_A:
                positionx, positiony = Player1.get_position()
                if (positionx-1 >= 0):
                    nextPosition=self.game[positiony][positionx-1]
                    if (nextPosition == '.'):
                        self.game[positiony][positionx] = '.'
                        Player1.move('a')
                        self.game[Player1.y][Player1.x] = 'A'
                        print('------------------')
                        # print_board(self.game)
                        self.send(self.game)
                        self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))
            # print(e.key())

            if e.key() == Qt.Key_D:
                positionx, positiony = Player1.get_position()
                if (positionx+1 < dimension):
                    nextPosition=self.game[positiony][positionx+1]
                    if (nextPosition == '.' ):
                        self.game[positiony][positionx]='.'
                        Player1.move('d')
                        self.game[Player1.y][Player1.x] = 'A'
                        print('------------------')
                        # print_board(self.game)
                        self.send(self.game)
                        self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))

            if e.key() == Qt.Key_Escape:
                # bomb
                # print('hello')
                if(self.click_bomb==0):
                    self.click_bomb=1
                    self.positionx, self.positiony = Player1.get_position()

                    self.bomb.setGeometry(QtCore.QRect(self.positionx * 21, self.positiony * 21, 21, 21))
                    self.B = Bomb(self.positionx,self.positiony,1)
                    # print(self.B.char)
                    # print(self.positionx, self.positiony)
                    self.game[self.positiony][self.positionx] = self.B.char
                    self.explX,self.explY=self.B.explode()


                    self.timer = QtCore.QTimer()
                    self.timer.timeout.connect(self.update)
                    self.timer.start(2000)
                    self.var= 'b'
                    self.timer.timeout.connect(self.destroy_by_bom)

                    self.send(self.game)





        # if e.key() == Qt.Key_Escape:
        #     self.close()



import icon_rc
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())



