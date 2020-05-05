import time
import RPi.GPIO as GPIO
from sensor import temp
from sensor import light

# main init
if __name__ == '__main__':

    # setup IO pin mode
    GPIO.setmode(GPIO.BOARD)

    # actuator open close
    GPIO.setup(31, GPIO.OUT)
    GPIO.setup(33, GPIO.OUT)
    # fan
    GPIO.setup(35, GPIO.OUT)
    # heater
    GPIO.setup(37, GPIO.OUT)

    while True:

        temp = temp.read_temp()
        lux = light.read_light()
        # debug temp
        # temp = 23  # type: int

        # f temp is below low limit
        if temp < 20:
            # turn on heater
            GPIO.output(37, 1)
            # turn off cooling fan
            GPIO.output(35, 0)
        elif temp > 22 & temp < 25:
            # turn off heater
            GPIO.output(37, 0)
            # turn off cooling fan
            GPIO.output(35, 0)
        elif temp > 25:
            # turn off heater
            GPIO.output(37, 0)
            # turn on cooling fan
            GPIO.output(35, 0)
        else:
            # turn off heater
            GPIO.output(37, 0)
            # turn off fan
            GPIO.output(35, 0)

        time.sleep(1)



import RPi.GPIO as GPIO

# here you would put all your code for setting up GPIO,
# we'll cover that tomorrow
# initial values of variables etc...
counter = 0

try:
    # here you put your main loop or block of code
    while counter < 9000000:
        # count up to 9000000 - takes ~20s
        counter += 1
    print "Target reached: %d" % counter

except KeyboardInterrupt:
    # here you put any code you want to run before the program
    # exits when you press CTRL+C
    print "\n", counter # print value of counter

except:
    # this catches ALL other exceptions including errors.
    # You won't get any error messages for debugging
    # so only use it once your code is working
    print "Other error or exception occurred!"

finally:
    GPIO.cleanup() # this ensures a clean exit




    GPIO.setup(33, GPIO.OUT)
    # fan
    GPIO.setup(35, GPIO.OUT)
    # heater
    GPIO.setup(37, GPIO.OUT)

    # if we are lower than the desired temp
    if temp < 25:
        # turn on heater
        print 'heater on..\n'
        GPIO.output(37, 1)
    elif temp > 23:
        GPIO.output(37, 0)
    elif temp > 25:
        GPIO.output(35, 1)
    else: