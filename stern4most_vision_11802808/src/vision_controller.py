#!/usr/bin/python

import rospy
import time

from sensor_msgs.msg import Image
from threading import Lock



from std_msgs.msg import String

import cv2
from cv_bridge import CvBridge, CvBridgeError

import numpy as np
from stern4most_messages.msg import Lines #niet vergeten te sourcen!!!

GUI_UPDATE_PERIOD = 0.10  # Seconds


class VisionDisplay:

    def __init__(self):
        self.running = True
        self.subVideo   = rospy.Subscriber('/camera/rgb/image_raw', Image, self.callback_image_raw)

        self.bridge = CvBridge()

        self.image = None
        self.imageLock = Lock()

        self.bound_low = np.array([0, 0, 0])
        self.bound_up  = np.array([0, 0, 0])

        #eigenschappen publisher
        self.pub = rospy.Publisher('/vision/lines', Lines, queue_size=10 )
        #self.image_pub = rospy.Publisher("lines", Image, queue_size=10)

        self.line_image = None
        #####

        self.statusMessage = ''

        self.connected = False

        self.redrawTimer = rospy.Timer(rospy.Duration(GUI_UPDATE_PERIOD), self.callback_redraw)
    

    def is_running(self):
        return self.running

    def region_of_interest(self, img, vertices):
        mask = np.zeros_like(img)
        # channel_count = img.shape[2]
        match_mask_color = 255
        cv2.fillPoly(mask, vertices, match_mask_color)
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image

    def draw_the_lines(self, img, lines):
        img = np.copy(img)
        blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
        try:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(blank_image, (x1, y1), (x2, y2), (0, 255, 0), thickness=10)
                    cv2.putText(blank_image, "x=100, y= 50:", (100, 0), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                    cv2.putText(blank_image, "position:", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
                    lijn = Lines()
                    lijn.x1 = x1
                    lijn.x2 = x2
                    self.pub.publish(lijn)

        except TypeError:
            print("oops")

        img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
        return img

    # = cv2.imread('road.jpg')
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    def detect_lane(self, image):  #dank aan https://www.youtube.com/watch?v=0se6_UPNWVc&list=PLS1QulWo1RIa7D1O6skqDQ-JZ1GGHKK-K&index=37

        height = image.shape[0]
        width = image.shape[1]
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV )

        mask = cv2.inRange(hsv, np.array([143,97,128]), np.array([255,255,255]))
        cv2.imshow("mlast", mask)

        region_of_interest_vertices = [
            (0, height),
            (width / 2, height / 2),
            (width, height)
        ]
        #gray_image = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
        canny_image = cv2.Canny(mask, 100, 120)
        cropped_image = self.region_of_interest(canny_image,
                                                 np.array([region_of_interest_vertices], np.int32), )
        
        cv2.imshow("crop", cropped_image)
        lines = cv2.HoughLinesP(cropped_image,
                                rho=2,
                                theta=np.pi / 180,
                                threshold=50,
                                lines=np.array([]),
                                minLineLength=40,
                                maxLineGap=100)
        #print(lines)
        image_with_lines = self.draw_the_lines(image, lines)
        return image_with_lines



    def convert_ros_to_opencv(self, ros_image):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
            return cv_image
        except CvBridgeError as error:
            raise Exception("Failed to convert to OpenCV image")

    def callback_redraw(self, event):
        if self.running == True and self.image is not None:
            self.imageLock.acquire()
            try:
                # Convert the captured frame from ROS to OpenCV.
                image_cv = self.convert_ros_to_opencv(self.image)
            finally:
                self.imageLock.release()

            cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
            img = cv2.resize(image_cv,(360,480))
            cv2.imshow("Image", img)

            #cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
            #cv2.createTrackbar("Hue lower bound:", "Mask", 0, 179, self.callback_trackbars)
            #cv2.createTrackbar("Hue upper bound:", "Mask", 0, 179, self.callback_trackbars)

            #image_hsv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2HSV)
            #mask = cv2.inRange(image_hsv, self.bound_low, self.bound_up)

            self.line_image = self.detect_lane(img)

            cv2.imshow("lane detection", self.line_image)


            #cv2.imshow('Mask', mask)

            key = cv2.waitKey(5)
            if key == 27: # Esc key top stop
                cv2.destroyAllWindows()
                self.running = False

    def callback_trackbars(self, value):
        h_low = 143#cv2.getTrackbarPos('Hue lower bound:', 'Mask')
        h_up  = 255#cv2.getTrackbarPos('Hue upper bound:', 'Mask')
        s_low = 97
        s_up  = 255
        v_low = 128
        v_up  = 255

        self.bound_low = np.array([h_low, s_low, v_low], np.uint8)
        self.bound_up = np.array([h_up, s_up, v_up], np.uint8)


    def callback_image_raw(self, data):
        self.imageLock.acquire()
        try:
            self.image = data
        finally:
            self.imageLock.release()


if __name__=='__main__':
    rospy.init_node('vision_controller')

    display = VisionDisplay()

    while display.is_running():
        time.sleep(5)
