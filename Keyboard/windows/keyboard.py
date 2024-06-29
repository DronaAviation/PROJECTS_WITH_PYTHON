import os
import sys
import keyboard_control 
import keyboard as kb

#####################################################
# Key Controls

# c : Connect
# spacebar : arm or disarm

# w : increase height
# s : decrease height
# a : yaw left
# d : yaw right

# q : take off
# e : land

# n: To enter developer mode

# Up arrow : go forward
# Down arrow : go backward
# Left arrow : go left
# Right arrow : go right

# e: to quit
#####################################################

if os.name == 'nt':  # Windows
    def getKey():
        event = kb.read_event()
        key = event.name
        if event.event_type == kb.KEY_DOWN:
            if key == 'up':
                key = '[A'
            elif key == 'down':
                key = '[B'
            elif key == 'left':
                key = '[D'
            elif key == 'right':
                key = '[C'
            elif key == 'space':
                key = ' '

            # print(key)
            return key
        

keyboard_cmds={  #dictionary containing the key pressed and value associated with it
                      '[A': 10,
                      '[D': 30,
                      '[C': 40,
                      'w':50,
                      's':60,
                      ' ': 70,
                      'r':80,
                      't':90,
                      'p':100,
                      '[B':110,
                      'n':120,
                      'q':130,
                      'e':140,
                      'a':150,
                      'd':160,
                      '+' : 15,
                      '1' : 25,
                      '2' : 30,
                      '3' : 35,
                      '4' : 45}

while True:
    key = getKey()
    if key == 'e':
        print("stopping")
        break
    if key in keyboard_cmds.keys():
        msg = keyboard_cmds[key]
        keyboard_control.identify_key(msg)  
    else: 
        msg = 80    
        keyboard_control.identify_key(msg)
  
