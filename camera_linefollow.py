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


    def color_detect(self, img, color_name):

        # The blue range will be different under different lighting conditions and can be adjusted flexibly.  H: chroma, S: saturation v: lightness
        resize_img = cv2.resize(img, (160,120), interpolation=cv2.INTER_LINEAR)  # In order to reduce the amount of calculation, the size of the picture is reduced to (160,120)
        hsv = cv2.cvtColor(resize_img, cv2.COLOR_BGR2HSV)              # Convert from BGR to HSV
        color_type = color_name

        mask = cv2.inRange(hsv,np.array([min(self.color_dict[color_type]), 60, 60]), np.array([max(self.color_dict[color_type]), 255, 255]) )           # inRange()：Make the ones between lower/upper white, and the rest black
        if color_type == 'blue':
                mask_2 = cv2.inRange(hsv, (self.color_dict['blue'][0],0,0), (self.color_dict['blue'][1],255,255))
                mask = cv2.bitwise_or(mask, mask_2)

        morphologyEx_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel_5,iterations=1)              # Perform an open operation on the image

        contours, hierarchy = cv2.findContours(morphologyEx_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)          # Find the contour in morphologyEx_img, and the contours are arranged according to the area from small to large

        color_area_num = len(contours) # Count the number of contours

        if color_area_num > 0:
            for i in contours:    # Traverse all contours
                x,y,w,h = cv2.boundingRect(i)      # Decompose the contour into the coordinates of the upper left corner and the width and height of the recognition object

                # Draw a rectangle on the image (picture, upper left corner coordinate, lower right corner coordinate, color, line width)
                if w >= 8 and h >= 8: # Because the picture is reduced to a quarter of the original size, if you want to draw a rectangle on the original picture to circle the target, you have to multiply x, y, w, h by 4.
                    x = x * 4
                    y = y * 4
                    w = w * 4
                    h = h * 4
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)  # Draw a rectangular frame
                    cv2.putText(img,color_type,(x,y), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)# Add character description

        return img,mask,morphologyEx_img

    def process(self):
        print("start color detect")
        camera = PiCamera()
        camera.resolution = (640,480)
        camera.framerate = 24
        rawCapture = PiRGBArray(camera, size=camera.resolution)
        for frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):# use_video_port=True
            img = frame.array
            img,img_2,img_3 =  self.color_detect(img,'blue')  # Color detection function
            cv2.imshow("video", img)    # OpenCV image show
            cv2.imshow("mask", img_2)    # OpenCV image show
            cv2.imshow("morphologyEx_img", img_3)    # OpenCV image show
            rawCapture.truncate(0)   # Release cache

            k = cv2.waitKey(1) & 0xFF
            # 27 is the ESC key, which means that if you press the ESC key to exit
            if k == 27:
                camera.close()
                break
    def read_frame(self):
        frame =cv2.imread('/home/pi/DeepPiCar/driver/data/road1_240x320.png')
        return frame

    def detect_edges(self):
        # filter for blue lane lines
        frame =self.read_frame()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        show_image("hsv", hsv)
        lower_blue = np.array([60, 40, 40])
        upper_blue = np.array([150, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        show_image("blue mask", mask)

        # detect edges
        edges = cv2.Canny(mask, 200, 400)

        return edges



#init camera
if __name__=='__main__':
    # det=ColorDetecframe = cv2.imread('/home/pi/DeepPiCar/driver/data/road1_240x320.png')

    color=ColorDetect()
    ed=color.read_frame()
    cv2.imshow('sample image',ed)

    cv2.waitKey(10)
    # det.process()
