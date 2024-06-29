from inputs import get_gamepad   # Importing the function to get input events from the gamepad
import math
import threading                 # Importing threading module for multi-threading support

class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)    # Maximum value for triggers
    MAX_JOY_VAL = math.pow(2, 15)    # Maximum value for joysticks

    def __init__(self):
        # Initialize all button and joystick states to zero
        
        # Left stick
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        
        # Right stick
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        
        # Triggers
        self.LeftTrigger = 0
        self.RightTrigger = 0
        
        # Bumpers
        self.LeftBumper = 0
        self.RightBumper = 0
        
        # Face buttons
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        
        # Stick buttons
        self.LeftThumb = 0
        self.RightThumb = 0
        
        # Buttons
        self.Back = 0
        self.Start = 0
        
        # D-pad
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        # Thread to continuously monitor the controller
        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self): 
        # Return the current state of buttons and joysticks
        
        x = self.LeftJoystickX
        y = self.LeftJoystickY
        
        a = self.RightJoystickX
        b = self.RightJoystickY
        
        A = self.A
        B = self.B
        X = self.X
        Y = self.Y # b=1, x=2
        
        rb = self.RightBumper
        lb = self.LeftBumper
        
        rt = self.RightTrigger
        lt = self.LeftTrigger
        
        ld = self.LeftDPad
        rd = self.RightDPad
        ud = self.UpDPad
        dd = self.DownDPad
        
        # Return the values as a list
        return [x, y, a, b, A, B, X, Y, rb, lb, rt, lt, ld, rd, ud, dd]


    def _monitor_controller(self):
        # Continuously monitor the controller for input events
        while True: 
            events = get_gamepad() # Get input events from the gamepad
            for event in events:
                 # Update controller attributes based on input events
                 
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = -(event.state / XboxController.MAX_JOY_VAL ) # normalize joystick value between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize joystick value between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = -(event.state / XboxController.MAX_JOY_VAL) # normalize joystick value between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize joystick value between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize joystick value between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize joystick value between 0 and 1
                
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                    
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                    # print(event.state)
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state

# Main block to create an instance of XboxController and continuously print its state
if __name__ == '__main__':
     joy = XboxController()
     while True:
         print(joy.read())
