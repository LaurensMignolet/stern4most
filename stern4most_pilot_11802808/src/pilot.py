#!/usr/bin/python
from __future__ import division

from geometry_msgs.msg import Twist
import datetime as dt
import rospy
import math
from stern4most_messages.msg import Lines #niet vergeten te sourcen!!!

'''
todo
subscriben op lines  ok
lines analyseren
richting aanpassen. 

'''
def moveforward(speed, distance):
    '''
    afstand = snelheid / tijd
    eerst tijd nu meten 
    elke loop tijd meten
    als distance > speed / (start - nu) stopt de robot. is afstand bereikt
    '''
    twist = Twist()
    twist.linear.x = speed
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 0

    start = dt.datetime.now()
    now = dt.datetime.now()
    n_distance = 0

    rate = rospy.Rate(100)

    print(distance > n_distance)
    while(distance > n_distance):

        print(twist)
        pub.publish(twist)
        now = dt.datetime.now()
        n_distance = speed * (now - start).total_seconds()
        rate.sleep()
    twist.linear.x = 0
    pub.publish(twist)


def turn(degrees_per_second,angle, isLeft):
    radian_speed = degrees_per_second * math.pi /180
    
    twist = Twist()
    twist.linear.x = 0
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    if isLeft == True:
        twist.angular.z = -radian_speed
    else:
        twist.angular.z = radian_speed
    rate = rospy.Rate(100)

    start = dt.datetime.now()
    now = dt.datetime.now()
    n_distance = 0

    print(angle  * math.pi /180 > n_distance)
    while(angle * math.pi /180 > n_distance):
        print(twist)
        pub.publish(twist)
        now = dt.datetime.now()
        n_distance = radian_speed * (now - start).total_seconds()
        print(n_distance)
        rate.sleep()

    twist.angular.z = 0
    pub.publish(twist)
    
    twist.linear.x = 0
    pub.publish(twist)


def pilot_callback(line_message):
    #print(line_message, "todo")
    '''
    rico zoeken. robot nabij recht (+- 5 graden?) met lijn laten gaan. 

    (X1 * Y2)^2 
    '''

    #rico = float((line_message.y2 - line_message.y1) / (line_message.x2 - line_message.x1)) * 100
    
# Slope = (y2 - y1)/(x2 - x1)
    x = (line_message.y2 - line_message.y1)
    y = (line_message.x2 - line_message.x1)
    print("modulo", x%y)
    print(x)
    print(y)
    print(x/y)
    slope = float((line_message.y2 - line_message.y1) / (line_message.x2 - line_message.x1))
    #print("slope", slope)

if __name__=='__main__':
    rospy.init_node('pilot')
    pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)

    rospy.Subscriber("/vision/lines", Lines, pilot_callback)


    rospy.spin()
    #moveforward(.2, 4.0)
    #turn(20, 90, True)
