from pynput import mouse
from plutocontrol import pluto

my_pluto = pluto()

def identify_mouse_action(action, x, y, button, pressed, dx, dy):
    if action == 'click':
        if button == mouse.Button.left and pressed:
            my_pluto.take_off()
        elif button == mouse.Button.right and pressed:
            my_pluto.land()
    elif action == 'move':
        if x < 100:
            my_pluto.left()
        elif x > 500:
            my_pluto.right()
        elif y < 100:
            my_pluto.forward()
        elif y > 500:
            my_pluto.backward()
    elif action == 'scroll':
        if dy > 0:
            my_pluto.increase_height()
        elif dy < 0:
            my_pluto.decrease_height()

def on_click(x, y, button, pressed):
    identify_mouse_action('click', x, y, button, pressed, None, None)

def on_move(x, y):
    identify_mouse_action('move', x, y, None, None, None, None)

def on_scroll(x, y, dx, dy):
    identify_mouse_action('scroll', x, y, None, None, dx, dy)

# Collect events until released
with mouse.Listener(
        on_click=on_click,
        on_move=on_move,
        on_scroll=on_scroll) as listener:
    listener.join()
