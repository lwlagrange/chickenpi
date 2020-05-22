#!/usr/bin/python
import time
import datetime
import smbus2
import bme280
import asyncio
from display import OLED_Driver
from gpiozero import Button, OutputDevice
from PIL import ImageDraw, Image, ImageFont
from sensor import sunriseandset

# ---------------------------------Configuration--------------------------------- #
# the runtime of the actuator
actuator_duration = 20
# max allowable temp
fan_on = 30
fan_off = 25
heat_on = 17
heat_off = 22
# light thresholds for closing / opening the door
lower_light = 500
upper_light = 600
# button
button = Button(11)
# door power actuator
door_power = OutputDevice(5, active_high=True, initial_value=False)
door_a = OutputDevice(26, active_high=True, initial_value=False)
door_b = OutputDevice(19, active_high=True, initial_value=False)
# relays
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
    try:
        bus = smbus2.SMBus(port)
        params = bme280.load_calibration_params(bus, address)
        data = bme280.sample(bus, address, params)
        return data
    except ValueError as err:
        print('Something went wrong' + str(err))


async def rev():
    door_a.toggle()
    door_b.toggle()
    print('reverse')


async def power():
    door_power.off()
    await asyncio.sleep(0.001)
    door_power.on()
    await asyncio.sleep(actuator_duration)
    door_power.off()
    print('power')


async def door():
    await asyncio.gather(
        power(),
        rev(),
    )


async def heat(temp):
    print(f"Heating..{temp}")


async def cool(temp):
    print(f"Cooling..{temp}")


def btn_push():
    btn_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(btn_loop)
    btn_future = asyncio.ensure_future(door())
    btn_loop.run_until_complete(btn_future)
    btn_loop.close()


async def main():
    # main loop
    OLED = await asyncio.create_task(init_display())
    # get sunrise and sunset times
    sun = sunriseandset.sunrise_sunset()

    while True:
        # read the environmental sensors
        env = await asyncio.create_task(get_environment())
        # assign variables and round
        temp = round(env.temperature, 1)
        humid = round(env.humidity, 1)
        await asyncio.sleep(0.0001)
        # get current time
        date_time = time.strftime("%b %d %Y %H:%M")
        button.when_activated = btn_push
        await asyncio.gather(
            cool(temp),
            heat(temp)
        )
        await asyncio.sleep(2)


asyncio.run(main())
