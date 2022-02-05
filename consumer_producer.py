
from buss import buss
import sys
sys.path.append(r'/home/nidhi/RoboticSystems/lib/')
from sensing_control import Sensing, Interpretation, Controller
import time
import concurrent.futures


def producer(sense_bus, delay, sense):
    while True:
        data_read = sense.sensing()
        sense_bus.write(data_read)
        time.sleep(delay)

def consumer_producer(sense_bus, process_bus, delay, process ):
    while True:
        print("enterd cp")
        data_read = sense_bus.read()
        print("read",data_read)
        data_pocess = process.Processing(data_read)
        process_bus.write(data_process)
        time.sleep(delay)


def consumer(process_bus, delay, control):
    while True:
        print("moving")
        data_process = process_bus.read()
        print(data_pocess)
        control.move(data_pocess)
        time.sleep(delay)


if __name__ == "__main__":
    sense = Sensing()
    process = Interpretation(sense)
    control = Controller(process)
    sense_bus = buss(0)
    process_bus = buss(0)
    sense_delay=.5
    process_delay=.5
    control_delay=.5
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            eSense = executor.submit(producer, sense_bus, sense_delay, sense)
            eProcess = executor.submit(consumer_producer, sense_bus, process_bus, process_delay, process)
            eControl = executor.submit(consumer, process_bus, control_delay, control)
        # eSense.result()
    except:
        print("Something else went wrong")
