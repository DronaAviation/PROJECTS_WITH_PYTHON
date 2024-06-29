from plutocontrol import pluto

my_pluto = pluto()

def identify_key(key):
    if key == 70:
        if(my_pluto.rcAUX4 == 1500):
            my_pluto.disarm()
        else:
            my_pluto.arm()
    elif key == 10:
        my_pluto.forward()
    elif key == 30:
        my_pluto.left()
    elif key == 40:
        my_pluto.right()
    elif key == 80:
        my_pluto.reset()
    elif key == 50:
        my_pluto.increase_height()
    elif key == 60:
        my_pluto.decrease_height()
    elif key == 110:
        my_pluto.backward()
    elif key == 130:
        my_pluto.take_off()
    elif key == 140:
        my_pluto.land()
    elif key == 150:
        my_pluto.left_yaw()
    elif key == 160:
        my_pluto.right_yaw()
    elif key == 120:
        print("Developer Mode ON")
        my_pluto.rcAUX2 = 1500


