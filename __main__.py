#!/usr/bin/python
import smbus2
import bme280
import asyncio
import display
import gpiozero
import datetime


async def update_display():
    print('update the display')
    # init display
    screen = display.init_display()
    message = {'temp': str(temp) + ' ' + u"\u00b0" + 'C', 'humid': str(humid) + ' ' + u"\u0025", 'datetime': date_time}
    # update the display
    display.update_text(screen, message)


async def get_environment():
    print('getting environment...')
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)
    params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, params)
    if data:
        return data
    print('Something went wrong')


async def main():
    # main loop
    print('Main loop initialized')
    try:
        # read the environmental sensors
        env = loop.create_task(get_environment())
        await asyncio.wait([env])
        temp = round((env.result()).temperature, 1)
        print('temperature is: {}'.format(temp))
        humid = round((env.result()).humidity, 1)
        print('humidity is: {}'.format(humid))
    except Exception as e:
        print('something went wrong')


# main init
if __name__ == "__main__":
    try:
        print('Welcome')
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
        loop.set_debug(1)
    except Exception as e:
        print('errors or exceptions: ' + str(e))
        # catch errors
        pass
    finally:
        print('close program')
        loop.close()
