# week 5

import sys
import atexit
try:
    sys.path.append(r'/home/nidhi/RoboticSystems/lib')
    from pin import Pin
except ImportError:
    sys.path.append(r'/home/nidhi/intro2/RoboticSystems/lib')
    print ("This computer does not appear to be a PiCar -X system (ezblock is not present). Shadowing hardware calls with substitute functions ")
    from sim_ezblock import *
from picarx_improved import Picarx
import time
import numpy
from ultrasonic import Ultrasonic

class SensingUltra(object):
    def __init__(self, trig_pin = Pin("D2") , echo_pin = Pin("D3"), timeout=0.02):
        self.trig = trig
        self.echo = echo
        self.timeout = timeout

    def sensing(self):
        ultra_sonic = Ultrasonic()
        dist_value=ultra_sonic.read()
        return dist_value

class InterpretationUltra(object):
    # take arguments for sensitivity and polarity
    def __init__(self, ref_TooClose = 25):
        self.TooClose = ref_TooClose


    def caliberation(self,cali):
        cali_val = cali
        sum=0
        for i in range(len(cali)):
            sum = sum+cali[i]
        final_cali = sum/len(cali)
        self.TooClose = final_cali

    def processing(self,data):
        val=data
        close=1 #defalut not close
        if val > self.TooClose:
            close=1
        else:
            close=0
        return close


class ControllerUltra(object):
    def __init__(self):
        self.sense=Sensing()
        # self.infer = Interpretation(self.sense)
        self.motor =motor_command.Picarx()

    def stop_move(self,dist):
        close=dist
        if close==0:
            self.motor.stop()
            time.sleep(0.01)
        else:
            self.motor.forward(30)
            time.sleep(0.01)

    def stop(self):
        self.motor.stop()
        time.sleep(0.01)

 # automatic steering

if __name__=='__main__':
    sense = Sensing(500)
    print("Code for line following using the Grayscale module")
    data=sense.sensing()

    infer=Interpretation()
    dist=infer.processing(data)
    control= Controller()

    print("Select 2 to calibrate or 1 to use the defalut values ")
    flag_cali=input()
    if flag_cali==2:
        print("please hold against the wall at a safe distance ")
        cali=[]
        cali.append(sense.sensing())
        cali.append(sense.sensing())
        cali.append(sense.sensing())
    else:
        if flag_cali != 1 and flag_cali != 2:
            print("no valid selection made using the defaut values")
        while (True):
            control.stop_move(dist)
