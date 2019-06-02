import time
import threading

import ICReaderProc
import DBProc
import ButtonProc
from DBProc import DEFINE_NUMS

class GPIO_NUM_DEF():
    RED_LED_GPIO = 18

if __name__ == "__main__":
    #from db.DBProc import DBProc
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_NUM_DEF.RED_LED_GPIO, GPIO.OUT)

    GPIO.output(GPIO_NUM_DEF.RED_LED_GPIO, 0)

    thread_1 = threading.Thread(target=ICReaderProc.ICReaderProc1)
    thread_2 = threading.Thread(target=DBProc.DBProc1)
    thread_3 = threading.Thread(target=ButtonProc.ButtonProc1)

    thread_1.start()
    thread_2.start()
    thread_3.start()
