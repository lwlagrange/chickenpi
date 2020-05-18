import time
from gpiozero import Button, OutputDevice
from sensor import environment as env
from sensor import light as lux
from display import display
import datetime

# main init
if __name__ == '__main__':

    # init display
    screen = display.init_display()

    # light variables
    light = 0
    upperLux = 20

    # temp variables
    temp = 0
    upperTemp = 24
    lowerTemp = 22
    desiredTemp = lowerTemp + ((upperTemp - lowerTemp)/2)
    print 'Target Temp: ' + str(desiredTemp)

    # button
    button = Button(11)

    # actuator relays
    doorA = OutputDevice(26, active_high=True, initial_value=False)
    doorB = OutputDevice(19, active_high=True, initial_value=False)

    # heating and cooling relays
    cooling = OutputDevice(13, active_high=True, initial_value=False)
    heating = OutputDevice(6, active_high=True, initial_value=False)


    def button_pushed():
        print 'Button pushed! \n'
        doorB.toggle()
        doorA.toggle()


    while True:
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
        message = {'temp': str(temp) + ' ' + u"\u00b0" + 'C', 'humid': str(humid) + ' ' + u"\u0025", 'datetime': date_time}
        # update the display
        display.update_text(screen, message)
        # update every 2 sec
        time.sleep(2)
