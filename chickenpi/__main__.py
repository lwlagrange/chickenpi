import time
import RPi.GPIO as GPIO

from sensor import environment as env
from sensor import light as lux
from sensor import realtime as rtc

# main init
if __name__ == '__main__':

    # setup IO pin mode
    GPIO.setmode(GPIO.BOARD)

    # create a dictionary of the pin assignments
    pins = {'open': 31, 'close': 33, 'cool': 35, 'heat': 37}

    # light variables
    light = 0
    upperLux = 20

    # temp variables
    temp = 0
    upperTemp = 25
    lowerTemp = 22

    # iterate through the list of pins
    for pin in pins.values():
        GPIO.setup(pin, GPIO.OUT)

    while True:
        # get the current temp
        temp = env.read_temp()
        # get the current light level
        light = lux.read_light()

        if temp < lowerTemp:
            print 'heating..\n'
            GPIO.output(pins['heat'], 1)
        else:
            GPIO.output(pins['heat'], 0)

        if temp > upperTemp:
            print 'cooling.. \n'
            GPIO.output(pins['cool'], 1)
        else:
            GPIO.output(pins['cool'], 0)

        if light > upperLux:
            GPIO.output(pins['open'], 1)
            GPIO.output(pins['close'], 1)

        else:
            GPIO.output(pins['open'], 0)
            GPIO.output(pins['close'], 0)

        # Updated every 30 sec
        time.sleep(2)