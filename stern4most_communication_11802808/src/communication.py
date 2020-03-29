#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
from std_msgs.msg import String

def racing(s):
    rospy.loginfo(s)
    publisher.publish(s)
    if(s.data == "Start"):
        publisher_to_pilot.publish(True)



def callback(com):
    race = com
    rospy.loginfo(race)
    while race.data == True:
        rospy.Subscriber("game_on", String, racing)
        rate.sleep()


        
rospy.init_node('communications_node', anonymous=True)
race = False
rate = rospy.Rate(5)
publisher = rospy.Publisher("communication/race", String, queue_size=1)
publisher_to_pilot = rospy.Publisher("gui", Bool, queue_size=1)

rospy.Subscriber("/gui/race", Bool, callback)

rospy.spin()