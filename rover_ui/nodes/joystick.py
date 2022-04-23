#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from PyQt5.QtCore import  QPointF, QTimer,  Qt ,pyqtSignal
from PyQt5.QtGui import  QPainter, QPen
from PyQt5.QtWidgets import QFrame, QApplication, QLabel,QWidget
import sys
import rospy
from sensor_msgs.msg import Joy

class JoyStick(QLabel):
    
    signal=pyqtSignal(float,float)

    def __init__(self):
        super(JoyStick,self).__init__()
        self.setMinimumSize(150,150)
        self.setMaximumSize(150,150)
        self.x=self.width()/2
        self.y=self.height()/2
        self.relative_x=0
        self.relative_y=0
        self.setStyleSheet("border-radius:100px;")

        #REMOVE WINDOW FLAG AND MAKE BACKGROUND TRANSLUCENT
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
    
    #SUBSCRIBE TO JOY NODE
    def sub(self):
        self.node=rospy.init_node("listen",anonymous=True)
        rospy.Subscriber('/joy',Joy,self.joyControl)

    #TAKE LOCATION INFO FROM NODE AND GIVE POSITION TO VIRTUAL JOYSTICK
    def joyControl(self,data):
        self.data=data.axes
        self.x=(-(self.data[0]*100)+100)
        self.y=(-(self.data[1]*100)+100)
        # print(self.data[0],self.data[1])
        self.repaint()

    #DRAW VIRTUAL JOYSTICK
    def paintEvent(self,event):
        pen=QPen()
        pen.setWidth(5)
        pen.setBrush(Qt.black)
        painter=QPainter(self)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawEllipse(5,5,140,140)
        # print(self.rect())
        
        painter_2=QPainter(self)
        painter_2.setBrush(Qt.black)
        painter_2.setRenderHint(QPainter.Antialiasing)
        painter_2.drawEllipse(QPointF(self.x,self.y),25,25)

    #TAKE MOUSE LOCATION AND REPAINT JOYSTICK     
    def mouseMoveEvent(self,e):
        self.relative_x=(e.x()-100)/100.0
        self.relative_y=(e.y()-100)/100.0  
        # print(round(self.relative_x,2),round(self.relative_y,2))
        if self.relative_x**2+self.relative_y**2<1: 
            self.signal.emit(self.relative_x,self.relative_y)
            self.x=e.x()
            self.y=e.y()
            self.repaint()
    
    #TAKE MOUSE LOCATION AND REPAINT JOYSTICK     
    def mousePressEvent(self,e):
        if self.relative_x**2+self.relative_y**2<1:  
            self.x=e.x()
            self.y=e.y()
            self.repaint()

    #TAKE MOUSE LOCATION AND REPAINT JOYSTICK     
    def mouseReleaseEvent(self,e):
        self.x=self.width()/2
        self.y=self.height()/2
        self.repaint()
    


if __name__=="__main__":
    app=QApplication(sys.argv)
    win=JoyStick()
    win.show()
    sys.exit(app.exec_())


    