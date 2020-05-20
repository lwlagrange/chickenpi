#!/usr/bin/python
import time
import smbus
import bme280

port = 1
address = 0x76
bus = smbus.SMBus(port)


def load_data():
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)
    if data:
        return data
    print('**** Sensor did not respond ****\n')
    return None


# the sample method will take a single reading and return a
# compensated_reading object
def read_data():
    data = None
    while data is None:
        try:
            data = load_data()
        except:
            pass
    if data:
        return data
    return False


def read_temp():
    read = read_data()
    if read:
        temp = round(read.temperature, 1)
        print('Temperature: ' + str(temp))
        return temp
    else:
        return False


def read_pressure():
    read = read_data()
    if read:
        print('Pressure: ' + str(read.pressure))
        return read.pressure
    return False


def read_humidity():
    read = read_data()
    if read:
        humid = round(read.humidity, 1)
        print('Humidity: ' + str(humid))
        return humid
    return False
