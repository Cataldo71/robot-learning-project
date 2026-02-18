"""
Simple Controller Test (Beginner Level)
========================================
This is a minimal example showing how to read controller input.
Perfect for learning the basics of controller event handling!

Concepts demonstrated:
- Connecting to a controller
- Defining callback functions
- Reading button presses
- Reading joystick movements
- Event loop basics

For a more advanced controller test, see: example_controller_simulator.py
"""

from robot.controller import eventLoop, connectToController

print('Simple Controller Test starting...')
print()

# Connect to the controller (will wait until it's plugged in)
connectToController()
print('Connected to Controller')
print('Press buttons and move sticks - output will appear below:')
print('-' * 60)
print()


def onButton(button, value):
    """
    Called whenever a button is pressed or released.
    
    Parameters:
    -----------
    button : str
        The button name (e.g., 'A', 'B', 'X', 'Y', 'start')
    value : float
        1.0 when pressed, 0.0 when released
    """
    print('button', button, value)


def onStick(stick, value):
    """
    Called whenever a joystick (analog stick) is moved.
    
    Parameters:
    -----------
    stick : str
        The stick name (e.g., 'stick1-X', 'stick1-Y', 'stick2-X')
    value : float
        Position from -1.0 (left/up) to 1.0 (right/down)
    """
    print('stick', stick, value)


# Start the event loop - this will call onButton() and onStick()
# automatically whenever controller input happens
# Press Ctrl+C to exit
eventLoop(onButton, onStick)

print("done")
