#!/usr/bin/python
import time
import datetime
import smbus2
import bme280
import asyncio
from gpiozero import Button, OutputDevice
from modules import sunriseandset
from modules import display

# ---------------------------------Configuration--------------------------------- #
# the runtime of the actuator
actuator_duration = 5
# max allowable temp
fan_on = 30
fan_off = 25
heat_on = 18
heat_off = 22
# light thresholds for closing / opening the door
lower_light = 500
upper_light = 600
# button
button = Button(11)
# door power actuator
door_state = False
door_power = OutputDevice(5, active_high=True, initial_value=False)
door_a = OutputDevice(26, active_high=True, initial_value=False)
door_b = OutputDevice(19, active_high=True, initial_value=False)
# relays
cooling = OutputDevice(13, active_high=True, initial_value=False)
heating = OutputDevice(6, active_high=True, initial_value=False)

# get sunrise and sunset times
sun = sunriseandset.sunrise_sunset()

# initialize the display
screen = display.screen()


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


async def heat(temp):
    if temp < heat_on:
        heating.on()
        print(f"Heating on..")
    elif heat_off > temp > heat_on:
        heating.on()
        print(f"Heating on..")
    elif heat_off > temp <= heat_off:
        print(f"Heating off..")
        heating.off()


async def cool(temp):
    if temp > fan_on:
        print('fan is on...')
        cooling.on()
    elif fan_on > temp > fan_off:
        print('fan is on...')
        cooling.on()
    elif fan_on > temp <= fan_off:
        print('fan is off')
        cooling.off()
    cooling.off()


async def rev():
    door_a.toggle()
    door_b.toggle()
    await asyncio.sleep(0.01)


async def power():
    door_power.off()
    await asyncio.sleep(0.01)
    door_power.on()


async def door():
    global door_state
    door_state = True
    await asyncio.gather(
        power(),
        rev()
    )


async def auto_door():
    sunset = str(sun['sunset'])
    sunrise = str(sun['sunrise'])
    print(f'door set to open at {sunrise} and close at {sunset}')
    curr_time = time.strftime("%H:%M")
    if curr_time == sunrise or curr_time == sunset:
        print(f"door was automatically activated at: {curr_time}")
        await door()


def btn_push():
    btn_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(btn_loop)
    btn_future = asyncio.ensure_future(door())
    btn_loop.run_until_complete(btn_future)
    btn_loop.close()


async def main():
    while True:
        print(f"door state: {door_state}")
        # get current time
        date_time = time.strftime("%b %d %Y %H:%M")
        button.when_activated = btn_push
        # read the environmental sensors
        env = await asyncio.create_task(get_environment())
        # assign variables and round
        temp = round(env.temperature, 1)
        humid = round(env.humidity, 1)
        message = {
            'temp': str(temp) + ' ' + u"\u00b0" + 'C',
            'humid': str(humid) + ' ' + u"\u0025",
            'button': str(door_a.value),
            'datetime': date_time
        }
        await asyncio.gather(
            cool(temp),
            heat(temp),
            auto_door()
        )

        display.update_display(screen, message)
        await asyncio.sleep(60)


asyncio.run(main())
