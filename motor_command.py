# week 2

import logging
from logdecorator import log_on_start , log_on_end , log_on_error
import time
import atexit
try:
    # from ezblock import *
    # from ezblock import __reset_mcu__
    from servo import Servo
    from pwm import PWM
    from pin import Pin
    from adc import ADC
    from filedb import fileDB
    from utils import reset_mcu
    reset_mcu()
    time.sleep (0.01)
except ImportError:
    print ("This computer does not appear to be a PiCar -X system (ezblock is not present). Shadowing hardware calls with substitute functions ")
    from sim_ezblock import *

logging_format = "%( asctime)s: %( message)s"
# logging.basicConfig(format=logging_format , level=logging.INFO , datefmt ="%H:%M:%S")
logging.getLogger ().setLevel(logging.DEBUG)



class Picarx(object):
    PERIOD = 4095
    PRESCALER = 1
    TIMEOUT = 0.02

    def __init__(self):
        atexit.register(self.cleanup)
        self.dir_servo_pin = Servo(PWM('P2'))
        self.config_flie = fileDB('/home/nidhi/.config')
        dir_cal_value = int(self.config_flie.get("picarx_dir_servo", default_value=0))
        self.dir_servo_pin.angle(dir_cal_value)


        self.left_rear_pwm_pin = PWM("P13")
        self.right_rear_pwm_pin = PWM("P12")
        self.left_rear_dir_pin = Pin("D4")
        self.right_rear_dir_pin = Pin("D5")

        #
        self.S0 = ADC('A0')
        # self.S1 = ADC('A1')
        # self.S2 = ADC('A2')

        self.motor_direction_pins = [self.left_rear_dir_pin, self.right_rear_dir_pin]
        self.motor_speed_pins = [self.left_rear_pwm_pin, self.right_rear_pwm_pin]
        # self.cali_dir_value = self.config_flie.get("picarx_dir_motor", default_value="[1,1]")
        # self.cali_dir_value = [int(i.strip()) for i in self.cali_dir_value.strip("[]").split(",")]
        self.cali_speed_value = [0, 0]
        self.dir_current_angle = 0
        #初始化PWM引脚
        for pin in self.motor_speed_pins:
            pin.period(self.PERIOD)
            pin.prescaler(self.PRESCALER)

    def set_motor_speed(self,motor,speed):
        # global cali_speed_value,cali_dir_value
        self.cali_speed_value = [0, 0]
        cali_dir_value = self.config_flie.get("picarx_dir_motor", default_value="[1,1]")
        cali_dir_value = [int(i.strip()) for i in cali_dir_value.strip("[]").split(",")]

        motor -= 1
        if speed >= 0:
            direction = 1 * cali_dir_value[motor]
        elif speed < 0:
            direction = -1 * cali_dir_value[motor]
        speed = abs(speed)
        if speed != 0:
            speed = int(speed /2 ) + 50
        speed = speed - self.cali_speed_value[motor]
        if direction < 0:
            self.motor_direction_pins[motor].high()
            self.motor_speed_pins[motor].pulse_width_percent(speed)
        else:
            self.motor_direction_pins[motor].low()
            self.motor_speed_pins[motor].pulse_width_percent(speed)

    def motor_speed_calibration(self,value):
        # global cali_speed_value,cali_dir_value
        cali_speed_value = value
        if value < 0:
            cali_speed_value[0] = 0
            cali_speed_value[1] = abs(cali_speed_value)
        else:
            cali_speed_value[0] = abs(cali_speed_value)
            cali_speed_value[1] = 0
        return cali_speed_value

    def motor_direction_calibration(self,motor, value):
        # 0: positive direction
        # 1:negative direction
        # global cali_dir_value
        motor -= 1
        if value == 1:
            cali_dir_value[motor] = -1 * cali_dir_value[motor]
        self.config_flie.set("picarx_dir_motor", cali_dir_value)


    def dir_servo_angle_calibration(self,value):
        # global dir_cal_value
        #self.dir_cal_value = value
        print("calibrationdir_cal_value:",value)
        self.config_flie.set("picarx_dir_servo", "%s"%value)
        self.dir_servo_pin.angle(value)

    def set_dir_servo_angle(self,value):
        # global dir_cal_value
        self.dir_current_angle = value
        dir_cal_value = int(self.config_flie.get("picarx_dir_servo", default_value=0))
        angle_value  = value + dir_cal_value
        print("angle_value:",angle_value)
        # print("set_dir_servo_angle_1:",angle_value)
        # print("set_dir_servo_angle_2:",dir_cal_value)
        self.dir_servo_pin.angle(angle_value)


    # def get_adc_value(self):
    #     adc_value_list = []
    #     adc_value_list.append(self.S0.read())
    #     adc_value_list.append(self.S1.read())
    #     adc_value_list.append(self.S2.read())
    #     return adc_value_list

    def set_power(self,speed):
        self.set_motor_speed(1, speed)
        self.set_motor_speed(2, speed)

    def backward(self,speed):
        current_angle = self.dir_current_angle
        if current_angle != 0:
            abs_current_angle = abs(current_angle)
            # if abs_current_angle >= 0:
            if abs_current_angle > 40:
                abs_current_angle = 40
            power_scale = (100 - abs_current_angle) / 100.0
            print("power_scale:",power_scale)
            if (current_angle / abs_current_angle) > 0:
                self.set_motor_speed(1, -1*speed)
                self.set_motor_speed(2, speed * power_scale)
            else:
                self.set_motor_speed(1, -1*speed * power_scale)
                self.set_motor_speed(2, speed )
        else:
            self.set_motor_speed(1, -1*speed)
            self.set_motor_speed(2, speed)

    def forward(self,speed):
        current_angle = self.dir_current_angle
        if current_angle != 0:
            abs_current_angle = abs(current_angle)
            # if abs_current_angle >= 0:
            if abs_current_angle > 40:
                abs_current_angle = 40
            power_scale = (100 - abs_current_angle) / 100.0
            print("power_scale:",power_scale)
            if (current_angle / abs_current_angle) > 0:
                self.set_motor_speed(1, speed)
                self.set_motor_speed(2, -1*speed * power_scale)
            else:
                self.set_motor_speed(1, speed * power_scale)
                self.set_motor_speed(2, -1*speed )
        else:
            self.set_motor_speed(1, speed)
            self.set_motor_speed(2, -1*speed)

    def stop(self):
        self.set_motor_speed(1, 0)
        self.set_motor_speed(2, 0)


    def cleanup(self):
        self.stop()



if __name__ == "__main__":
    px = Picarx()
    px.forward(50)
    time.sleep(1)
    px.stop()
