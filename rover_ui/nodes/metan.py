#!/usr/bin/env python2.7
# -- coding: utf-8 --

import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QHBoxLayout,QFrame,QVBoxLayout,QLabel,QGridLayout,QScrollArea,QWidget
from PyQt5.QtCore import QTimer,QRect
from PyQt5.QtGui import QFont
# from main import MainWindow
from kanvas_class import MplCanvas
from std_msgs.msg import Float64
#import pandas as pd
import csv
import rospy
import numpy as np
import random

class metan(QFrame):

    x=[]
    y=[]
    temp_ave=[]
    sum=0
    counter=0

    def __init__(self,widget):
        super(metan, self).__init__()
        
        #Rate = rospy.Rate(10)
        self.setMinimumSize(561,422)


        # self.resize(1200, 900)
        self.font=QFont()
        self.font.setBold(True)
        self.font.setFamily('Roboto')
        self.font.setPointSize(20)
        #GET THE args
        # print(data.toolTip())
        # if data.toolTip()!="":
        #     self.data=int(data.toolTip())   
        # else:
        #     self.data = 0
        #rospy.Subscriber('/sensor_Basinc',Float64,self.sicaklik_cb)



        self.container_layout=QHBoxLayout(self)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        
        self.frame=QFrame(self)
        self.layout_2=QVBoxLayout(self.frame)
        self.label=QLabel(self.frame)
        self.label.setFont(self.font)
        self.label_2=QLabel(self.frame)
        self.label_2.setFont(self.font)
        self.layout_2.addWidget(self.label)
        self.layout_2.addWidget(self.label_2)
    
        
        self.container_layout.addWidget(self.canvas)
        self.container_layout.addWidget(self.frame)
        self.container_layout.setStretch(0,8)
        self.container_layout.setStretch(1,2)
        # self.main_layout.addWidget(self.scrollArea)
        
        # self.values=[]
        # with open('/home/melikenur/proje2_ws/src/rover_ui/nodes/110-tavg-1-12-1895-2021.csv','r') as csvfile:
        #     lines = csv.reader(csvfile, delimiter=',')
        #     next(lines)
        #     for row in lines:
        #         self.values.append(int(float(row[1])))

        self.update_plot()
        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.metan_cb)
        self.timer.start()
        #Rate.sleep()
    def metan_cb(self):
        data=random.uniform(5.5, 6.02)
        if data is not None:
            self.y.append(data)
            self.x.append(self.counter)
            self.sum=self.sum+data
            ave=self.sum/(self.counter+1)+.1
            self.temp_ave.append(ave)
            self.label.setText("Methane:{}".format(data))
            self.label_2.setText("Ave:{}".format(round(ave)))
            # Drop off the first y element, append a new one.
            self.canvas.axes.cla()  # Clear the canvas.
            self.canvas.axes.plot(range(len(self.y)),self.y,label='temperature')
            self.canvas.axes.plot(range(len(self.y)),self.temp_ave,label='average')
            # Trigger the canvas to update and redraw.
            self.canvas.draw()
            self.counter+=1

    def update_plot(self):
        # if self.counter==126:
        #     self.timer.stop()
        pass