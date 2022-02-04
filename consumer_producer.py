
from buss import buss
import sys
sys.path.append(r'/home/nidhi/RoboticSystems')
from sensing_control import Sensing, Interpretation, Controller
import time
import concurrent.futures


def producer(buss, delay):
    while True:
        data_read = sense.sensing()
        sense_bus.write(data_read)
        time.sleep(delay)

def consumer_producer(buss, delay):
    while True:
        data_read = sense_bus.read()
        data_pocess = process.Processing(data_read)
        process_bus.write(data_process)
        time.sleep(delay)


def consumer(buss, delay):
    while True:
        data_process = process_bus.read()
        control.move(data_pocess)
        time.sleep(delay)   


if __name__ == "__main__":
    sense = Sensing()
    process = Interpretation()
    control = Controller()
    sense_bus = Bus([1, 1, 1])
    process_bus = Bus(0)

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            eSense = executor.submit(producer, sense_bus, sense)
            eProcess = executor.submit(consumer_producer, sense_bus, process_bus, process)
            eControl = executor.submit(consumer, process_bus, control)
        eSensor.result ()
