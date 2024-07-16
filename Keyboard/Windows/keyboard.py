import keyboard as kb
from plutocontrol import pluto

my_pluto = pluto()

actions = {
    70: lambda: my_pluto.disarm() if my_pluto.rcAUX4 == 1500 else my_pluto.arm(),
    10: my_pluto.forward,
    30: my_pluto.left,
    40: my_pluto.right,
    80: my_pluto.reset,
    50: my_pluto.increase_height,
    60: my_pluto.decrease_height,
    110: my_pluto.backward,
    130: my_pluto.take_off,
    140: my_pluto.land,
    150: my_pluto.left_yaw,
    160: my_pluto.right_yaw,
    120: lambda: (print("Developer Mode ON"), setattr(my_pluto, 'rcAUX2', 1500)),
    200: my_pluto.connect,
    210: my_pluto.disconnect,
}

keyboard_cmds = {
    '[A': 10, '[D': 30, '[C': 40, 'w': 50, 's': 60, ' ': 70, 'r': 80, 't': 90,
    'p': 100, '[B': 110, 'n': 120, 'q': 130, 'e': 140, 'a': 150, 'd': 160,
    '+': 15, '1': 25, '2': 30, '3': 35, '4': 45, 'c': 200, 'x': 210
}

key_map = {'up': '[A', 'down': '[B', 'left': '[D', 'right': '[C', 'space': ' '}

def getKey():
    event = kb.read_event()
    return key_map.get(event.name, event.name) if event.event_type == kb.KEY_DOWN else None

while (key := getKey()) != 'e':
    actions.get(keyboard_cmds.get(key, 80), my_pluto.reset)()
print("stopping")
