import time
import RPi.GPIO as GPIO

from sensor import environment as env
from sensor import light as lux
from sensor import realtime as rtc

# main init
if __name__ == '__main__':

    def button_pushed(channel):
        print "rising edge detected on channel: " + str(channel) + "\n"

    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)  # setup IO pin mode
    outputs = {'open': 31, 'close': 33, 'cool': 35, 'heat': 37}  # create a dictionary of output pin assignments
    inputs = {'button': 15}  # create a dictionary of input pin assignments
    light = 0  # light variables
    upperLux = 20

    # temp variables
    temp = 0
    upperTemp = 20
    lowerTemp = 18
    nominalTemp = int(lowerTemp + ((upperTemp - lowerTemp) / 2))

    # iterate through the list of pins
    for pin_out in outputs.values():
        GPIO.setup(pin_out, GPIO.OUT)

    buttonState = 0

    GPIO.setup(inputs['button'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(inputs['button'], GPIO.RISING, callback=button_pushed, bouncetime=300)

    while True:
        # get the current temp
        temp = env.read_temp()

        if temp < lowerTemp:
            print 'heating..\n'
            print 'nominal temp is: ' + str(nominalTemp) + '\n'
            GPIO.output(outputs['heat'], 1)
        else:
            GPIO.output(outputs['heat'], 0)
        time.sleep(2)
