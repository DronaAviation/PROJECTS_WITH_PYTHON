from plutocontrol import pluto
import time

# Initialize the drone
drone = pluto()

# Connect to the drone
print("Connecting to the drone")
drone.connect()
time.sleep(2)  # Ensure connection is established

# Arm the drone
drone.arm()
time.sleep(3)  

# Take off
drone.take_off()
time.sleep(1) 

for _ in range(50):  
    drone.increase_height()
    time.sleep(0.05) 
    
# Hover for a bit before landing
print("Hovering")
time.sleep(5)

# Land the drone
print("Landing the drone")
drone.land()
time.sleep(5)

drone.disconnect()
