import Joystick_control  # Importing the Joystick_controls module for Xbox controller input
from plutocontrol import pluto  # Importing the Pluto module for interfacing with the Pluto drone


# Initialize Xbox controller and Pluto drone objects
joy = Joystick_control.XboxController()
my_pluto = pluto()

# Function to map input range to output range
def mapping(x, inMin, inMax, outMin, outMax): 
    x = (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin
    if (x < outMin):
      return int(outMin)
    elif (x > outMax):
      return int(outMax)
    else:
      return int(x)

# Main loop for continuously reading and processing controller input
while True:
  
    # Read input from the Xbox controller
    [x, y, a, b, A, B, X, Y, rb, lb, rt, lt, ld, rd, ud, dd] = joy.read()

     # Map controller input to drone controls
    my_pluto.rcThrottle = mapping(y, 1, -1, 1000, 2000)    
    my_pluto.rcYaw = mapping(x, -1, 1, 1000, 2000)
    my_pluto.rcPitch = mapping(b, 1, -1, 1000, 2000)
    my_pluto.rcRoll = mapping(a, -1, 1, 1000, 2000)
    
    # Check button states for drone actions
    print(my_pluto.rcRoll)
    if A: 
      my_pluto.arm()  # Arm the drone
      # time.sleep(0.5)
      print("arming", A)
    elif B:
      my_pluto.disarm()  # Disarm the drone
      print("disarming", B)
    elif Y:
      my_pluto.take_off()  # Take off the drone
      # time.sleep(0.5)
      print("taken off", X)
    elif X:
      my_pluto.land() # Land the drone
      my_pluto.disarm()
      print("landing", Y)
      

    
