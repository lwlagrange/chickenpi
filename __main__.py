import time
from gpiozero import Button, OutputDevice

from sensor import environment as env
from sensor import light as lux
from display import display
from sensor import realtime as rtc

# main init
if __name__ == '__main__':

    light = 0  # light variables
    upperLux = 20

    # temp variables
    temp = 0
    upperTemp = 24
    lowerTemp = 22
    desiredTemp = lowerTemp + (upperTemp - lowerTemp)

    button = Button(23)
    doorA = OutputDevice(6, active_high=True)
    doorB = OutputDevice(13, active_high=True)

    cooling = OutputDevice(19, active_high=True)
    heating = OutputDevice(26, active_high=True)


    def button_pushed():
        print 'Button pushed! \n'
        doorB.toggle()
        doorA.toggle()

    while True:
        button.when_activated = button_pushed
        # get the current light level
        light = lux.read_light()

        # get the current temp
        temp = env.read_temp()
        print 'The current temperature is: ' + str(temp)

        if int(temp) < lowerTemp:
            print 'Heating...\n'
            heating.on()
        else:
            heating.off()
        message = 'Temperature: ' + str(temp) + '\n' + ' Desired temperature: ' + str(desiredTemp) + '\n'

        time.sleep(2)

        # update the display
        screen = display.update_text(message)
