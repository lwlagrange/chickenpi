import time
import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)


# the sample method will take a single reading and return a
# compensated_reading object
def read_data():
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)
    if data:
        return data
    print('**** Sensor did not respond ****\n')
    return False


def read_temp():
    read = read_data()
    if read:
        temp = round(read.temperature, 2)
        print('Temperature: ' + str(temp) + '\n')
    return False


def read_pressure():
    read = read_data()
    if read:
        print('Pressure: ' + str(read.pressure) + '\n')
        return read.pressure
    return False


def read_humidity():
    read = read_data()
    if read:
        print('Pressure: ' + str(read.humidity) + '\n')
        return read.humidity
    return False
