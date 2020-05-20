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

        # get the current light level
        # light = lux.read_light()
        if light > upperLux:
            GPIO.output(outputs['open'], 1)
            GPIO.output(outputs['close'], 1)

            GPIO.add_event_detect(inputs['button'], GPIO.BOTH)  # add rising edge detection to button
            if GPIO.event_detected(inputs['button']):
                print('Button pressed')

            if GPIO.input(inputs['button']):

                GPIO.output(outputs['open'], 1)
                GPIO.output(outputs['close'], 1)

            else:
                GPIO.output(outputs['open'], 0)
                GPIO.output(outputs['close'], 0)

            # iterate through the list of pins
        for pin in outputs.values():
            GPIO.setup(pin, GPIO.OUT)

        # GPIO.setup(inputs['button'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # GPIO.add_event_detect(inputs['button'], GPIO.RISING, callback=button_pushed(this, button_state), bouncetime=300)


        if temp < lowerTemp:
            print 'Temperature is:' + str(temp) + '\n'
            print 'heating..\n'
            print 'nominal temp is: ' + str(nominalTemp) + '\n'
            GPIO.output(outputs['heat'], 1)
        else:
            GPIO.output(outputs['heat'], 0)

            GPIO.setwarnings(False)  # Ignore warning for now
            GPIO.setmode(GPIO.BOARD)  # setup IO pin mode
            outputs = {'open': 31, 'close': 33, 'cool': 35, 'heat': 37}  # create a dictionary of output pin assignments
             5 6 13 19
            while True:
                if button.is_active:
                    print('Button Pushed!')
                # get the current temp
                temp = env.read_temp()
                if int(temp) < lowerTemp:
                    print 'Heating...\nThe current temperature is: ' + str(temp)
                    GPIO.output(outputs['heat'], 1)
                    time.sleep(2)
                else:
                    GPIO.output(outputs['heat'], 0)
                    time.sleep(2)

# while True:
# print relay states
print 'Door relay power:' + str(doorPower.value)
print 'Door relay A:' + str(doorA.value)
print 'Door relay B:' + str(doorB.value)
# get current time
date_time = time.strftime("%b %d %Y %H:%M")
button.when_activated = button_pushed
# get the current light level

light = lux.read_light()
# get the current temp
temp = env.read_temp()
# get the humidity
humid = env.read_humidity()
if int(temp) < lowerTemp:
    print 'Heating...\n'
    heating.on()
else:
    heating.off()
# create temperature message for display
message = {'temp': str(temp) + ' ' + u"\u00b0" + 'C', 'humid': str(humid) + ' ' + u"\u0025",
           'datetime': date_time}
# update the display
display.update_text(screen, message)
# update every 2 sec
time.sleep(2)





result = None
    while result is None:
        try:
            # read data
            result = read_data()
        except:
            pass









# get the average of all the samples
        light = round(sum(light_values) / len(light_values), 1)
        print('light: ' + str(light))
        return light