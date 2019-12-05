import smbus2 as smbus
import numpy
import time
from datetime import datetime

# Function to read data from accelerometer
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

    # Calculate Total Acceleration
    accel = numpy.array([xms, yms])
    t = numpy.linalg.norm(accel)

    # Output data to screen - debugging
#     print ("Acceleration in X-Axis : ", xms, "m/s^2")
#     print ("Acceleration in Y-Axis : ", yms, "m/s^2")
#     print ("Acceleration in Z-Axis : ", zms, "m/s^2")
#     print ("Total Acceleration : ", t, "m/s^2")
    
    return t
# end of readData()

# Function to write data to text file
def writeData(tData, vData):
    rn = datetime.now()
    timestamp = rn.strftime("%H:%M:%S")
    fs.write(timestamp + " -- " + "Tot: " + "%0.6f" % tData + ", Vel: " + "%0.6f" % vData + "\n")
    return
# end of writeData()

# Function to calculate velocity
def calculateVelocity(oldV, t, freq):
    delT = freq
    a = t
    v = oldV + (a * delT)
    return v
# end of calculateVelocity()

# Function to find standard acceleration
def fsa():
    one = readData()
    two = readData()
    three = readData()
    four = readData()
    five = readData()
    
    stan = (one + two + three + four + five) / 5
    return stan
# end of fsa()

# Function to normalize acceleration (try to get rid of noise)
def normalizeAcc(t, stan):
    if (t - stan < 1.5 and t - stan > -1.5):
        return 0
    else:
        return (t - stan)
# end of normalizeAcc()

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



# Getting date and time to create name of test file
now = datetime.now()
dt = now.strftime("%m-%d-%Y_%H:%M")

# Opening filestream to write to test file
fs = open("/home/pi/3DS/tests/" + dt + ".txt", 'a+')
print("\tFile opened with name " + dt + ".txt in location /home/pi/3DS/tests.")

count = 0
velocity = 0
readLimit = 1200
frequency = 0.5
minutes = ((readLimit * frequency) / 60)
print("\tCollecting data every " + str(frequency) + " second(s) for " + str(minutes) + " minute(s).")

stanAcc = fsa() # Calculate a standard acceleration to mark zero point

while count < readLimit:
    t = readData()
    acc = normalizeAcc(t, stanAcc)
    velocity = calculateVelocity(velocity, acc, frequency)
#    print(acc, ", ", velocity)
    writeData(acc, velocity)
    time.sleep(frequency)
    count += 1

# Must close filestream before exiting program! Otherwise data doesn't save!
fs.close()
print("\tData collection complete and filestream closed.")

