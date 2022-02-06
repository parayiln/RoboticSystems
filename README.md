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
- takes in the value sensing class values are return the approximate position of car.
- Also has a function to calibrate the sensor reading (Highly recommended when trying on new surfaces!)
- Sensitivity defines the threshold for dark vs light.
- position is estimated based on which sensor reading is from light or dark region.
- Polarity defines if the line is darker than background (polarity=1 by default) or vice versa (polarity=0)

Class Controller:
- Takes in the distance values from the Interpretation class and uses the value to control the steering angle of the car.



Note:
all there are tested for black tape. Please to the calibration for any other surface.
The speed is set to 30, worked best for the carpet I tested, do change the values if it does not work for you.

camera_linefolow.py:
-Code for lane following.
-Has two classes. One does all the sensing (of the two lanes, I used blue tapes for lanes), processing and results the steering angle.
- The other uses pycar_improved.py to move the car with constant speed of 30 (best speed for my carpet) with the steering angle given.



************************************************
Week 4 codes Modifications
*********************************************
buss.py
- has read, write methods, which reads and writes messages .

consumer_producer.py
- it has three types of functions: producer, consumer_producer and consumer.
- Has threading to run all the 3 functions in parallel

************************************************
Week 5 codes Modifications
*********************************************
Introducing rossros.py for Bus and Consumer-Producer

rossros.py
- developed by Prof. Hatton.
- contains Class Buss which can read and write messages
- Contains Class producer, consumer and Condumer-Producer.
  - Producer : takes in the Producer function (usually sensing), sensor bus, delay, termination bus and write the values to the sensor bus.
  - ConsumerProducer : takes in the ConsumerProducer  function (usually processing sensed data), sensor bus, processor bus,  delay, termination bus and reads the data from sensor bus to process and write it into the processor bus
  - Consumer : takes in the Consumer function (usually function to be executed ), processor bus,  delay, termination bus and reads the data  processor bus and executes action.

  sensing_control_ultrsonic.py
  - Has three classes sensing, interpretation and control similar to sensing_control.py
  - The sensing class reads the ultrasonic values.
  - Intrepretation class the provision to calibrate close distance value. The default value is 25. Processing method checks if the value is less that close distance and value and returns 0 or 1.
  - Control : check the close distance value and stops the car if its 0 else move forward with 30 speed.

  concurrency.py
  - Similar to the consumer_producer.py
  - uses the class from rossros.py and sensing_control_ultrsonic.py to implement threading
