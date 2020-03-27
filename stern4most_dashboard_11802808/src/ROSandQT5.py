#!/usr/bin/python

import sys
import os

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QApplication

import rospy
from std_msgs.msg import Bool


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

        self.label = None
        self.init_ui()

    def init_ui(self):
        start = QPushButton('start autopilot', self)
        stop = QPushButton('stop autopilot', self)

        start.clicked.connect(self.start_clicked)
        start.resize(start.sizeHint())
        start.move(10, 50)

        stop.clicked.connect(self.stop_clicked)
        stop.resize(start.sizeHint())
        stop.move(10, 100)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('stern4most')
        self.show()

    def send_data(self, on):
        rospy.loginfo("Sending: " + str(on))
        self.publisher.publish(on)
        rospy.loginfo("Sent\n")
    
    def start_clicked(self):
        self.send_data(True)

    def stop_clicked(self):
        self.send_data(False)

    def string_message_received(self, data):
        rospy.loginfo("Receiving data: " + data.data)
        self.label.setText(data.data)
        self.label.resize(self.label.sizeHint())
        rospy.loginfo("GUI updated\n")



if __name__ == '__main__':
    application = QApplication(sys.argv)
    gui = GUI()
    sys.exit(application.exec_())
