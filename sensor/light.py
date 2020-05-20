#!/usr/bin/python
# import libraries
import smbus
import time

# Define some constants from the datasheet
DEVICE = 0x23  # Default device I2C address
POWER_DOWN = 0x00  # No active state
POWER_ON = 0x01  # Power on
RESET = 0x07  # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

samples = 100  # type: int
light_values = []


def convert_to_number(data):
    # Simple function to convert 2 bytes of data
    # into a decimal number. Optional parameter 'decimals'
    # will round to specified number of decimal places.
    result = round(((data[1] + (256 * data[0])) / 1.2), 1)
    return result


def load_data(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, CONTINUOUS_LOW_RES_MODE)
    if data:
        data = convert_to_number(data)
        return data
    return None


def read_data():
    data = None
    while data is None:
        try:
            data = load_data()
        except:
            pass
    if data:
        return data


def read_light():
    # take the average of the samples
    for x in range(1, samples):
        # Read data from I2C interface
        data = read_data()
        if data and len(light_values) < samples:
            light_values.append(data)
        # get the average of all the samples
        if len(light_values) == samples:
            light = round(sum(light_values) / len(light_values), 1)
            return light
        time.sleep(2)
    print('**** Sensor did not respond!! ****')
    return False
