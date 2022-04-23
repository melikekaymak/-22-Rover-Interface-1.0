#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QWidget,QApplication,QFrame,QLabel,QVBoxLayout,QPushButton,QButtonGroup,QHBoxLayout,QScrollArea,QGridLayout,QSizePolicy
from PyQt5.QtGui import QPixmap,QPalette,QColor
from PyQt5.QtCore import QSize,Qt,QEvent,QRect
from fetch_record import fetcher

class backend(QWidget):

    def __init__(self):
        super(backend,self).__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        #self.horizontalLayout.setGeometry(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))
        self.scrolll = QScrollArea(self)
        self.scrolll.setWidgetResizable(True)
        self.scrolll.setObjectName("scroll")
        self.scrollWidgetContents = QWidget()
        # self.scrollWidgetContents.setGeometry(QRect(0, 0, 801, 717))
        self.scrollWidgetContents.setObjectName("scrollWidgetContents")
        self.gridLayout = QGridLayout(self.scrollWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.scrolll.setWidget(self.scrollWidgetContents)
        self.horizontalLayout.addWidget(self.scrolll)


        data=fetcher()
        data=data.fetch()


        #VARIABLES 
        self.no=0
        count=0
        count_2=0
        row=0

        #LIST FOR ITEMS
        self.labels= []
        self.rock_names=[]
        list=[]


        
        #CREATING ROW AND COLUMN NUMBERS
        for x in data:
            for col in range(0,2):
                count+=1
                if count>len(data):
                    break
                list.append([row,col])
            row+=1
        
        
        #CREATING FRAMES
        for rock in data:
            self.create_frame(list[count_2][0],list[count_2][1],rock.name,rock.description)
            self.rock_names.append(rock.name)
            count_2+=1

    #FUNCTION TO CREATE FRAMES
    def create_frame(self,row,column,name,description):
        
        self.no = 2*row + column

        self.frame = QFrame(self.scrollWidgetContents)
        self.frame.setMinimumSize(QSize(500, 500))
        self.frame.setMaximumSize(QSize(500, 500))
        self.frame.setStyleSheet("QFrame#frame{background-color: rgb(0, 0, 0); \n border-radius:50px; \n padding :15px;}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame_{}".format(self.no))
        
        self.gridLayout.setSpacing(20)

        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")

        self.image_label = QLabel(self.frame)
        self.image_label.setObjectName("image_label{}_{}".format(row,column))
        self.image_label.setMinimumSize(QSize(100,100))
        self.image_label.setAlignment(Qt.AlignVCenter|Qt.AlignCenter)
        self.image_label.setPixmap(QPixmap('/home/melikenur/proje2_ws/images/{}/{}_1.png'.format(name,name)))
        self.image_label.setScaledContents(True)
        self.verticalLayout.addWidget(self.image_label)
        pos=self.frame.geometry().center()

        self.button_first=QPushButton(self.frame)
        self.button_first.setGeometry(pos.x()-30,pos.y(),20,20)
        self.button_first.setToolTip('{}'.format(self.no))
        self.button_first.clicked.connect(lambda:self.image_slide(name))
        
        self.button_second=QPushButton(self.frame)
        self.button_second.setGeometry(pos.x()+10,pos.y(),20,20)
        self.button_second.setToolTip('{}'.format(self.no))

        self.button_second.clicked.connect(lambda:self.image_slide_2(name))

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.label_2.setText(name)
        self.verticalLayout.addWidget(self.label_2)
        
        self.label_3 = QLabel(self.frame)
        #LIST FOR ITEMS
        self.labels= []
        self.rock_names=[]
        self.label_3.setObjectName("label_3")
        self.label_3.setText(description)
        self.verticalLayout.addWidget(self.label_3)
        
        self.verticalLayout.setStretch(0, 6)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 3)
        self.gridLayout.addWidget(self.frame, row, column, 1, 1)

        self.labels.append(self.findChild(QLabel,'image_label{}_{}'.format(row,column)))
        print(self.labels)

    def image_slide(self,image):
        sender=int(self.sender().toolTip())
        self.labels[sender].setPixmap(QPixmap('/home/melikenur/proje2_ws/images/{}/{}_1.png'.format(image,image)))


    def image_slide_2(self,image):
        sender=int(self.sender().toolTip())
        self.labels[sender].setPixmap(QPixmap('/home/melikenur/proje2_ws/images/{}/{}_2.png'.format(image,image)))




def run():
    app=QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)    
    app.setPalette(palette)
    win=backend()
    win.show()
    sys.exit(app.exec_())

run()
