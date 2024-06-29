from plutocontrol import pluto
import time

drone = pluto()
#drone.cam()
drone.connect()
drone.arm()
time.sleep(2)
drone.disarm()
drone.disconnect()