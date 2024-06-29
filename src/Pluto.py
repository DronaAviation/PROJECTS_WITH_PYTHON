import socket
from threading import Thread
import time

TRIM_MAX = 1000
TRIM_MIN = -1000
MSP_HEADER_IN = "244d3c"

MSP_FC_VERSION = 3
MSP_RAW_IMU = 102
MSP_RC = 105
MSP_ATTITUDE = 108
MSP_ALTITUDE = 109
MSP_ANALOG = 110
MSP_SET_RAW_RC = 200
MSP_ACC_CALIBRATION = 205
MSP_MAG_CALIBRATION = 206
MSP_SET_MOTOR = 214
MSP_SET_ACC_TRIM = 239
MSP_ACC_TRIM = 240
MSP_EEPROM_WRITE = 250
MSP_SET_POS = 216
MSP_SET_COMMAND = 217
MSP_SET_1WIRE = 243
MSP_VARIO = 122  # Example MSP command for vario (check your drone's documentation for the correct value)
RETRY_COUNT = 3

class pluto:
    def __init__(self):
        self.rcRoll = 1500
        self.rcPitch = 1500
        self.rcThrottle = 1500
        self.rcYaw = 1500
        self.rcAUX1 = 1500
        self.rcAUX2 = 1000
        self.rcAUX3 = 1500
        self.rcAUX4 = 1000
        self.command_type = 0  # Initialize command_type here
        self.droneRC = [1500, 1500, 1500, 1500, 1500, 1000, 1500, 1000]
        self.NONE_COMMAND = 0
        self.TAKE_OFF = 1
        self.LAND = 2
        self.connected = False
        self.cam_connected = False
        self.TCP_IP = '192.168.4.1'
        self.TCP_PORT = 23
        self.thread = Thread(target=self.write_function)
        self.thread.start()

    def start_write_function(self):
        self.thread = Thread(target=self.write_function)
        self.thread.start()
        
    def connect(self):
        if not self.connected:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.client.connect((self.TCP_IP, self.TCP_PORT))
                self.connected = True
                print("Connected to server")
                self.start_write_function()
            except Exception as e:
                print("Error connecting to server:", e)

    def disconnect(self):
        if self.connected:
            self.client.close()
            self.connected = False
            print("Disconnected from server")

    def cam(self):
        self.TCP_IP = '192.168.0.1'
        self.TCP_PORT = 9060
        self.camera_mode = True
        
    def arm(self):
        print("Arming")
        self.rcRoll = 1500
        self.rcYaw = 1500
        self.rcPitch = 1500
        self.rcThrottle = 1000
        self.rcAUX4 = 1500

    def box_arm(self):
        print("boxarm")
        self.rcRoll = 1500
        self.rcYaw = 1500
        self.rcPitch = 1500
        self.rcThrottle = 1800
        self.rcAUX4 = 1500

    def disarm(self):
        print("Disarm")
        self.rcThrottle = 1300
        self.rcAUX4 = 1200

    def devOn(self):
        print("Developer mode ON")
        self.rcAUX2 = 1500
        
    def devOff(self):
        print("Developer mode OFF")
        self.rcAUX2 = 1000
        
    def forward(self):
        print("Forward")
        self.rcPitch = 1600

    def backward(self):
        print("Backward")
        self.rcPitch = 1300

    def left(self):
        print("Left Roll")
        self.rcRoll = 1200

    def right(self):
        print("Right Roll")
        self.rcRoll = 1600

    def left_yaw(self):
        print("Left Yaw")
        self.rcYaw = 1300

    def right_yaw(self):
        print("Right Yaw")
        self.rcYaw = 1600

    def reset(self):
        self.rcRoll = 1500
        self.rcThrottle = 1500
        self.rcPitch = 1500
        self.rcYaw = 1500
        self.commandType = 0

    def increase_height(self):
        print("Increasing height")
        self.rcThrottle = 1800

    def decrease_height(self):
        print("Decreasing height")
        self.rcThrottle = 1300

    def take_off(self):
        self.disarm()
        self.box_arm()
        print("take off")
        self.commandType = 1

    def land(self):
        self.commandType = 2

    def rc_values(self):
        return [self.rcRoll, self.rcPitch, self.rcThrottle, self.rcYaw,
                self.rcAUX1, self.rcAUX2, self.rcAUX3, self.rcAUX4]

    def motor_speed(self, motor_index, speed):
        if 0 <= motor_index < 4:
            motor_speeds = [1000, 1000, 1000, 1000]
            motor_speeds[motor_index] = speed
            self.send_request_msp_set_motor(motor_speeds)
        else:
            print("Invalid motor index. Must be between 0 and 3.")

    def trim_left_roll(self):
        print("Trimming Left Roll")
        self.rcRoll = max(TRIM_MIN, self.rcRoll + 100)
    
            
    def send_request_msp(self, data):
       if self.connected:
           self.client.send(bytes.fromhex(data))
       else:
           if not hasattr(self, 'connection_error_logged'):
               print("Error: Not connected to server")
               self.connection_error_logged = True

    def create_packet_msp(self, msp, payload):
        bf = ""
        bf += MSP_HEADER_IN

        checksum = 0
        if (msp == MSP_SET_COMMAND):
            pl_size = 1
        else:
            pl_size = len(payload) * 2

        bf += '{:02x}'.format(pl_size & 0xFF)
        checksum ^= pl_size

        bf += '{:02x}'.format(msp & 0xFF)
        checksum ^= msp

        for k in payload:
            if (msp == MSP_SET_COMMAND):
                bf += '{:02x}'.format(k & 0xFF)
                checksum ^= k & 0xFF
            else:
                bf += '{:02x}'.format(k & 0xFF)
                checksum ^= k & 0xFF
                bf += '{:02x}'.format((k >> 8) & 0xFF)
                checksum ^= (k >> 8) & 0xFF

        bf += '{:02x}'.format(checksum)

        return bf

    def send_request_msp_set_raw_rc(self, channels):
        self.send_request_msp(self.create_packet_msp(MSP_SET_RAW_RC, channels))

    def send_request_msp_set_command(self, command_type):
        self.send_request_msp(self.create_packet_msp(MSP_SET_COMMAND, [command_type]))

    def send_request_msp_get_debug(self, requests):
        for i in range(len(requests)):
            self.send_request_msp(self.create_packet_msp(requests[i], []))

    def send_request_msp_set_acc_trim(self, trim_roll, trim_pitch):
        self.send_request_msp(self.create_packet_msp(MSP_ACC_TRIM, [trim_roll, trim_pitch]))

    def send_request_msp_acc_trim(self):
        if self.connected:
            self.send_request_msp(self.create_packet_msp(MSP_ACC_TRIM, []))
        else:
            print("Error: Not connected to server")

    def send_request_msp_eeprom_write(self):
        self.send_request_msp(self.create_packet_msp(MSP_EEPROM_WRITE, []))

    def send_request_msp_set_motor(self, motor_speeds):
        payload = []
        for speed in motor_speeds:
            payload.append(speed & 0xFF)
            payload.append((speed >> 8) & 0xFF)
        self.send_request_msp(self.create_packet_msp(MSP_SET_MOTOR, payload))

    def write_function(self):
        requests = [MSP_RC, MSP_ATTITUDE, MSP_RAW_IMU, MSP_ALTITUDE, MSP_ANALOG]
        self.send_request_msp_acc_trim()

        while self.connected:
            self.droneRC[:] = self.rc_values()

            self.send_request_msp_set_raw_rc(self.droneRC)
            self.send_request_msp_get_debug(requests)

            if self.command_type != self.NONE_COMMAND:
                self.send_request_msp_set_command(self.command_type)
                self.command_type = self.NONE_COMMAND

            time.sleep(0.022)

    def get_height(self):
        data = []
        self.create_packet_msp(MSP_ALTITUDE, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 109:
                i += 1
            if i + 3 < len(data):
                height = self.read16(data[i + 1:i + 3])
                print(f"height: {height} cm")
                return height

    def get_vario(self):
        data = []
        self.create_packet_msp(MSP_ALTITUDE, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 109:
                i += 1
            if i + 7 < len(data):
                return self.read16(data[i + 5:i + 7])

    def get_roll(self):
        data = []
        self.create_packet_msp(MSP_ATTITUDE, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 108:
                i += 1
            if i + 3 < len(data):
                roll = self.read16(data[i + 1:i + 3]) / 10
                print(f"roll: {roll} degrees")
                return roll

    def get_pitch(self):
        data = []
        self.create_packet_msp(MSP_ATTITUDE, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 108:
                i += 1
            if i + 5 < len(data):
                pitch = self.read16(data[i + 3:i + 5]) / 10
                print(f"pitch: {pitch} degrees")
                return pitch

    def get_yaw(self):
        data = []
        self.create_packet_msp(MSP_ATTITUDE, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 108:
                i += 1
            if i + 7 < len(data):
                return self.read16(data[i + 5:i + 7])

    def get_acc_x(self):
        data = []
        self.create_packet_msp(MSP_RAW_IMU, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 102:
                i += 1
            if i + 3 < len(data):
                return self.read16(data[i + 1:i + 3])

    def get_acc_y(self):
        data = []
        self.create_packet_msp(MSP_RAW_IMU, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 102:
                i += 1
            if i + 5 < len(data):
                return self.read16(data[i + 3:i + 5])

    def get_acc_z(self):
        data = []
        self.create_packet_msp(MSP_RAW_IMU, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 102:
                i += 1
            if i + 7 < len(data):
                return self.read16(data[i + 5:i + 7])

    def get_gyro_x(self):
        data = []
        self.create_packet_msp(MSP_RAW_IMU, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 102:
                i += 1
            if i + 9 < len(data):
                return self.read16(data[i + 7:i + 9])

    def get_gyro_y(self):
        data = []
        self.create_packet_msp(MSP_RAW_IMU, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 102:
                i += 1
            if i + 11 < len(data):
                return self.read16(data[i + 9:i + 11])

    def get_gyro_z(self):
        data = []
        self.create_packet_msp(MSP_RAW_IMU, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 102:
                i += 1
            if i + 13 < len(data):
                return self.read16(data[i + 11:i + 13])

    def get_mag_x(self):
        data = []
        self.create_packet_msp(MSP_RAW_IMU, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 102:
                i += 1
            if i + 15 < len(data):
                return self.read16(data[i + 13:i + 15])

    def get_mag_y(self):
        data = []
        self.create_packet_msp(MSP_RAW_IMU, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 102:
                i += 1
            if i + 17 < len(data):
                return self.read16(data[i + 15:i + 17])

    def get_mag_z(self):
        data = []
        self.create_packet_msp(MSP_RAW_IMU, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 102:
                i += 1
            if i + 19 < len(data):
                return self.read16(data[i + 17:i + 19])

    def calibrate_acceleration(self):
        self.create_packet_msp(MSP_ACC_CALIBRATION, [])
        time.sleep(5)  # Adjust sleep duration based on calibration time
        acc_x = self.get_acc_x()
        acc_y = self.get_acc_y()
        acc_z = self.get_acc_z()
        print("Calibrated Accelerometer Values:")
        print(f"X-Axis: {acc_x}, Y-Axis: {acc_y}, Z-Axis: {acc_z}")

    def calibrate_magnetometer(self):
        self.create_packet_msp(MSP_MAG_CALIBRATION, [])
        time.sleep(5)  # Adjust sleep duration based on calibration time
        mag_x = self.get_mag_x()
        mag_y = self.get_mag_y()
        mag_z = self.get_mag_z()
        print("Calibrated Magnetometer Values:")
        print(f"X-Axis: {mag_x}, Y-Axis: {mag_y}, Z-Axis: {mag_z}")

    def get_battery(self):
        data = []
        self.create_packet_msp(MSP_ANALOG, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 110:
                i += 1
            if i + 1 < len(data):
                battery_value = data[i + 1] / 10
                print(f"Battery: {battery_value} volts")
                return battery_value

    def get_battery_percentage(self):
        data = []
        self.create_packet_msp(MSP_ANALOG, data) 
        for i in range(RETRY_COUNT):
            data = self.receive_packet()
            i = 0
            while i < len(data) and data[i] != 110:
                i += 1
            if i + 1 < len(data):
                battery_voltage = data[i + 1] / 10
                battery_percentage = (battery_voltage / 4.2) * 100
                print(f"Battery: {battery_percentage:.2f}%")
                return battery_percentage
            
    def send_packet(self, buff):
        self.client.send(buff)

    def receive_packet(self):
        return self.client.recv(4096)

    def read16(self, arr):
        if (arr[1] & 0x80) == 0:
            return (arr[1] << 8) + (arr[0] & 0xff)
        else:
            return (-65535 + (arr[1] << 8) + (arr[0] & 0xff))
