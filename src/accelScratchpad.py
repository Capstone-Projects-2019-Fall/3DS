import smbus2 as smbus
import time
import numpy

# Function to read acceleration data from accelerometer
def readData():
    # Read data back from 0x32(50), 2 bytes
    # X-Axis LSB, X-Axis MSB
    data0 = bus.read_byte_data(0x53, 0x32)
    data1 = bus.read_byte_data(0x53, 0x33)

    # Convert the data to 10-bits
    xAccl = ((data1 & 0x03) * 256) + data0
    if xAccl > 511 :
        xAccl -= 1024

    # Read data back from 0x34(52), 2 bytes
    # Y-Axis LSB, Y-Axis MSB
    data0 = bus.read_byte_data(0x53, 0x34)
    data1 = bus.read_byte_data(0x53, 0x35)

    # Convert the data to 10-bits
    yAccl = ((data1 & 0x03) * 256) + data0
    if yAccl > 511 :
        yAccl -= 1024

    # Read data back from 0x36(54), 2 bytes
    # Z-Axis LSB, Z-Axis MSB
    data0 = bus.read_byte_data(0x53, 0x36)
    data1 = bus.read_byte_data(0x53, 0x37)

    # Convert the data to 10-bits
    zAccl = ((data1 & 0x03) * 256) + data0
    if zAccl > 511 :
        zAccl -= 1024

    # Convert whatever unit this is to m/s^2
#    print (xAccl, ", ", yAccl, ", ", zAccl)
    xms = xAccl / 250 * 9.8
    yms = yAccl / 250 * 9.8
    zms = zAccl / 250 * 9.8

    # Output data to screen - debugging
#     print ("Acceleration in X-Axis : ", xms, "m/s^2")
#     print ("Acceleration in Y-Axis : ", yms, "m/s^2")
#     print ("Acceleration in Z-Axis : ", zms, "m/s^2")

    accel = numpy.array([xms, yms])
    t = numpy.linalg.norm(accel)
    
    return xms, yms, t
# end of readData()

def calculateVelocity(oldV):
    delT = 0.5
    a = t
    v = oldV + (a * delT)
    return v

# Setup
# Get I2C bus
bus = smbus.SMBus(1)

# ADXL345 accelerometer address is 0x53(83)

# Select bandwidth rate register, 0x2C(44)
#       0x0A(10)    Normal mode, Output data rate = 100 Hz
bus.write_byte_data(0x53, 0x2C, 0x0A)
# Select power control register, 0x2D(45)
#       0x08(08)    Auto Sleep disable
bus.write_byte_data(0x53, 0x2D, 0x08)
# Select data format register, 0x31(49)
#       0x08(08)    Self test disabled, 4-wire interface
#                   Full resolution, Range = +/-2g
bus.write_byte_data(0x53, 0x31, 0x08)

time.sleep(0.5)

x, y, t = readData()

vel = calculateVelocity(1)

print("%0.5f" % vel, "m/s")

