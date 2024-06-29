import sys
import platform

# Check the operating system
if platform.system() == 'Windows':
    from plutocontrol import pluto
    my_pluto = pluto()
elif platform.system() == 'Linux':
    from plutocontrol import pluto
    import sys, select, termios, tty

    settings = termios.tcgetattr(sys.stdin)

    def getKey():
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
            if (key == '\x1b'):
                key = sys.stdin.read(2)
            sys.stdin.flush()
        else:
            key = ''

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    my_pluto = pluto()

# Function to identify the key pressed and perform corresponding drone actions
def identify_key(key):
    if key == 70:
        # Arm or disarm the drone based on the current state of rcAUX4
        if(my_pluto.rcAUX4 == 1500):
            my_pluto.disarm()   # arm the drone
        else:
            my_pluto.arm()  # disarm the drone
    elif key == 10:
        my_pluto.forward() # Move the drone forward
    elif key == 30:
        my_pluto.left()  # Move the drone left
    elif key == 40:
        my_pluto.right() # Move the drone right
    elif key == 80:
        my_pluto.reset() # Reset drone movements
    elif key == 50:
        my_pluto.increase_height()  # Increase drone height
    elif key == 60:
        my_pluto.decrease_height() # Decrease drone height
    elif key == 110:
        my_pluto.backward() # Move the drone backward
    elif key == 130:
        my_pluto.take_off() # Take off the drone
    elif key == 140:
        my_pluto.land() # Land the drone
    elif key == 150:
        my_pluto.left_yaw() # Rotate the drone to the left
    elif key == 160:
        my_pluto.right_yaw()  # Rotate the drone to the right
    elif key == 120:
        print("Developer Mode ON")
        my_pluto.rcAUX2 = 1500  # Set developer mode on
