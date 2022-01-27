Installation:
Install logdecorator : sudo pip3 install logdecorator
Install the picar-x libs using the link https://docs.sunfounder.com/projects/picar-x/en/latest/download_and_run_code.html

*****************************************
Week 2 codes Modifications
*********************************************
picarx_improved.py :
-contains both ezblock packages and shadow environment. (sim_ezblock is the setup for shadow environment)
-added the logging message for forward functions.
-added atextit to make sure the picar stops in case of any error.
-commented on the speed scaling part of the code to input the actual speed. -Calibrated the steering angle to 0 (I did not find any noticeable steering offset).
-tested this code and work fine.

maneuver.py:
-The code can command the car to drive in a straight line (forward or backward, w/wo steering angle), parallel parking (left or right) or 3 points turning. -Run the code and follow the instructions to move the car in the desired trajectory.
-Tested this code and works fine for all the trajectories.

motor_command.py
-Similar to picarx_improved.py with only the functions related to the motor commands but changed all the calibration-related global variable to local.
-Tested this code and worked fine.

Review inputs: Suggested to put all the lib files and give the path to the library.
                I could use the atextit inside the __init__() functions

************************************************
Week 3 codes Modifications
*********************************************

Made the changes suggested in the code review

sensing_control.py

Run this code to make the car follow a line either using the grayscale module (this is an IR sensor, works best for a back color line vs a lighter color or vise versa) or a camera.

Following is a brief description of the code, feel free to skip if you can understand the code.

Class Sensing:
- obtains the reading from grayscale module as a list called adc_value_list.

class Interpretation:
- taken in the value sensing class values are return the approximate position of car.
- Also has a function to calibrate the sensor reading (Highly recommended when trying on new surfaces!)
- Sensitivity defines the threshold for dark vs light.
- Polarity defines if the line is darker than background (polarity=1 by default) or vice versa (polarity=0)

Class Controller:
- Takes in the distance values from the Interpretation class and uses the value to control the steering angle of the car.
- Camera
