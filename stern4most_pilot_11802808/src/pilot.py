#!/usr/bin/python
from __future__ import division

from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

import datetime as dt
import rospy
import math
from stern4most_messages.msg import Lines #niet vergeten te sourcen!!!


class Pilot:

    def __init__(self):
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

        self.lines_sub = rospy.Subscriber("/vision/lines", Lines, self.pilot_callback, queue_size = 1)
        self.gui_sub = rospy.Subscriber("/gui", Bool, self.autopilot_start_stop, queue_size = 1)
        self.gui_control_sub = rospy.Subscriber("gui/controls", Twist, self.control )
        self.gui_reverse_sub = rospy.Subscriber("/gui/reverse", Bool, self.is_reverse )

        self.running = True
        self.start_autopilot = False
        self.reverse = False

    def is_reverse(self, bool):
        self.reverse = bool.data


    def control(self, twist):
        print(twist)
        self.pub.publish(twist)

    def moveforward(self, speed, distance):
    
   # afstand = snelheid / tijd
   # eerst tijd nu meten 
   # elke loop tijd meten
   # als distance > speed / (start - nu) stopt de robot. is afstand bereikt
    
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

    #print(distance > n_distance)
        while(distance > n_distance):

        #print(twist)
            self.pub.publish(twist)
            now = dt.datetime.now()
            n_distance = speed * (now - start).total_seconds()
            rate.sleep()
        twist.linear.x = 0
        self.pub.publish(twist)


    def turn(self, degrees_per_second,angle, isright):
        radian_speed = degrees_per_second * math.pi /180
    
        twist = Twist()
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        if isright == True:
            twist.angular.z = -radian_speed
        else:
            twist.angular.z = radian_speed
        rate = rospy.Rate(100)

        start = dt.datetime.now()
        now = dt.datetime.now()
        n_distance = 0

        print(angle  * math.pi /180 > n_distance)
        while(angle * math.pi /180 > n_distance):
       # print(twist)
            self.pub.publish(twist)
            now = dt.datetime.now()
            n_distance = radian_speed * (now - start).total_seconds()
       # print(n_distance)
            rate.sleep()

        twist.angular.z = 0
        self.pub.publish(twist)
    
        twist.linear.x = 0
        self.pub.publish(twist)


    def pilot_callback(self, line_message):

        print("must drive: ", str(self.start_autopilot))

        if(self.start_autopilot== True):
            
            y = (line_message.y2 - line_message.y1)
            x = (line_message.x2 - line_message.x1)
   
            slope = float((line_message.y2 - line_message.y1) / (line_message.x2 - line_message.x1))
    #print("slope", slope)
            print(slope)
    
            if(slope < 1.2 and slope > 0) :
                
                if(self.reverse == False):
                    self.turn(12,12,False)
                    rint("left!")
                    self.moveforward(0.1,0.1)
                    print("forward!")
                elif(self.reverse == True):
                    self.turn(12,12,True)
                    print("right!")
                    self.moveforward(-0.1,0.1)
                    print("backward!")  
            elif(slope > -1.2 and slope < 0):
                
                
                if(self.reverse == False):
                    self.turn(12,12,True)
                    print("right!")
                    self.moveforward(0.1,0.1)
                    print("forward!")
                elif(self.reverse == True):
                    self.turn(12,12,False)
                    print("left!")
                    self.moveforward(-0.1,0.1)
                    print("backward!")  
            else:
                if(self.reverse == False):
                    self.moveforward(0.15,0.1)
                    print("forward!")
                elif(self.reverse == True):
                    self.moveforward(-0.15,0.1)
                    print("backward!")  
        

    def autopilot_start_stop(self, on):
        print(on)
        self.start_autopilot = on.data
        print("i just set start to :" , str(self.start_autopilot))

    def is_running(self):
        return self.running

if __name__=='__main__':
    rospy.init_node('pilot')
    


    pilot = Pilot()

    while pilot.is_running():
        #time.sleep(5)
        rospy.spin()
    #moveforward(.2, 4.0)
    #turn(20, 90, True)
