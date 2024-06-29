import time
from plutocontrol import pluto
drone = pluto()

# Assuming you've instantiated your drone object as 'drone'
drone.connect()

drone.get_battery()

def continuously_get_sensor_values(interval_seconds=1):
    while True:
        mag_x = drone.get_mag_x()
        mag_y = drone.get_mag_y()
        mag_z = drone.get_mag_z()
        gyro_x = drone.get_gyro_x()
        gyro_y = drone.get_gyro_y()
        gyro_z = drone.get_gyro_z()
        acc_x = drone.get_acc_x()
        acc_y = drone.get_acc_y()
        acc_z = drone.get_acc_z()

        print(f"Magnetometer (X,Y,Z): ({mag_x}, {mag_y}, {mag_z})")
        print(f"Gyroscope (X,Y,Z): ({gyro_x}, {gyro_y}, {gyro_z})")
        print(f"Accelerometer (X,Y,Z): ({acc_x}, {acc_y}, {acc_z})")

        time.sleep(interval_seconds)

# Call the function to start retrieving sensor values continuously
continuously_get_sensor_values()