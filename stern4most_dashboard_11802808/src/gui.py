#!/usr/bin/python

import sys
import os

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QApplication
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

import rospy
from std_msgs.msg import Bool
from std_msgs.msg import String

from geometry_msgs.msg import Twist


class GUI(QWidget):

    def __init__(self):
        super(GUI, self).__init__()

        self.counter = 0
        topic_name = "gui"

        self.bridge = CvBridge()
        #subscriber_name = "test_subscriber"

        self.publisher_name = "gui_publisher"
        rospy.init_node("gui_publish", anonymous=False)

        self.race_info_subscriber = rospy.Subscriber("/communication/race", String, self.string_message_received)
        self.subscriber = rospy.Subscriber("/camera/rgb/image_raw", Image, self.image_message_received)
        self.publisher = rospy.Publisher(topic_name, Bool, queue_size=1)
        self.publisher_race = rospy.Publisher("gui/race", Bool, queue_size=1)
        self.control_publisher = rospy.Publisher("gui/controls", Twist, queue_size=1)

        self.init_ui()

    def init_ui(self):
        start = QPushButton('start autopilot', self)
        stop = QPushButton('stop autopilot', self)

        forward = QPushButton('go forward', self)
        backward = QPushButton('go backward', self)
        right = QPushButton('go right', self)
        left = QPushButton('go left', self)
        brake = QPushButton('brake', self)
        race = QPushButton('race (experimental)', self)

        start.clicked.connect(self.start_clicked)
        start.resize(start.sizeHint())

        stop.clicked.connect(self.stop_clicked)
        stop.resize(start.sizeHint())

        forward.clicked.connect(self.forward)
        forward.resize(start.sizeHint())

        backward.clicked.connect(self.back)
        backward.resize(start.sizeHint())

        right.clicked.connect(self.right)
        right.resize(start.sizeHint())

        left.clicked.connect(self.left)
        left.resize(start.sizeHint())

        brake.clicked.connect(self.brake)
        brake.resize(start.sizeHint())
        
        race.clicked.connect(self.race)
        race.resize(start.sizeHint())
        
        self.race_info = QtWidgets.QLabel("[][][] race info [][][]", self)
        self.race_info.move(200,200)

        self.image_frame = QtWidgets.QLabel()
        self.image_frame.move(200,200)


        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.race_info)
        self.layout.addWidget(start)
        self.layout.addWidget(stop)
        self.layout.addWidget(brake)
        self.layout.addWidget(forward)
        self.layout.addWidget(left)
        self.layout.addWidget(right)
        self.layout.addWidget(backward)

        self.layout.addWidget(self.image_frame)
        self.layout.addWidget(race)

        self.setLayout(self.layout)


        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle('stern4most gui')
        self.show()

    def race(self):
        rospy.loginfo("sending message to race ")
        bol = True
        self.publisher_race.publish(bol)
    def brake(self):
        self.control_button(0,0,0,0,0,0)
        self.send_data(False)
    def forward(self): 
        self.control_button( 0.2,0,0,0,0,0)
    def back(self): 
        self.control_button( -0.2,0,0,0,0,0)
    def left(self): 
        self.control_button( 0,0,0,0,0,0.2)
    def right(self): 
        self.control_button( 0,0,0,0,0,-0.2)

    def send_data(self, on):
        rospy.loginfo("Sending: " + str(on))
        self.publisher.publish(on)
        rospy.loginfo("Sent\n")
    
    def control_button(self, lx, ly, lz, ax, ay, az):
        twist = Twist()
        twist.linear.x = lx
        twist.linear.y = ly
        twist.linear.z = lz
        twist.angular.x = ax
        twist.angular.y = ay
        twist.angular.z = az

        rospy.loginfo("Sending: " + str(twist))
        self.control_publisher.publish(twist)

    def start_clicked(self):
        self.send_data(True)

    def stop_clicked(self):
        self.send_data(False)

    def string_message_received(self, data):
        self.race_info.setText(data.data)

    def image_message_received(self, data):
        image = self.convert_ros_to_opencv(data)
        image = cv2.pyrDown(image)

        #self.image = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()))
    
    def convert_ros_to_opencv(self, ros_image):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
            return cv_image
        except CvBridgeError as error:
            raise Exception("Failed to convert to OpenCV image")

if __name__ == '__main__':
    application = QApplication(sys.argv)
    gui = GUI()
    sys.exit(application.exec_())
