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
async def button_pushed():
    print('Button pushed! \n')
    if door_power.value is 1:
        act_reverse()
    door_on = door_power.on()
    time.sleep(20)
    door_power.off()
    await asyncio.sleep(0.00001)


# actuator reverse
async def act_reverse():
    # remove power from actuator relays
    door_power.off()
    await asyncio.sleep(0.001)
    # toggle polarity of actuator
    door_b.toggle()
    door_a.toggle()
    # wait actuator to extend / retract
    await asyncio.sleep(20)
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

    light = loop.create_task(lux.read_light())
    # get the current temp
    temp = loop.create_task(env.read_temp())
    # get the humidity
    humid = loop.create_task(env.read_humidity())

    # create temperature message for display
    message = {
        'temp': str(temp) + ' ' + u"\u00b0" + 'C',
        'humid': str(humid) + ' ' + u"\u0025",
        'light': str(light),
        'button': str(door_a.value),
        'datetime': date_time,
    }
    # update the display
    update_screen = loop.create_task(display.update_text(screen, message))

    await asyncio.wait([temp, light, humid, update_screen])
    return temp, light, humid


# main init
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.set_debug(1)
        loop.run_forever(main())
    except Exception as e:
        # logging...etc
        pass
    finally:
        loop.close()




esult = []
    samples = 10
    for i in range(samples):
        value = 1
        if sensor_type == 'temp':
            value = env.read_temp()
            result.append(value)
            await asyncio.sleep(0.0001)
        elif sensor_type == 'humid':
            value = env.read_humidity()
            result.append(value)
            await asyncio.sleep(0.0001)
    await asyncio.wait(result)
    print(result)
    return result

import time
from gpiozero import Button, OutputDevice
from sensor import environment as env
from sensor import light as lux
from display import display
import datetime


async def main():


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
    desiredTemp = lowerTemp + ((upperTemp - lowerTemp) / 2)
    print('Target Temp: ' + str(desiredTemp))
    # button
    button = Button(11)
    # actuator relays
    doorA = OutputDevice(26, active_high=True, initial_value=False)
    doorB = OutputDevice(19, active_high=True, initial_value=False)
    # heating and cooling relays
    cooling = OutputDevice(13, active_high=True, initial_value=False)
    heating = OutputDevice(6, active_high=True, initial_value=False)


    async def button_pushed():
        print('Button pushed! \n')
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
            print('Heating...\n')
            heating.on()
        else:
            heating.off()

        # create temperature message for display

        import smbus2
        import bme280

        port = 1
        address = 0x76
        bus = smbus2.SMBus(port)

        calibration_params = bme280.load_calibration_params(bus, address)

        # the sample method will take a single reading and return a
        # compensated_reading object
        data = bme280.sample(bus, address, calibration_params)

        # the compensated_reading class has the following attributes
        print(data.id)
        print(data.timestamp)
        print(data.temperature)
        print(data.pressure)
        print(data.humidity)

        # there is a handy string representation too
        print(data)

        # -*- coding:UTF-8 -*-
        import DEV_Config
        import OLED_Driver

        from PIL import ImageDraw, Image, ImageFont


        def load_data():
            OLED = OLED_Driver.OLED()
            OLED_ScanDir = OLED_Driver.SCAN_DIR_DFT  # SCAN_DIR_DFT = D2U_L2R
            OLED.OLED_Init(OLED_ScanDir)
            return OLED


        def init_display():
            OLED_data = None
            while OLED_data is None:
                try:
                    OLED_data = load_data()
                    print
                    'loading OLED data'
                except:
                    pass
            if OLED_data:
                return OLED_data


        def update_text(OLED, message):
            if OLED:
                print
                'updating text'
                image = Image.new("L", (OLED.OLED_Dis_Column, OLED.OLED_Dis_Page), 0)
                draw = ImageDraw.Draw(image)
                reading = ImageFont.truetype('/usr/share/fonts/truetype/Arial.ttf', 36)
                title = ImageFont.truetype('/usr/share/fonts/truetype/Arial.ttf', 22)
                draw.text((0, 0), 'ChickenPi', font=title, fill="White")
                draw.text((104, 10), 'v1.2', fill="White")
                draw.text((0, 25), message['datetime'], fill="White")
                draw.text((0, 40), 'Temperature', fill="White")
                draw.text((0, 48), message['temp'], font=reading, fill="White")
                draw.text((0, 82), 'Humidity', fill="White")
                draw.text((0, 88), message['humid'], font=reading, fill="White")
                OLED.OLED_ShowImage(image, 0, 0)
            else:
                # try initializing the screen again
                print
                'initializing display'
                init_display()






# button control
async def button_pushed():
    print('Button pushed! \n')
    # remove power from actuator relays
    power_off = door_power.off()
    await asyncio.wait(power_off)
    # flip the phase
    door_a.toggle()
    door_b.toggle()
    await asyncio.sleep(0.0001)
    # power it on
    door_power.on()
    # wait actuator to extend / retract
    await asyncio.sleep(actuator_duration)
    # remove power
    door_power.off()
    await asyncio.sleep(0.001)


def btn_push():
    btn_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(btn_loop)
    future = asyncio.ensure_future(button_pushed())
    btn_loop.run_until_complete(future)
    btn_loop.close()