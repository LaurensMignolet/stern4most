#!/usr/bin/python

import sys
import os

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QApplication

import rospy
from std_msgs.msg import Bool

from geometry_msgs.msg import Twist


class GUI(QWidget):

    def __init__(self):
        super(GUI, self).__init__()

        self.counter = 0
        topic_name = "gui"

        #subscriber_name = "test_subscriber"

        self.publisher_name = "gui_publisher"
        rospy.init_node("gui_publish", anonymous=False)

        #self.subscriber = rospy.Subscriber(topic_name, String, self.string_message_received)
        self.publisher = rospy.Publisher(topic_name, Bool, queue_size=1)
        self.control_publisher = rospy.Publisher("gui/controls", Twist, queue_size=1)

        self.label = None
        self.init_ui()

    def init_ui(self):
        start = QPushButton('start autopilot', self)
        stop = QPushButton('stop autopilot', self)

        forward = QPushButton('go forward', self)
        backward = QPushButton('go backward', self)
        right = QPushButton('go right', self)
        left = QPushButton('go left', self)
        emergency_stop = QPushButton('emergency stop', self)

        start.clicked.connect(self.start_clicked)
        start.resize(start.sizeHint())
        start.move(10, 50)

        stop.clicked.connect(self.stop_clicked)
        stop.resize(start.sizeHint())
        stop.move(10, 100)

        forward.clicked.connect(self.forward)
        forward.resize(start.sizeHint())
        forward.move(10, 150)

        backward.clicked.connect(self.back)
        backward.resize(start.sizeHint())
        backward.move(10, 200)

        right.clicked.connect(self.right)
        right.resize(start.sizeHint())
        right.move(10, 250)

        left.clicked.connect(self.left)
        left.resize(start.sizeHint())
        left.move(10, 300)

        emergency_stop.clicked.connect(self.emergency_stop)
        emergency_stop.resize(start.sizeHint())
        emergency_stop.move(10, 350)

        self.setGeometry(300, 300, 250, 500)
        self.setWindowTitle('stern4most')
        self.show()

    def emergency_stop(self):
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

    #def string_message_received(self, data):
    #    rospy.loginfo("Receiving data: " + data.data)
    #    self.label.setText(data.data)
    #    self.label.resize(self.label.sizeHint())
    #    rospy.loginfo("GUI updated\n")



if __name__ == '__main__':
    application = QApplication(sys.argv)
    gui = GUI()
    sys.exit(application.exec_())
