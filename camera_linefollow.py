# coding=utf-8
# week 3

import logging
from logdecorator import log_on_start , log_on_end , log_on_error
import time
import motor_command
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

logging_format = "%( asctime)s: %( message)s"
# logging.basicConfig(format=logging_format , level=logging.INFO , datefmt ="%H:%M:%S")
logging.getLogger ().setLevel(logging.DEBUG)


class ColorDetect(object):

    def __init__(self):
        self.color_dict = {'red':[0,4],'orange':[5,18],'yellow':[22,37],'green':[42,85],'blue':[92,110],'purple':[115,165],'red_2':[165,180]}  #Here is the range of H in the HSV color space represented by the color
        self.kernel_5 = np.ones((5,5),np.uint8) #Define a 5×5 convolution kernel with element values of all 1.


    def color_detect(self, img):

        # The blue range will be different under different lighting conditions and can be adjusted flexibly.  H: chroma, S: saturation v: lightness
        resize_img = cv2.resize(img, (160,120), interpolation=cv2.INTER_LINEAR)  # In order to reduce the amount of calculation, the size of the picture is reduced to (160,120)
        hsv = cv2.cvtColor(resize_img, cv2.COLOR_BGR2HSV)              # Convert from BGR to HSV
        color_type = color_name
        lower_blue = np.array([60, 40, 40])
        upper_blue = np.array([150, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        edges = cv2.Canny(mask, 200, 400)
        return edges

    def region_of_interest(self, edges):
        height, width = edges.shape
        mask = np.zeros_like(edges)

        # only focus bottom half of the screen
        polygon = np.array([[
            (0, height * 1 / 2),
            (width, height * 1 / 2),
            (width, height),
            (0, height),
        ]], np.int32)

        cv2.fillPoly(mask, polygon, 255)
        cropped_edges = cv2.bitwise_and(edges, mask)
        return cropped_edges

    def process(self):
        print("lane following using the camera")
        camera = PiCamera()
        camera.resolution = (640,480)
        camera.framerate = 24
        rawCapture = PiRGBArray(camera, size=camera.resolution)
        for frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):# use_video_port=True
            img = frame.array
            img =  self.region_of_interest(img)  # Color detection function
            cv2.imshow("video", img)    # OpenCV image show
            rawCapture.truncate(0)   # Release cache

            k = cv2.waitKey(1) & 0xFF
            # 27 is the ESC key, which means that if you press the ESC key to exit
            if k == 27:
                camera.close()
                break



#init camera
if __name__=='__main__':
    det=ColorDetect()
    det.process()
