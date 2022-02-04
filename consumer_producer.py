
from buss import buss
import sys
sys.path.append(r'/home/nidhi/RoboticSystems/lib/')
from sensing_control import Sensing, Interpretation, Controller
import time
import concurrent.futures


def producer(buss, delay):
    while True:
        data_read = sense.sensing()
        print(data_read)
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
    sense_bus = buss([1, 1, 1])
    process_bus = buss(0)

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            print("enter")
            eSense = executor.submit(producer,.2, sense_bus, sense)
            eProcess = executor.submit(consumer_producer,.2, sense_bus, process_bus, process)
            eControl = executor.submit(consumer,.2, process_bus, control)
        eSense.result()
    except:
        print("Something else went wrong")
