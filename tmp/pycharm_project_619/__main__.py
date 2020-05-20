import asyncio
import time
from gpiozero import Button, OutputDevice
from sensor import environment as env
from sensor import light as lux
from display import display
import datetime


# init display
screen = display.init_display()

# light variables
light = 0
upper_lux = 20

# temp variables
temp = 0
upperTemp = 24
lowerTemp = 22
desiredTemp = lowerTemp + ((upperTemp - lowerTemp) / 2)
print('Target Temp: ' + str(desiredTemp))

# button
button = Button(11)

# actuator relays
door_power = OutputDevice(5, active_high=True, initial_value=False)
door_a = OutputDevice(26, active_high=True, initial_value=False)
door_b = OutputDevice(19, active_high=True, initial_value=False)

# heating and cooling relays
cooling = OutputDevice(13, active_high=True, initial_value=False)
heating = OutputDevice(6, active_high=True, initial_value=False)


# button control
def button_pushed():
    print('Button pushed! \n')
    if door_power.value is 1:
        act_reverse()
    door_power.on()
    time.sleep(20)
    door_power.off()


# actuator reverse
def act_reverse():
    # remove power from actuator relays
    door_power.off()
    time.sleep(0.2)
    # toggle polarity of actuator
    door_b.toggle()
    door_a.toggle()
    # wait actuator to extend / retract
    time.sleep(20)
    # remove power
    door_power.off()


async def main():


    print('Door relay power:' + str(doorPower.value))
    print('Door relay A:' + str(doorA.value))
    print('Door relay B:' + str(doorB.value))
    # get current time
    date_time = time.strftime("%b %d %Y %H:%M")
    button.when_activated = button_pushed
    # get the current light level

    light = lux.read_light()
    # get the current temp
    temp = env.read_temp()
    # get the humidity
    humid = env.read_humidity()

    # create temperature message for display
    message = {
        'temp': str(temp) + ' ' + u"\u00b0" + 'C',
        'humid': str(humid) + ' ' + u"\u0025",
        'light': str(light),
        'button': str(door_a.value),
        'datetime': date_time,
    }
    # update the display
    display.update_text(screen, message)


# main init
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.set_debug(1)
        loop.run_until_complete(main())
    except Exception as e:
        # logging...etc
        pass
    finally:
        loop.close()
