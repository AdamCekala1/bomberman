# w self.game jest [Y][X]

# ****************************************************** znajdowanie i zamykanie klocka o x=5 y=5
# objectO = self.findChild(QWidget, "wall_type1_5_5");
# objectO.close()
# *************************************************************************************
# *************************************************************************************


import sys
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import threading
import jsonpickle
import json
import io

import threading
import wnoGame
from PyQt5.QtCore import Qt, QBasicTimer
from wnoGame import *
dimension=40
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.create_socket()
        self.initUI()
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.repaint()
        else:
            super.timerEvent(event)



    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.repaint()
        else:
            super.timerEvent(event)

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

        return self.labels


    def initUI(self):
        self.setGeometry(100, 100, 994, 905)
        self.setWindowTitle('BombermanServ')

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

        # enemies - bots
        for i in range (0,5,1):
            print(i)
            x=Monsters[i].x
            y=Monsters[i].y
            print(x)
            print(y)
            self.monster = QtWidgets.QPushButton(self.frame)
            self.monster.setGeometry(QtCore.QRect(x*21, y*21, 21, 21))
            self.monster.setText("")
            icon1 = QtGui.QIcon()
            if(Monsters[i].power==1):
                icon1.addPixmap(QtGui.QPixmap(":/soldier.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            else:
                icon1.addPixmap(QtGui.QPixmap(":/thief.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.monster.setIcon(icon1)
            self.monster.setIconSize(QtCore.QSize(21, 21))
            self.monster.setObjectName("Monster"+str(Monsters[i].number))
            print("Monster"+str(Monsters[i].number))



        self.show()



    # ///////////////////////////////////////////////




    def recieve(self, socket):
        while True:
            resp = self.clientsocket.recv(80000).decode('utf-8')
            map = jsonpickle.decode(resp)
            self.prevMap = self.game
            self.game = map
            for i in range(0,dimension,1):
                for j in range(0,dimension,1):
                    if(self.game[i][j]!= self.prevMap[i][j]):
                        if(self.prevMap[i][j]=="0"):
                            objectO = self.findChild(QWidget, "wall_type1_" + str(i) + "_" + str(j))
                            objectO.close()
                        if (self.prevMap[i][j] == "M" or self.prevMap[i][j] == "N"):
                            for Monster in Monsters:
                                if Monster.x == j:
                                    print("i found it!")
                                    objectOMonster = self.findChild(QWidget, "Monster" + str(Monster.number))
                                    print("Monster" + str(Monster.number))
                                    objectOMonster.close()
                            # objectO = self.findChild(QWidget, "wall_type1_" + str(i) + "_" + str(j))
                        if (self.game[i][j] == "!"):
                            self.bomb.setGeometry(QtCore.QRect(j * 21, i * 21, 21, 21))
                        if (self.prevMap[i][j] == "!" and self.game[i][j] == "."):
                            print("znikam")
                            self.bomb.setGeometry(QtCore.QRect(-j * 21, -i * 21, 21, 21))


            # print_board(self.game)
            print("otrzymalem")
            # self.send(self.game)
            with io.open('data.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(self.game, ensure_ascii=False))
            self.repaint()

    def send(self, map):
        self.clientsocket.send(jsonpickle.encode(map).encode('utf-8'))

    def create_socket(self):
        print("test")
        self.game=board;
        # create an INET, STREAMing socket
        serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host,
        # and a well-known port
        serversocket.bind((socket.gethostname(), 8070))
        print(socket.gethostname())
        # become a server socket
        serversocket.listen(5)
        #while True:
        (self.clientsocket, address) = serversocket.accept()
        print("hi ", address)
        self.clientsocket.send(jsonpickle.encode(self.game).encode('utf-8'))
        threading.Thread(target = self.recieve, args = (self.clientsocket,)).start()



    # ///////////////////////////////////////////////





import icon_rc
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())





                # if e.key() == Qt.Key_W:
                #     self.__player.move('Up', self.__game)
                # if e.key() == Qt.Key_S:
                #     self.__player.move('Down', self.__game)
                # if e.key() == Qt.Key_A:
                #     self.__player.move('Left', self.__game)
                # if e.key() == Qt.Key_D:
                #     self.__player.move('Right', self.__game)
                # self.send(self.__player)

