#!/usr/bin/env python2.7
# -- coding: utf-8 --

from PyQt5.QtCore import  pyqtSlot 
from PyQt5.QtWidgets import QApplication, QMainWindow ,QWidget
import sys
from joystick import JoyStick
from joyui import Ui_MainWindow

class Main(QWidget):
    text="(0,0,0,0)"
    msg_1=0
    msg_2=0
    msg_3=0
    msg_4=0


    def __init__(self):
        super(Main,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        #CREATE JOYSTICK OBJECT
        self.joy=JoyStick()
        self.joy_2=JoyStick()
        
        #ADD JOYSTICKS TO LAYOUT
        self.ui.horizontalLayout_2.addWidget(self.joy)
        self.ui.horizontalLayout_2.addWidget(self.joy_2)
        
        #CONNECT TO JOYSTICK SIGNAL
        self.joy.signal.connect(self.on_change)
        self.joy_2.signal.connect(self.on_change_2)

        #GIVE FIRST POSITION TO JOYSTICK
        self.ui.label.setText(self.text)


        
    #UPDATE JOYSTICK POSITION
    @pyqtSlot(float,float)
    def on_change(self,msg_1,msg_2):
        self.msg_1=msg_1
        self.msg_2=msg_2
        self.text="({msg_1},{msg_2},0,0)".format(msg_1=round(self.msg_1,2),msg_2=round(self.msg_2,2))
        self.ui.label.setText(self.text)

    #UPDATE JOYSTICK POSITION
    @pyqtSlot(float,float)
    def on_change_2(self,msg_3,msg_4):
        self.msg_3=msg_3
        self.msg_4=msg_4
        self.text="(0,0,{msg_3},{msg_4})".format(msg_3=round(self.msg_3,2),msg_4=round(self.msg_4,2))
        self.ui.label.setText(self.text)





if __name__=="__main__":
    app=QApplication(sys.argv)
    win=Main()
    win.show()
    sys.exit(app.exec_())