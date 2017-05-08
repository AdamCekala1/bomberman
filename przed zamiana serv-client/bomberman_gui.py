# w board jest [Y][X]

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
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)
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

    def paintEvent(self, *args, **kwargs):
        try:

            print("refresh")
            # print(str(self.game[3][3]) == str(Player1.char))
            for i in range(0, dimension):
                for j in range(0, dimension):
                    if (str(board[i][j]) == str(Player1.char)):
                        if(Player1):
                            # Player1.set_position((i,j))
                            print(i)
                            print(Player1.x)
                            print(j)
                            print(Player1.y)
                            self.user.setGeometry(QtCore.QRect(j * 21, i * 21, 21, 21))

        except:
            pass
    def initMap(self):
        self.labels = []
        for i in range(0, dimension):
            for j in range(0, dimension):
                if (board[i][j] == '#'):
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
                if (board[i][j] == '0'):
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
        self.setWindowTitle('Event handler')

        self.setStyleSheet("QWidget{\n"
                                 " background-color:#2980b9;\n"
                                 "}\n"
                                 "QFrame{\n"
                                 "background-color:#ecf0f1;\n"
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
        # walls_to_use
        # self.labels=[]
        # for i in range(0, dimension):
        #     for j in range(0, dimension):
        #         if (board[i][j] == '#'):
        #             self.wall_type2 = QtWidgets.QPushButton(self.frame)
        #             self.wall_type2.setGeometry(QtCore.QRect(j * 21, i * 21, 21, 21))
        #             self.wall_type2.setText("")
        #             icon3 = QtGui.QIcon()
        #             icon3.addPixmap(QtGui.QPixmap(":/wall2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #             self.wall_type2.setIcon(icon3)
        #             self.wall_type2.setIconSize(QtCore.QSize(21, 21))
        #             self.wall_type2.setObjectName("wall_type2_" + str(i) + '_' + str(j))
        #             self.labels.append(self.wall_type2)
        #             # print(self.wall_type2.objectName())
        #         if (board[i][j] == '0'):
        #             self.wall_type1 = QtWidgets.QPushButton(self.frame)
        #             self.wall_type1.setGeometry(QtCore.QRect(j * 21, i * 21, 21, 21))
        #             self.wall_type1.setText("")
        #             icon2 = QtGui.QIcon()
        #             icon2.addPixmap(QtGui.QPixmap(":/wall1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #             self.wall_type1.setIcon(icon2)
        #             self.wall_type1.setIconSize(QtCore.QSize(21, 21))
        #             self.wall_type1.setObjectName("wall_type1_" + str(i) + '_' + str(j))
        #             self.labels.append(self.wall_type1)

        # enemy = QtWidgets.QPushButton(self.frame)
        # enemy.setGeometry(QtCore.QRect(i * 21 + 21, j * 21 + 21, 21, 21))
        # enemy.setText("")
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(":/enemy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # enemy.setIcon(icon)
        # enemy.setIconSize(QtCore.QSize(21, 21))
        # enemy.setObjectName("enemy")
        # enemyList.append(enemy)




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

    def destroy_by_bom(self):
        # print(self.explX)
        for i in self.explX:
            # print('Punkt:'+str(i)+"_"+str(self.positiony))
            if(board[self.positiony][i]=='0'):
                board[self.positiony][i] = '.'
                objectO = self.findChild(QWidget, "wall_type1_"+str(self.positiony)+"_"+str(i))
                objectO.close()
        for i in self.explY:
            if (board[i][self.positionx] == '0'):
                board[i][self.positionx] = '.'
                objectO = self.findChild(QWidget, "wall_type1_"+str(i)+"_"+str(self.positionx))
                objectO.close()
        self.send(board)
        self.timer.stop()


    # ///////////////////////////////////////////////

    def recieve(self, socket):
        while True:
            resp = socket.recv(128).decode('utf-8')
            print(resp)
            print_board(resp)
            print("true")

    def send(self, map):
        self.clientsocket.send(jsonpickle.encode(map).encode('utf-8'))


    def create_socket(self):
        print("test")
        self.__game="truea";
        # create an INET, STREAMing socket
        serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host,
        # and a well-known port
        serversocket.bind((socket.gethostname(), 8000))
        print(socket.gethostname())
        # become a server socket
        serversocket.listen(5)
        #while True:
        (self.clientsocket, address) = serversocket.accept()
        print("hi ", address)
        self.clientsocket.send(jsonpickle.encode(board).encode('utf-8'))
        threading.Thread(target = self.recieve, args = (self.clientsocket,)).start()

    # def connect_to_socket(self):
    #     clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     clientsocket.connect(('Czarek', 8080))
    #     resp = clientsocket.recv(4048).decode('utf-8')
    #     game = jsonpickle.decode(resp)



    # ///////////////////////////////////////////////




    def keyPressEvent(self, e):

        if e.key() == Qt.Key_W:
            positionx, positiony = Player1.get_position()
            if (positiony-1 >= 0):
                nextPosition=board[positiony-1][positionx];
                if (nextPosition == '.' ):
                    Player1.move('w')
                    print('------------------')
                    print_board(board)
                    self.send(board)
                    self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))

        if e.key() == Qt.Key_S:
            positionx, positiony = Player1.get_position()
            if(positiony + 1<=dimension-1):
                nextPosition=board[positiony+1][positionx]
                if(nextPosition=='.'):
                    Player1.move('s')
                    print('------------------')
                    print_board(board)
                    self.send(board)
                    self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))

        if e.key() == Qt.Key_A:
            positionx, positiony = Player1.get_position()
            if (positionx-1 >= 0):
                nextPosition=board[positiony][positionx-1]
                if (nextPosition == '.'):
                    Player1.move('a')
                    print('------------------')
                    print_board(board)
                    self.send(board)
                    self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))
        # print(e.key())

        if e.key() == Qt.Key_D:
            positionx, positiony = Player1.get_position()
            if (positionx+1 < dimension):
                nextPosition=board[positiony][positionx+1]
                if (nextPosition == '.' ):
                    Player1.move('d')
                    print('------------------')
                    print_board(board)
                    self.send(board)
                    self.user.setGeometry(QtCore.QRect(Player1.x * 21, Player1.y * 21, 21, 21))

        if e.key() == Qt.Key_Escape:
            # bomb
            # print('hello')

            self.positionx, self.positiony = Player1.get_position()

            self.bomb.setGeometry(QtCore.QRect(self.positionx * 21, self.positiony * 21, 21, 21))
            self.B = Bomb(self.positionx,self.positiony,1)
            # print(self.B.char)
            # print(self.positionx, self.positiony)
            board[self.positiony][self.positionx] = self.B.char
            self.explX,self.explY=self.B.explode()


            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update)
            self.timer.start(2000)
            self.var= 'b'
            self.timer.timeout.connect(self.destroy_by_bom)
            self.send(board)




        # if e.key() == Qt.Key_Escape:
        #     self.close()



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

