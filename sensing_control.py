# week 3

import logging
from logdecorator import log_on_start , log_on_end , log_on_error
import time
import motor_command
import sys
sys.path.append(r'/home/nidhi/RoboticSystems/lib/')
try:

    from adc import ADC
    from utils import reset_mcu
    reset_mcu()
    time.sleep (0.01)
except ImportError:
    print ("Sense and control: This computer does not appear to be a PiCar -X system (ezblock is not present). Shadowing hardware calls with substitute functions ")
    from sim_ezblock import *

logging_format = "%( asctime)s: %( message)s"
# logging.basicConfig(format=logging_format , level=logging.INFO , datefmt ="%H:%M:%S")
logging.getLogger ().setLevel(logging.DEBUG)

class Sensing(object):
    def __init__(self,ref = 1000):
        self.chn_0 = ADC("A0")
        self.chn_1 = ADC("A1")
        self.chn_2 = ADC("A2")
        self.ref = ref

    def sensing(self):
        adc_value_list = []
        adc_value_list.append(self.chn_0.read())
        adc_value_list.append(self.chn_1.read())
        adc_value_list.append(self.chn_2.read())
        return adc_value_list

class Interpretation(Sensing):
    # take arguments for sensitivity and polarity
    def __init__(self, ref_polarity = 1, ref_sensitivity = 1000):
        # polarity 1 means the line the car is following is darker than the surrounding.
        #change polarity to 0 if the car is following a lighter line.
        self.polarity = ref_polarity
        self.sensitivity = ref_sensitivity
        self.sense=Sensing()

    def caliberation(self):
        print("please hold against the light surface")
        light_values = self.sense.sensing()
        average_light =(light_values[0]+light_values[1]+light_values[2])/3
        print("Thank you ! please hold against the dark surface")
        dark_values = self.sense.sensing()
        average_dark =(dark_values[0]+dark_values[1]+dark_values[2])/3
        cali_values= (average_dark+average_light)/2
        self.sensitivity=cali_values

    def Processing(self,data):
        adc_values=data
        label=adc_values
        ####### label the values as dark or light ############
        for i in range(3):
            if adc_values[i] > self.sensitivity: # should i take an average to detect sharp changes???
                label[i]=0 # light
            else:
                label[i]=1 #dark
        # setting the polarity condition
        if self.polarity==1:
            line =1
        else:
            line =0
     ######### calculate distance
        if (label[0]==line and label[1]==line and label[2]==line):
            distance =0
        elif (label[0]!=line and label[1]==line and label[2]==line):
            distance = .5
        elif (label[0]!=line and label[1]!=line and label[2]==line):
            distance = 1
        elif (label[0]==line and label[1]==line and label[2]!=line):
            distance = -.5
        elif (label[0]==line and label[1]!=line and label[2]!=line):
            distance = -1
        else:
            distance =0
            print("I cannot see any line - moving straight blindly. Please guide this blind car to a line, Thankyou!")
        return distance


class Controller(Interpretation):
    def __init__(self, scaling = -40):
        print("enter control")
        self.sense=Sensing(500)
        self.infer = Interpretation(self.sense)
        self.scaling_factor=-40
        self.motor =motor_command.Picarx()

    def control(self, angle):
        angle_steer =self.motor.set_dir_servo_angle(angle)
        return angle_steer
# function for control - sensing integration
    def move(self,dist):
        distance=dist
        self.control(distance*self.scaling_factor)
        time.sleep(.05)
        self.motor.forward(30)
        time.sleep(.05)

    def stop(self):
        self.motor.stop()






 # automatic steering

if __name__=='__main__':
    sense = Sensing(500)
    print("Code for line following using the Grayscale module")
    data=sense.sensing()

    infer=Interpretation(sense)
    dist=infer.Processing(data)
    control= Controller(infer)

    print("Select 2 to calibrate or 1 to use the defalut values ")
    flag_cali=input()
    if flag_cali==2:
        infer.calibration()
    else:
        if flag_cali != 1 and flag_cali != 2:
            print("no valid selection made using the defaut values")
        while (True):
            control.move(dist)



 # sensor control integration
 # camera based driving
