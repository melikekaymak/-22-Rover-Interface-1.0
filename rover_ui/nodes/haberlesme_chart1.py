#!/usr/bin/env python2.7
# -- coding: utf-8 --

import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QHBoxLayout,QFrame,QVBoxLayout,QLabel,QGridLayout,QScrollArea,QWidget
from PyQt5.QtCore import QTimer,QRect
from PyQt5.QtGui import QFont
from kanvas_class import MplCanvas
#import pandas as pd
import csv

class HabWindow(QFrame):

    x=[]
    y=[]
    temp_ave=[]
    sum=0
    counter=0

    def __init__(self, *args, **kwargs):
        super(HabWindow, self).__init__(*args, **kwargs)

        # self.resize(700,200)
        self.font=QFont()
        self.font.setBold(True)
        self.font.setFamily('Roboto')
        self.font.setPointSize(20)

        #SET MAİN WİNDOW LAYOUT
        self.main_layout=QHBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.main_layout)
        
        #CREATE SCROLLAREA
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scroll_layout=QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setLayout(self.scroll_layout)
        self.scrollArea.setContentsMargins(0,0,0,0)
        
        self.container_frame=QFrame(self.scrollAreaWidgetContents)
        self.container_layout=QHBoxLayout(self.container_frame)
        self.canvas = MplCanvas(self.container_frame, width=7, height=2, dpi=100)
        self.canvas.setContentsMargins(0,0,0,0)
        
        # self.frame=QFrame(self.container_frame)
        # self.layout_2=QVBoxLayout(self.frame)
        # self.label=QLabel(self.frame)
        # self.label.setFont(self.font)
        # self.label_2=QLabel(self.frame)
        # self.label_2.setFont(self.font)
        # self.layout_2.addWidget(self.label)
        # self.layout_2.addWidget(self.label_2)
    
        
        self.container_layout.addWidget(self.canvas)
        #self.container_layout.addWidget(self.frame)
        #self.container_layout.setStretch(0,8)
        #self.container_layout.setStretch(1,2)
        self.main_layout.addWidget(self.scrollArea)
        
        self.values=[]
        with open('/home/melikenur/proje2_ws/src/rover_ui/nodes/110-tavg-1-12-1895-2021.csv','r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            next(lines)
            for row in lines:
                self.values.append(int(float(row[1])))

        # self.data=pd.read_csv("110-tavg-1-12-1895-2021.csv")
        # self.value=self.data['Value']

        self.update_plot()
        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QTimer()
        self.timer.setInterval(700)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        if self.counter==126:
            self.timer.stop()
        self.y.append(self.values[self.counter])
        self.x.append(self.counter)
        self.sum=self.sum+self.values[self.counter]
        ave=self.sum/(self.counter+1)
        self.temp_ave.append(ave)
        #self.label.setText("Temp:{}".format(self.values[self.counter]))
        #self.label_2.setText("Ave:{}".format(round(ave)))
        # Drop off the first y element, append a new one.
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.x, self.y,label='temperature')
        self.canvas.axes.plot(self.temp_ave,label='average')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()
        self.counter+=1
