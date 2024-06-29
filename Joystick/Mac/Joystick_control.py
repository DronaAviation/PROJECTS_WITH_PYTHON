import pygame
import threading

class XboxController(object):
    MAX_TRIG_VAL = 255
    MAX_JOY_VAL = 32768

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        pygame.init()
        pygame.joystick.init()

        # Initialize joystick
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def read(self):
        pygame.event.pump()  # Pump events to update joystick status
        # Update joystick axes
        self.LeftJoystickX = self.joystick.get_axis(0)
        self.LeftJoystickY = -self.joystick.get_axis(1)
        self.RightJoystickX = self.joystick.get_axis(3)
        self.RightJoystickY = -self.joystick.get_axis(4)
        # Update triggers
        self.LeftTrigger = max(0, self.joystick.get_axis(2))
        self.RightTrigger = max(0, self.joystick.get_axis(5))
        # Update buttons
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

if __name__ == '__main__':
    joy = XboxController()
    while True:
        print(joy.read())
