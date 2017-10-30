# coding : utf-8

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter,QColor,QPen,QFont
from PyQt5.QtCore import Qt,QTimer

class iwork(QWidget):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.r = 15 #R 30px
        self.v = 1 #
        self.dirc_x = 1 #x - direction 1 or -1
        self.dirc_y = 1
        self.initUI()

    def initUI(self):
        self.resize(600,400) #set 600 X 400
        self.setWindowTitle("HomeWork")
        self.setStyleSheet('background-color:#FFF;') # set background-color white
        self.show()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.setInterval(30)
        self.timer.start()


    def paintEvent(self, event):
        self.qp = QPainter(self)
        self.qp.setBrush(Qt.red)
        self.qp.setPen((Qt.red))
        # a 30px red circle on top-left
        self.qp.drawEllipse(self.x, self.y, self.r, self.r)
        self.qp.end()


    def animate(self):
        #self.dirc = random.choice([-1,1])
        self.checkCollision()
        self.x += (self.v * self.dirc_x)
        self.y += (self.v * self.dirc_y)
        #print(self.dirc)

        self.update()



    def checkCollision(self):
        limit_x = self.width()-self.r
        limit_y = self.height()-self.r
        #print(self.size())
        if self.y + self.v > limit_y:
            self.dirc_y = -1
            #self.dirc_x = (self.dirc_x)
            return
        if self.x  - self.v  < 0:
            self.dirc_x = 1
            #self.dirc_y = self.dirc_y
            return
        if self.y -self.v <0:
            self.dirc_y = 1
            #self.dirc_x = self.dirc_x
            return
        if self.x +self.v > limit_x:
            self.dirc_x = -1
            #self.dirc_y = self.dirc_y
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = iwork()
    sys.exit(app.exec_())
