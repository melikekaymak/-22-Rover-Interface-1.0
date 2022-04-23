#!/usr/bin/env python2.7
# -- coding: utf-8 --


import sys


from PyQt5.QtCore import*
from PyQt5.QtGui import*
from PyQt5.QtWidgets import *
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64MultiArray, Bool,String, Float64
from sensor_msgs.msg import Image, Imu, BatteryState, NavSatFix
from geometry_msgs.msg import TwistStamped
from mavros_msgs.msg import State
import math
import cv2
import rospy
from cv_bridge import CvBridge
from tf.transformations import euler_from_quaternion
import random
from interface import *
#from sicaklik import * 
from joystick import JoyStick
from tekerlekkkk import paint
import pyautogui 
import time


class MainWindow(QMainWindow):
    text="(0,0,0,0)"
    msg_1=0
    msg_2=0
    msg_3=0
    msg_4=0 
  
    signal=pyqtSignal(String)
    gallery_signal=pyqtSignal(int)
    sicaklik_sensor_signal=pyqtSignal(int)

    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.subscriber()

        

        self.ui.j_1.signal.connect(self.on_change)
        self.ui.j_2.signal.connect(self.on_change_2)


        #GALLERY DEFAULT LAYOUT SETTİNGS
        self.horizontal = QHBoxLayout(self.ui.gallery_page)
        self.horizontal.setObjectName("horizontal")
        
        self.scroll_gallery = QScrollArea(self)
        self.scroll_gallery.setWidgetResizable(True)
        self.scroll_gallery.setObjectName("scroll_gallery")
        self.scrollwidget_gallery = QWidget()
        
        self.scrollwidget_gallery.setObjectName("scrollwidget_gallery")
        self.grid = QGridLayout(self.scrollwidget_gallery)
        self.grid.setObjectName("grid")
        self.scroll_gallery.setWidget(self.scrollwidget_gallery)
        self.horizontal.addWidget(self.scroll_gallery)

        #Start QTimer
        # self.timer = QTimer()
        # self.timer.setInterval(150)
        # self.timer.timeout.connect(self.create_random)
        # self.timer.start()
        
        #Matched Rocks Scroll
        self.scroll_layout=QVBoxLayout(self.ui.scrollAreaWidgetContents)
        self.ui.scrollArea.setWidgetResizable(True)

        
        self.publisher = rospy.Publisher("/classification_flag",Bool,queue_size=10)
        self.ui.label_32.setMaximumSize(686,603)
        self.ui.label_32.setScaledContents(True)
        
        self.ui.label_33.setScaledContents(True)
        self.ui.label_33.setMaximumSize(686,603)

        # Creat a button for the artificial intelligence page 
        self.cam_button=QPushButton(self.ui.ai_page)
        self.x=self.ui.label_32.x()
        self.y=self.ui.label_32.y()
        self.cam_button.setStyleSheet("background-color: rgb(239, 41, 41); border-radius:25px;")
        self.cam_button.setGeometry(self.x+275,self.y+510,50,50)
        self.foto_counter = 0
        
    
        
        
        
        # Main body buttons match to pages 
        self.ui.drive_system_button.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.drive_system_page))
        self.ui.rocks_button.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.rocks_page))
        self.ui.sensor_button.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensor_page))
        self.ui.spectrometer_button.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.spectrometer_page))
        self.ui.biochemistry_button.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.biochemistry_page))
        self.ui.drone_button.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.drone_page))
        self.ui.robotic_arm_button.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.robotik_arm_page))
        self.ui.rviz_button.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.rviz_page))
        self.ui.qgraund_button.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.qground_page))        
        self.ui.igneous_button.clicked.connect(lambda:self.ui.stackedWidget_2.setCurrentWidget(self.ui))
        self.ui.sedimentary_button.clicked.connect(lambda:self.ui.stackedWidget_2.setCurrentWidget(self.ui))
        self.ui.metamorphic_button.clicked.connect(lambda:self.ui.stackedWidget_2.setCurrentWidget(self.ui))
        self.ui.ai_button.clicked.connect(lambda:self.ui.stackedWidget_2.setCurrentWidget(self.ui.ai_page))
        self.ui.gallery_button.clicked.connect(lambda:self.ui.stackedWidget_2.setCurrentWidget(self.ui.gallery_page))
        self.ui.metamorphic_button.clicked.connect(lambda:self.ui.stackedWidget_2.setCurrentWidget(self.ui.rocks_page_2))
        # self.ui.raman_button.clicked.connect(lambda:self.ui.spectrometer_stackedWidget.setCurrentWidget(self.ui.page_raman))
        # self.ui.visible_button.clicked.connect(lambda:self.ui.spectrometer_stackedWidget.setCurrentWidget(self.ui.page_visible))
        self.ui.terminal.clicked.connect(self.terminal)


        
        self.signal.connect(self.monitoringSlot)
        self.gallery_signal.connect(self.create_gallery)
        self.cam_button.clicked.connect(self.send_flag_for_rock)
    


        
    # Subscriber function
    def subscriber(self):
        
        rospy.Subscriber('/lio_sam/mapping/odometry',Odometry,self.odomback)
        rospy.Subscriber('/drive_system/wheel_speed',Float64MultiArray,self.encoder_speed)
        rospy.Subscriber('/drive_system/encoder/angle_degree',Float64MultiArray,self.encoder_angle)
        rospy.Subscriber('/camera/image_raw', Image,self.camback)
        rospy.Subscriber('/imu2/data', Imu,self.imu)
        rospy.Subscriber('classification_result',String,self.show_rock)
        rospy.Subscriber('/mavros/battery',BatteryState,self.drone_battery)
        rospy.Subscriber('/mavros/altitude',NavSatFix,self.drone_altitude)
        rospy.Subscriber('/mavros/global_position/global',NavSatFix,self.drone_gps)
        rospy.Subscriber('/mavros/local_position/velocity_body',TwistStamped,self.drone_linear_velocity)
        rospy.Subscriber('/mavros/state',State,self.drone_state)
        rospy.Subscriber('/communication',Float64MultiArray, self.communicationback)

        self.bridge= CvBridge()
    
    def communicationback (self,data):
        self.ui.haberleme_1.setText(data.data.freq)
        self.ui.haberleme_2.setText(data.data.signal)
        
    def drone_battery (self,data):
        self.ui.drone_battery.setNum('')

    def drone_altitude(self,data):
        self.ui.drone_height.setNum(data.monotonic)

    def drone_gps(self,data):
        self.ui.drone_enlem.setNum(data.latitude)
        self.ui.drone_boylam.setNum(data.longitude)

    def drone_linear_velocity(self,data):
        self.x = data.twist.linear.x
        self.y = data.twist.linear.y
        self.z = data.twist.linear.z
        self.velocity = math.sqrt((math.sqrt(self.x**2+self.y**2))**2+self.z**2)

    def drone_state (self,data):
        self.ui.status_indicator.setText(data.mode)
    
    def terminal(self):
        pyautogui.hotkey("ctrl", "alt", "t")
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "shift", "o")
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "shift", "e")
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "shift", "e")
        time.sleep(0.2)
        pyautogui.hotkey("alt","left")
        time.sleep(0.2)
        pyautogui.hotkey("alt","left")
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "shift", "e")
        time.sleep(0.2)
        pyautogui.hotkey("alt","up")
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "shift", "e")
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "shift", "e")
        time.sleep(0.2)
        pyautogui.hotkey("alt","left")
        time.sleep(0.2)
        pyautogui.hotkey("alt","left")
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "shift", "e")
    
    def show_rock(self,data):
        self.signal.emit(data)
    
    @pyqtSlot(float,float)
    def on_change(self,msg_1,msg_2):
        self.msg_1=msg_1
        self.msg_2=msg_2
        self.text="({msg_1},{msg_2},0,0)".format(msg_1=round(self.msg_1,2),msg_2=round(self.msg_2,2))
        self.ui.label_61.setText(self.text)
        print(self.text)

    @pyqtSlot(float,float)
    def on_change_2(self,msg_3,msg_4):
        self.msg_3=msg_3
        self.msg_4=msg_4
        self.text="(0,0,{msg_3},{msg_4})".format(msg_3=round(self.msg_3,2),msg_4=round(self.msg_4,2))
        self.ui.label_61.setText(self.text)
        print(self.text)

        

    
    @pyqtSlot(String)   
    def monitoringSlot(self,data):
        count=0
        for x in range(3):
            if self.findChild(QFrame,'frame'+str(x)) is not None:
                x=self.findChild(QFrame,'frame'+str(x))
                print(x)
                x.deleteLater()
        q=data.data.split(',')
        for x in q:
            rock,sml=x.split(':')
            sml=100*float(sml)
            self.result_frame=QFrame(self.ui.scrollAreaWidgetContents)
            self.result_frame.setMinimumSize(200,300)
            self.result_frame.setObjectName('frame'+str(count))
            self.horizontal = QHBoxLayout(self.ui.gallery_page)
            self.horizontal.setObjectName("horizontal")
            #self.horizontalLayout.setGeometry(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))
            self.scroll_gallery = QScrollArea(self)
            self.scroll_gallery.setWidgetResizable(True)
            self.scroll_gallery.setObjectName("scroll_gallery")
            self.scrollwidget_gallery = QWidget()
            # self.scrollwidget_gallery.setGeometry(QRect(0, 0, 801, 717))
            self.scrollwidget_gallery.setObjectName("scrollwidget_gallery")
            self.grid = QGridLayout(self.scrollwidget_gallery)
            self.grid.setObjectName("grid")
            self.scroll_gallery.setWidget(self.scrollwidget_gallery)
            self.horizontal.addWidget(self.scroll_gallery)
            self.result_layout=QVBoxLayout(self.result_frame)
            self.labbel=QLabel(self.result_frame)
            self.labbel.setPixmap(QPixmap('./images/{}/{}_1.png'.format(rock,rock)))
            self.labbel.setScaledContents(True)
            self.labbel_2=QLabel(self.result_frame)
            self.labbel_2.setText('%{}'.format(sml))
            self.labbel_3=QLabel(self.result_frame)
            self.labbel_3.setText('{}'.format(rock))
            self.result_layout.addWidget(self.labbel)
            self.result_layout.addWidget(self.labbel_2)
            self.result_layout.addWidget(self.labbel_3)
            self.result_layout.setStretch(0,4)
            self.result_layout.setStretch(1,1)
            self.result_layout.setStretch(2,1)
            self.scroll_layout.addWidget(self.result_frame)
            count+=1

    
    def camback(self, Image):
        self.image = self.bridge.imgmsg_to_cv2(Image,desired_encoding='passthrough')

        # Camera for the AI
        
        ConvertToQtFormat_1 = QImage(self.image.data,self.image.shape[1],
        self.image.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.ui.label_32.setPixmap(QPixmap.fromImage(ConvertToQtFormat_1))
        
        

        

    def odomback(self,data):

        self.ui.linear_x.setNum(data.twist.twist.linear.x)
        self.ui.linear_y.setNum(data.twist.twist.linear.y)

        self.ui.angular_x.setNum(data.twist.twist.angular.x)
        self.ui.angular_y.setNum(data.twist.twist.angular.y)

        self.ui.position_x.setNum(data.pose.pose.position.x)
        self.ui.position_y.setNum(data.pose.pose.position.y)

        self.ui.orientation_x.setNum(data.pose.pose.orientation.x)
        self.ui.orientation_y.setNum(data.pose.pose.orientation.y)
        self.ui.label_22.setNum(data.pose.pose.orientation.w)
    
    
    def encoder_angle(self,data):
        self.ui.angle_1.setNum(round((data.data[0])))
        self.ui.angle_2.setNum(round(data.data[1]))
        self.ui.angle_3.setNum(round((data.data[2])))
        self.ui.angle_4.setNum(round((data.data[3])))
    

    def encoder_speed(self,data):
        self.ui.speed_1.setNum(data.data[0])
        self.ui.speed_2.setNum(data.data[1])
        self.ui.speed_3.setNum(data.data[2])
        self.ui.speed_4.setNum(data.data[3])
    
    
    def imu(self,data):
        
        self.orientation_q = data.orientation
        self.orientation_list = [self.orientation_q.x,self.orientation_q.y,self.orientation_q.z,self.orientation_q.w]   
        # Calculation of the imu data     
        (self.roll,self.pitch,self.yaw) = euler_from_quaternion(self.orientation_list)
        self.ui.label_54.setNum(round((((self.roll)/math.pi)*180),2))
        self.ui.label_56.setNum(round((((self.pitch)/math.pi)*180),2))
        self.ui.label_58.setNum(round((((self.yaw)/math.pi)*180),2))
        self.ui.label_60.setNum(round((((data.orientation.w)/math.pi)*180),2))

    @pyqtSlot(int)   
    def create_gallery(self,count):
        print(count)
        column=count%3
        row=int(count/3)

        self.g_frame = QFrame(self.scrollwidget_gallery)
        self.g_frame.setMinimumSize(QSize(500, 500))
        self.g_frame.setMaximumSize(QSize(500, 500))
        self.g_frame.setStyleSheet("QFrame#frame{border-radius:50px; \n padding :15px;}")
        self.g_frame.setFrameShape(QFrame.StyledPanel)
        self.g_frame.setFrameShadow(QFrame.Raised)
        self.g_frame.setObjectName("g_frame_{}".format(count))
        
        self.grid.setSpacing(20)

        self.verticall = QVBoxLayout(self.g_frame)
        self.verticall.setObjectName("verticall")

        self.gal_label = QLabel(self.g_frame)
        self.gal_label.setObjectName("gal_label_{}_{}".format(row,column))
        self.gal_label.setMinimumSize(QSize(100,100))
        self.gal_label.setAlignment(Qt.AlignVCenter|Qt.AlignCenter)
        self.gal_label.setPixmap(QPixmap('/home/melikenur/proje2_ws/gallery/{}.jpg'.format(count)))
        self.gal_label.setScaledContents(True)
        self.verticall.addWidget(self.gal_label)

        self.gal_num = QLabel(self.g_frame)
        self.gal_num.setObjectName("label_3")
        self.gal_num.setText("{}".format(count))
        self.verticall.addWidget(self.gal_num)
        
        self.verticall.setStretch(0, 9)
        self.verticall.setStretch(1, 1)
        self.grid.addWidget(self.g_frame, row, column, 1, 1)


    def send_flag_for_rock(self):
        self.publisher.publish(True)
        print('True')
        cv2.imwrite("/home/melikenur/proje2_ws/gallery/" + str(self.foto_counter) + ".jpg" ,self.image)
        self.ui.label_33.setPixmap(QPixmap('/home/melikenur/proje2_ws/gallery/'+str(self.foto_counter) + '.jpg'))
        self.gallery_signal.emit(self.foto_counter)
        self.foto_counter +=1
        
        
        

        
if __name__=="__main__":
    rospy.init_node('listener', anonymous=True)
    rospy.loginfo( "zort")


    app= QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
    
