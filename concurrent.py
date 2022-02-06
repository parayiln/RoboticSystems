# week 5

import sys
from sensing_control import Sensing, Interpretation, Controller
import rossros as ros
from sensing_control_ultasonic import SensingUltra, InterpretationUltra, ControllerUltra



if __name__=='__main__':
    Sensor = Sensing()
    SensorU= SensingUltra()
    Process = Interpretation()
    ProcessU = InterpretationUltra()
    Control = Controller()
    ControlU = ControllerUltra()

    sense_bus=ros.Bus()
    process_bus=ros.Bus()
    senseU_bus=ros.Bus()
    processU_bus=ros.Bus()
    termination_bus = ros.Bus()

    delay=.01

    sense_p = ros.Producer(Sensor.sensing, sense_bus, delay, termination_bus, 'sense line')
    process_cp = ros.ConsumerProducer(Process.processing, sense_bus, process_bus, delay, termination_bus, 'process line')
    control_c= ros.Consumer(Control.move, process_bus, delay, termination_bus, 'control line follower')

    sense_u_p = ros.Producer(SensorU.sensing, senseU_bus, delay, termination_bus, 'sense object')
    process_u_cp = ros.ConsumerProducer(ProcessU.processing, senseU_bus, processU_bus, delay, termination_bus, 'process object')
    control_u_c = ros.Consumer(ControlU.stop_move, processU_bus, delay, termination_bus, 'stop if object')

    time = ros.Timer(termination_bus, 5, 0.01, term_bus, "Timer")

    try:
        ros.runConcurrently([sense_p, sense_u_p, process_cp, process_u_cp, control_c, control_u_c, time.timer()])
    except:
        print("Someting is wrong, exiting code")
