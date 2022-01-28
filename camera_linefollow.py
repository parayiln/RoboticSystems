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


    def detect_edges(self, img):

        # The blue range will be different under different lighting conditions and can be adjusted flexibly.  H: chroma, S: saturation v: lightness
        resize_img = cv2.resize(img, (160,120), interpolation=cv2.INTER_LINEAR)  # In order to reduce the amount of calculation, the size of the picture is reduced to (160,120)
        hsv = cv2.cvtColor(resize_img, cv2.COLOR_BGR2HSV)              # Convert from BGR to HSV
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

    def detect_line_segments(cropped_edges):
        # tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
        rho = 1  # distance precision in pixel, i.e. 1 pixel
        angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
        min_threshold = 10  # minimal of votes
        line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold,
                                        np.array([]), minLineLength=8, maxLineGap=4)

        return line_segments

    def average_slope_intercept(self,frame, line_segments):
    # """
    # This function combines line segments into one or two lane lines
    # If all line slopes are < 0: then we only have detected left lane
    # If all line slopes are > 0: then we only have detected right lane
    # """
        lane_lines = []
        if line_segments is None:
            logging.info('No line_segment segments detected')
            return lane_lines

        height, width, _ = frame.shape
        left_fit = []
        right_fit = []

        boundary = 1/3
        left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
        right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

        for line_segment in line_segments:
            for x1, y1, x2, y2 in line_segment:
                if x1 == x2:
                    logging.info('skipping vertical line segment (slope=inf): %s' % line_segment)
                    continue
                fit = np.polyfit((x1, x2), (y1, y2), 1)
                slope = fit[0]
                intercept = fit[1]
                if slope < 0:
                    if x1 < left_region_boundary and x2 < left_region_boundary:
                        left_fit.append((slope, intercept))
                else:
                    if x1 > right_region_boundary and x2 > right_region_boundary:
                        right_fit.append((slope, intercept))

        left_fit_average = np.average(left_fit, axis=0)
        if len(left_fit) > 0:
            lane_lines.append(make_points(frame, left_fit_average))

        right_fit_average = np.average(right_fit, axis=0)
        if len(right_fit) > 0:
            lane_lines.append(make_points(frame, right_fit_average))

        logging.debug('lane lines: %s' % lane_lines)  # [[[316, 720, 484, 432]], [[1009, 720, 718, 432]]]

        return lane_lines


    def make_points(self, frame, line):
        height, width, _ = frame.shape
        slope, intercept = line
        y1 = height  # bottom of the frame
        y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

        # bound the coordinates within the frame
        x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
        x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
        return [[x1, y1, x2, y2]]

    def detect_lane(self, frame):
        edges = detect_edges(frame)
        cropped_edges = region_of_interest(edges)
        line_segments = detect_line_segments(cropped_edges)
        lane_lines = average_slope_intercept(frame, line_segments)

        return lane_lines


    def process(self):
        print("lane following using the camera")
        camera = PiCamera()
        camera.resolution = (640,480)
        camera.framerate = 24
        rawCapture = PiRGBArray(camera, size=camera.resolution)
        for frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):# use_video_port=True
            frame = frame.array
            img=self.detect_lane(frame)
            print("hello",img) # Color detection function
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
