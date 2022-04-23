#!/usr/bin/env python2.7

#Halil Faruk Karagoz

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Bool,String
import cv2
from cv_bridge import CvBridge, CvBridgeError 
import numpy as np
import time
import os
import copy
import subprocess as subprocess



class take_photo:
    def __init__(self):
        rospy.init_node("take_photo");
        self.bridge = CvBridge(); 
        self.cv_image = None
        rospy.Subscriber("/camera/image_raw",Image,self.camera_img);
        rospy.Subscriber("/classification_flag",Bool,self.classify)
        self.pub = rospy.Publisher("/classification_result",String,queue_size=10)
        rospy.loginfo("Wait for image")
        rospy.spin()
    def camera_img(self,data):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

    def classify(self,data):
        if(data.data):
            cv2.imwrite("img.jpg",self.cv_image)
            rospy.loginfo("Processing")
            subprocess.call(['python3',  '/home/melikenur/proje2_ws/src/science_classification/src/classify_rock.py'])
            with open('result.txt','r') as f:
                lines = f.readlines()
            print(lines[0])
            self.pub.publish(str(lines[0]))
        rospy.loginfo("Wait for image")


if __name__ == "__main__":
    take_photo();
