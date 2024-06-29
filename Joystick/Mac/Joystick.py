import time
import pygame
import threading

from Pluto import pluto

my_pluto = pluto()


class XboxController(object):
    MAX_TRIG_VAL = 255
    MAX_JOY_VAL = 32768

    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def read(self):
        pygame.event.pump()
        self.LeftJoystickX = self.joystick.get_axis(0)
        self.LeftJoystickY = -self.joystick.get_axis(1)
        self.RightJoystickX = self.joystick.get_axis(3)
        self.RightJoystickY = -self.joystick.get_axis(4)
        self.LeftTrigger = max(0, self.joystick.get_axis(2))
        self.RightTrigger = max(0, self.joystick.get_axis(5))
        self.A = self.joystick.get_button(0)
        self.B = self.joystick.get_button(1)
        self.X = self.joystick.get_button(2)
        self.Y = self.joystick.get_button(3)
        self.LeftBumper = self.joystick.get_button(4)
        self.RightBumper = self.joystick.get_button(5)
        self.Back = self.joystick.get_button(6)
        self.Start = self.joystick.get_button(7)
        self.LeftThumb = self.joystick.get_button(8)
        self.RightThumb = self.joystick.get_button(9)
        self.LeftDPad = self.joystick.get_button(10)
        self.RightDPad = self.joystick.get_button(11)
        self.UpDPad = self.joystick.get_button(12)
        self.DownDPad = self.joystick.get_button(13)
        return [self.LeftJoystickX, self.LeftJoystickY, self.RightJoystickX, self.RightJoystickY,
                self.A, self.B, self.X, self.Y, self.RightBumper, self.LeftBumper]

    def _monitor_controller(self):
        while True:
            pass

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
# Main loop for continuously reading and processing controller input
joy = XboxController()
while True:
    # Read input from the Xbox controller
    [x, y, a, b, A, B, X, Y, rb, lb] = joy.read()

    # Map controller input to drone controls
    my_pluto.rcThrottle = mapping(y, 1, -1, 1000, 2000)
    my_pluto.rcYaw = mapping(x, -1, 1, 1000, 2000)
    my_pluto.rcPitch = mapping(b, 1, -1, 1000, 2000)
    my_pluto.rcRoll = mapping(a, -1, 1, 1000, 2000)

    # Check button states for drone actions
    print(my_pluto.rcRoll)
    if A:
        my_pluto.arm()  # Arm the drone
        print("arming", A)
    elif B:
        my_pluto.disarm()  # Disarm the drone
        print("disarming", B)
    elif Y:
        my_pluto.take_off()  # Take off the drone
        print("taken off", X)
    elif X:
        my_pluto.land()  # Land the drone
        my_pluto.disarm()
        print("landing", Y)

    time.sleep(0.01)  # Adjust sleep time as needed

