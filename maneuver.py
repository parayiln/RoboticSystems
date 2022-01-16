import picarx_improved
from picarx_improved import Picarx
import time
import atexit

def inLine(px,dir,ang):
        px.dir_servo_angle_calibration(0)
        px.set_dir_servo_angle(ang)
        if dir== "forward":
            px.forward(50)
        else:
            px.backward(50)
        time.sleep(1)

def parallelPark(px):
    px.stop()
    px.backward(50)
    time.sleep(.5)
    px.set_dir_servo_angle(60)
    time.sleep(1)
    px.set_dir_servo_angle(-60)
    time.sleep(1)
    px.stop()

def Kturning(px,dir):
    if dir =='l':
        flag=-1
    else:
        flag=1
    px.set_dir_servo_angle(40*flag)
    px.forward()
    px.stop()
    px.backward()
    time.sleep(1.8)
    px.stop()
    px.set_dir_servo_angle(40*flag)
    px.forward()
    time.sleep(1.2)
    px.stop()


if __name__ == "__main__":
    px = Picarx()
    px.dir_servo_angle_calibration(0)
    px.set_dir_servo_angle(0)
    px.forward(50)
    time.sleep(1)
    px.stop()


    ########## code for maneuvering ###########
    print("plase select an action a- straight line, b -parking, c- K turning")
    choice=input()
    if choice=="a":
        angle=10
        dir="forward"
        inLine(px,dir,angle)
    elif choice=="b":
        parallelPark(px)
    else:
        Kturing(px)

    atexit.register(px.stop)
    atexit.register(print, "Exited")
