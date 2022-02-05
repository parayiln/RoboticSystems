# week4
from buss import buss
import sys
sys.path.append(r'/home/nidhi/RoboticSystems/lib/')
from sensing_control import Sensing, Interpretation, Controller
import time
import concurrent.futures


def producer(sense_bus, delay):
    sense = Sensing()
    while True:
        data_read = sense.sensing()
        sense_bus.write(data_read)
        time.sleep(delay)

def consumer_producer(sense_bus, process_bus, delay):
    infer = Interpretation()
    while True:
        data_read_cp = sense_bus.read()
        data_process_cp = infer.processing(data_read_cp)
        process_bus.write(data_process_cp)
        time.sleep(delay)


def consumer(process_bus, delay):
    control = Controller()
    while True:
        data_process = process_bus.read()
        control.move(data_process)
        time.sleep(delay)


if __name__ == "__main__":
    sense_bus = buss()
    process_bus = buss()
    sense_delay=1
    process_delay=1
    control_delay=1
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            eSense = executor.submit(producer, sense_bus, sense_delay)
            eProcess = executor.submit(consumer_producer,sense_bus, process_bus, process_delay)
            eControl = executor.submit(consumer, process_bus, control_delay)
        # eSense.result()
    except:
        print("Something else went wrong")
