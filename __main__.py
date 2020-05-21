#!/usr/bin/python
import time
import datetime
import smbus2
import bme280
import asyncio
from display import OLED_Driver
from gpiozero import Button, OutputDevice
from PIL import ImageDraw, Image, ImageFont
from sensor import light as lux
from sensor import sunriseandset

# ---------------------------------Configuration--------------------------------- #
# the runtime of the actuator
actuator_duration = 20
# max allowable temp
upper_temp = 24
# lowest allowable temp
lower_temp = 22
# find the mean of thresholds
desired_temp = lower_temp + ((upper_temp - lower_temp) / 2)
# light thresholds for closing / opening the door
lower_light = 500
upper_light = 600
# button
button = Button(11)
# door power actuator
door_power = OutputDevice(5, active_high=True, initial_value=False)
# actuator bi polar connections
door_a = OutputDevice(26, active_high=True, initial_value=False)
door_b = OutputDevice(19, active_high=True, initial_value=False)
# heating and cooling relays
cooling = OutputDevice(13, active_high=True, initial_value=False)
heating = OutputDevice(6, active_high=True, initial_value=False)


async def init_display():
    OLED = OLED_Driver.OLED()
    OLED_ScanDir = OLED_Driver.SCAN_DIR_DFT  # SCAN_DIR_DFT = D2U_L2R
    OLED.OLED_Init(OLED_ScanDir)
    await asyncio.sleep(0.001)
    return OLED


async def update_display(OLED, message):
    if OLED:
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
    print(message)


async def get_environment():
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)
    params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, params)
    if data:
        return data
    print('Something went wrong')


# button control
async def button_pushed():
    print('Button pushed! \n')
    # remove power from actuator relays
    if door_power.on():
        door_power.off()
    await asyncio.sleep(0.1)
    # flip the phase
    door_a.toggle()
    door_b.toggle()
    await asyncio.sleep(0.1)
    # power it on
    if door_power.off():
        door_power.on()
    await asyncio.sleep(20)
    door_power.off()


def btn_push():
    btn_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(btn_loop)
    future = asyncio.ensure_future(button_pushed())
    btn_loop.run_until_complete(future)
    btn_loop.close()


async def main():
    # main loop
    print('Main loop initialized')
    print('Target Temp: ' + str(desired_temp))
    OLED = await asyncio.create_task(init_display())
    # get sunrise and sunset times
    sun = sunriseandset.sunrise_sunset()
    while True:
        # get current time
        date_time = time.strftime("%b %d %Y %H:%M")
        print(date_time)
        button.when_activated = btn_push
        print('Door relay power:' + str(door_power.value))
        print('Door relay A:' + str(door_a.value))
        print('Door relay B:' + str(door_b.value))
        # read the environmental sensors
        env = asyncio.create_task(get_environment())
        await asyncio.wait([env])

        # assign variables and round
        temp = round((env.result()).temperature, 1)
        humid = round((env.result()).humidity, 1)

        await asyncio.sleep(0.0001)
        # open the door at sunrise
        if str(sun['sunrise']) == time.strftime("%H:%M"):
            # open the door
            print('sunrise, opening door...')
            await asyncio.create_task(button_pushed())
        if str(sun['sunset']) == time.strftime("%H:%M"):
            # close the door
            print('sunset, closing door...')
            await asyncio.create_task(button_pushed())
        if temp < lower_temp:
            heating.on()
            print('heating')
        elif desired_temp <= temp <= upper_temp:
            heating.off()
            cooling.off()
        elif temp > upper_temp:
            cooling.on()
            print('cooling')
        await asyncio.sleep(0.0001)
        # create message for display
        message = {
            'temp': str(temp) + ' ' + u"\u00b0" + 'C',
            'humid': str(humid) + ' ' + u"\u0025",
            'button': str(door_a.value),
            'datetime': date_time,
        }

        # update the display
        asyncio.create_task(update_display(OLED, message))
        # loop every 5 seconds
        await asyncio.sleep(2)


# main init
if __name__ == "__main__":
    try:
        print('Welcome')
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
    except Exception as e:
        print('Exception: ' + str(e))
        # catch errors
        pass
    finally:
        print('close program')
        asyncio.get_running_loop().close()
