# Module Purpose: Decides whether the driver is distracted or not, based on results from image analysis modules.

# Amount of time that the driver’s eyes have been distracted.
timeEyesDistracted = 0

# A static value which is the maximum amount of time that the driver’s eyes can be detected as distracted before the driver is classified as distracted.
eyesTimeThreshold = 0

# Amount of time that a distracting object has been detected.
timeObjectDetected = 0

# A static value which is the maximum amount of time that an object can be detected before the driver is classified as distracted.
objectTimeThreshold = 0

# Amount of time between image captures (equivalent to 1/framerate)
cameraInterval = 0

# Purpose: updates the consecutive frame counts data fields.  Increments relevant timeDistracted fields if distracted, sets other timeDistracted fields to 0 if not distracted.
# Pre-conditions: timeEyesDistracted >=0, timeObjectDetected >=0.
# Post-conditions:  timeEyesDistracted >=0, timeObjectDetected >=0.
# Parameters: boolean eyesDistracted, boolean objectDetected.
# Return type: int return code.
def updateTimes():
    pass

# Purpose: Classifies if the driver is distracted or not, based on the timeDistracted fields.
# Pre-conditions: None
# Post-Conditions: None
# Parameters: all of the module data fields (timeDistracted fields and respective threshold fields).
# Return type: boolean driverIsDistracted.
def isDistracted():
    pass
