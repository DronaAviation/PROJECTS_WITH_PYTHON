import evdev
import threading
import errno

class XboxController(object):
    MAX_TRIG_VAL = 255
    MAX_JOY_VAL = 32768

    def __init__(self, device_path):
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

        # Open the joystick device
        self.device = evdev.InputDevice(device_path)

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def read(self):
        try:
            for event in self.device.read():
                if event.type == evdev.ecodes.EV_ABS:
                    if event.code == evdev.ecodes.ABS_X:
                        self.LeftJoystickX = event.value
                    elif event.code == evdev.ecodes.ABS_Y:
                        self.LeftJoystickY = event.value
                    elif event.code == evdev.ecodes.ABS_RX:
                        self.RightJoystickX = event.value
                    elif event.code == evdev.ecodes.ABS_RY:
                        self.RightJoystickY = event.value
                    elif event.code == evdev.ecodes.ABS_Z:
                        self.LeftTrigger = event.value
                    elif event.code == evdev.ecodes.ABS_RZ:
                        self.RightTrigger = event.value
                elif event.type == evdev.ecodes.EV_KEY:
                    if event.code == evdev.ecodes.BTN_A:
                        self.A = event.value
                    elif event.code == evdev.ecodes.BTN_B:
                        self.B = event.value
                    elif event.code == evdev.ecodes.BTN_X:
                        self.X = event.value
                    elif event.code == evdev.ecodes.BTN_Y:
                        self.Y = event.value
                    elif event.code == evdev.ecodes.BTN_TL:
                        self.LeftBumper = event.value
                    elif event.code == evdev.ecodes.BTN_TR:
                        self.RightBumper = event.value
                    elif event.code == evdev.ecodes.BTN_THUMBL:
                        self.LeftThumb = event.value
                    elif event.code == evdev.ecodes.BTN_THUMBR:
                        self.RightThumb = event.value
                    elif event.code == evdev.ecodes.BTN_START:
                        self.Start = event.value
                    elif event.code == evdev.ecodes.BTN_SELECT:
                        self.Back = event.value
                    elif event.code == evdev.ecodes.BTN_TRIGGER_HAPPY1:
                        self.LeftDPad = event.value
                    elif event.code == evdev.ecodes.BTN_TRIGGER_HAPPY2:
                        self.RightDPad = event.value
                    elif event.code == evdev.ecodes.BTN_TRIGGER_HAPPY3:
                        self.UpDPad = event.value
                    elif event.code == evdev.ecodes.BTN_TRIGGER_HAPPY4:
                        self.DownDPad = event.value
        except OSError as e:
            if e.errno != errno.EAGAIN:
                raise

        return [self.LeftJoystickX, self.LeftJoystickY, self.RightJoystickX, self.RightJoystickY,
                self.LeftTrigger, self.RightTrigger, self.LeftBumper, self.RightBumper,
                self.A, self.B, self.X, self.Y, self.LeftThumb, self.RightThumb,
                self.Back, self.Start, self.LeftDPad, self.RightDPad, self.UpDPad, self.DownDPad]

    def _monitor_controller(self):
        # You can handle continuous monitoring here if required
        pass

if __name__ == '__main__':
    device_path = "/dev/input/event23"  # Replace X with the appropriate event number
    joy = XboxController(device_path)
    while True:
        print(joy.read())
