#week2
import picarx_improved
from picarx_improved import Picarx
import time
import atexit

def inLine(px,dir,ang):
    # px.dir_servo_angle_calibration(0)
    px.set_dir_servo_angle(int(ang))
    if dir =='1':
        px.forward(30)
        time.sleep(3)
        px.stop()
    elif dir =='2':
        px.backward(30)
        time.sleep(3)
        px.stop()
    else:
        print("No direction chosen the car will move forward")
        px.forward(30)
        time.sleep(3)
        px.stop()

def parallelPark(px, dir):

    if dir =='1':
        flag=-1
    elif dir =='2':
        flag=1
    else:
        print("No direction chosen the car will turn left")
        flag=-1
    px.stop()
    px.set_dir_servo_angle(30*flag)
    px.stop()
    time.sleep(.01)
    px.backward(40)
    time.sleep(1.)
    px.stop()
    px.set_dir_servo_angle(-30*flag)
    time.sleep(.01)
    px.backward(40)
    time.sleep(1)
    px.stop()
    px.set_dir_servo_angle(0)
    time.sleep(1)
    px.forward(40)
    time.sleep(.1)
    px.stop()

def Kturning(px,dir):
    px.dir_servo_angle_calibration(0)
    if dir =='1':
        flag=-1
    elif dir =='2':
        flag=1
    else:
        print("No direction chosen the car will turn left")
        flag=-1
    px.set_dir_servo_angle(30*flag)
    px.forward(40)
    time.sleep(2)
    px.stop()
    px.set_dir_servo_angle(-30*flag)
    px.backward(40)
    time.sleep(1.8)
    px.stop()
    px.set_dir_servo_angle(15*flag)
    px.forward(40)
    time.sleep(1)
    px.stop()


if __name__ == "__main__":
    px = Picarx()
    px.dir_servo_angle_calibration(0)
    px.set_dir_servo_angle(0)

    atexit.register(px.stop)
    atexit.register(print, "Exited")
    while("True"):
        ########## code for maneuvering ###########
        print("plase select an action: a- straight line, b -parking, c- K turning or d- exit the code")
        choice=input()
        if choice=="a":
            print("Plese Select : 1 for forward , 2 for back")
            dir=input()
            print("please enter an angle")
            angle=input()
            inLine(px,dir,angle)
        elif choice=="b":
            print("Plese Select : 1 for left , 2 for right")
            dir=input()
            parallelPark(px,dir)
        elif choice=="c":
            print("Plese Select : 1 for left , 2 for right")
            dir=input()
            Kturning(px, dir)
        elif choice=="d":
            print("Exiting code! See you next time!")
            break
        else:
            print("You made a wrong selection please select again")
