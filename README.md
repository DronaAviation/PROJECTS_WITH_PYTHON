# PLUTO_PYTHON_WRAPPER

Pluto can be operated using Python for various tasks. Python is a versatile programming language known for its simplicity and readability.

## Basic Flight Controls/ Commands:
![W](https://github.com/csaail/PLUTO_PYTHON_WRAPPER/assets/87662482/86b0fbee-adbe-42af-9f66-f3d1518fe15d)

Pitch => Forward/Back.<br/> Roll => Left/right.<br/>  Yaw => Left/right rotation around the centre of the frame.<br/>  Throttle => Changed altitude/speed.

# plutocontrol

plutocontrol is a Python library for controlling Pluto drones. This library provides various methods to interact with the drone, including connecting, controlling movements, and accessing sensor data.

## Installation

```bash
pip install plutocontrol
```

## Usage

After installing the package, you can import and use the `Pluto` class in your Python scripts.

### Example Usage

#### Example 1

```python
from plutocontrol import Pluto

# Create an instance of the Pluto class
pluto = Pluto()

# Connect to the drone
pluto.connect()

# Arm the drone
pluto.arm()

# Disarm the drone
pluto.disarm()

# Disconnect from the drone
pluto.disconnect()
```


## Keyboard Controls:

To set up keyboard controls for your Pluto drone, follow these general steps:

1. Locate Keyboard Control Files:
   - Navigate to the appropriate directory based on your operating system:
     - For Windows users: Keyboard/windows
     - For Linux/Mac users: Keyboard/linux,mac

2. Run Keyboard Control Script:
   - Locate the keyboard.py file in the respective directory and run it.

### Specific Instructions:

#### For Windows Users:
- Navigate to the Keyboard/windows directory.
- Run the ```keyboard.py``` script.

#### For Linux/Mac Users:
- Navigate to the Keyboard/linux_mac directory.
- Run the ```keyboard.py``` script.

![W](https://github.com/csaail/PLUTO_PYTHON_WRAPPER/assets/87662482/88f4e13c-2aed-4037-a63b-0d4a57ca5677)

## Joystick Controls Setup:

To set up joystick controls for your Pluto drone, follow these general steps:

1. Ensure Necessary Libraries:
   - Make sure you have the required libraries installed for your operating system.

2. Locate Joystick Control Files:
   - Navigate to the appropriate directory based on your operating system:
     - For Windows users: Joystick/windows
     - For Ubuntu (Linux) users: Joystick/linux
     - For macOS users: Joystick/mac

3. Run Joystick Control Script:
   - Locate the ```joystick.py``` file in the respective directory and run it.

### Specific Instructions:

#### For Windows Users:
- Ensure that you have the necessary libraries installed.
- Navigate to the Joystick/windows directory.
- Run the joystick.py script.

#### For Ubuntu (Linux) Users:
- Make sure you have the Evdev library installed on your system.
- Navigate to the Joystick/linux directory.
- Run the joystick.py script.

#### For macOS Users:
- Ensure that you have the Pygame library installed.
- Navigate to the Joystick/mac directory.
- Run the joystick.py script.

Currently the default settings are: (Note: you can change them according to your need)

![joystick (1)](https://github.com/csaail/PLUTO_PYTHON_WRAPPER/assets/87662482/1c021e29-8390-4133-96a4-02808f522b44)
![joystick tp (1)](https://github.com/csaail/PLUTO_PYTHON_WRAPPER/assets/87662482/336ae10a-6ea9-4ad1-9b3b-7bb3cc0e3999)

## Voice Controlled Drone

We've developed a script that enables you to control your Pluto drone using your voice!

1. **Download Pre-trained Voice Model:**
   - Visit [Vosk Models](https://alphacephei.com/vosk/models) to download a pre-trained voice model.
   - Recommended models: `vosk-model-small-en-us-0.15` or `vosk-model-en-in-0.5`.

2. **Configure Voice Command Script:**
   - Copy the path where you've stored your downloaded model.
   - Paste the path into the `voice_cmd.py` file located in the "voice" folder.

3. **Run Voice Command Script:**
   - Navigate to the "voice" folder.
   - Run the file:
     `
     voice_cmd.py
     `
     
Currently, the drone responds to the following voice commands:
- "hello" to arm the drone.
- "take off" to initiate takeoff.
- "land" to initiate landing.

Feel free to customize these commands according to your preferences.

![Arm](https://github.com/csaail/PLUTO_PYTHON_WRAPPER/assets/87662482/3585846f-4a2e-46fa-8bfb-704ad2a6c131)

