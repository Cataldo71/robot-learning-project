"""
Controller Input Module
=======================
This module handles input from a game controller (like Xbox or PlayStation controller).
It uses the evdev library to read controller events and converts them into easy-to-use
button presses and joystick movements.

Key Concepts:
- evdev: Linux library for reading input device events
- Event codes: Numbers that represent different buttons and sticks
- Callback functions: Functions you provide that get called when inputs happen
"""

import evdev
from evdev import InputDevice, categorize, ecodes
import time

# Path to the controller device in Linux
# /dev/input/event2 is typically where USB game controllers appear
# Bluetooth controllers may appear at different event numbers (event3, event4, etc.)
# Check with: ls /dev/input/event* or cat /proc/bus/input/devices | grep -A 5 "Xbox"
# See docs/XBOX_CONTROLLER_BLUETOOTH.md for Bluetooth setup
controller_path = '/dev/input/event2'
controller = None  # Will hold the controller object once connected


def connectToController():
    """
    Connect to the game controller.
    
    This function will keep trying to connect until it succeeds.
    This is helpful because you can plug in the controller after starting the program.
    
    For Bluetooth controllers: Make sure the controller is turned on and has
    auto-connected (you should see a solid Xbox button, not flashing).
    
    Uses 'global' keyword because we're modifying the module-level 'controller' variable.
    """
    global controller
    retry_count = 0
    
    while controller is None:
        try:
            # Try to open the controller device
            controller = InputDevice(controller_path)
            print(f"✓ Controller connected at {controller_path}")
            print(f"  Device: {controller.name}")
        except (FileNotFoundError, PermissionError) as e:
            # Controller not found - wait and try again
            retry_count += 1
            if retry_count == 1:
                print(f"Looking for controller at {controller_path}...")
                print("  - If using USB: Make sure it's plugged in")
                print("  - If using Bluetooth: Turn on controller (press Xbox button)")
                print("  - See docs/XBOX_CONTROLLER_BLUETOOTH.md for setup help")
                print()
            elif retry_count % 5 == 0:
                print(f"Still waiting for controller... (attempt {retry_count})")
                print(f"  Tip: Check if device path is correct with: ls /dev/input/event*")
            
            time.sleep(1)


# Dictionary mapping event codes (numbers) to friendly button/stick names
# These codes come from the evdev library and vary by controller type
# This mapping is for a typical Xbox-style controller
buttonNames = {
    # Face buttons
    304: 'A',
    305: 'B',
    308: 'X',
    307: 'Y',
    
    # Shoulder buttons and triggers
    313: 'RB',      # Right bumper
    311: 'RT',      # Right trigger
    310: 'LT',      # Left trigger
    312: 'LB',      # Left bumper
    
    # Special buttons
    316: 'home',    # Xbox/PS button
    315: 'start',   # Start button
    
    # D-pad (directional pad)
    16: 'pad-X',    # D-pad left/right
    17: 'pad-Y',    # D-pad up/down
    
    # Analog sticks (joysticks)
    0: 'stick1-X',  # Left stick left/right
    1: 'stick1-Y',  # Left stick up/down
    3: 'stick2-X',  # Right stick left/right
    4: 'stick2-Y',  # Right stick up/down
    5: 'stick3-Y',  # Left trigger analog (some controllers)
    2: 'stick3-X'   # Right trigger analog (some controllers)
}


def eventLoop(onButton, onStick):
    """
    Main event loop - continuously reads controller input.
    
    This function runs forever, reading events from the controller and calling
    your callback functions when buttons are pressed or sticks are moved.
    
    Parameters:
    -----------
    onButton : function
        Callback function for button events. Called with (button_name, value)
        Example: onButton('A', 1.0) when A button is pressed
        
    onStick : function
        Callback function for stick/joystick events. Called with (stick_name, value)
        Example: onStick('stick1-Y', 0.5) when left stick is pushed halfway up
        
    How it works:
    -------------
    1. Read events from the controller in a continuous loop
    2. Check if event is a button (EV_KEY) or stick (EV_ABS)
    3. Convert the event code to a friendly name using buttonNames dictionary
    4. Normalize the value (divide by 32767 to get range -1.0 to 1.0)
    5. Call the appropriate callback function
    """
    global controller
    
    # read_loop() returns events as they happen - this loop never ends!
    for event in controller.read_loop():
        # Check if this is a button press/release (EV_KEY) or joystick movement (EV_ABS)
        if event.type in [ecodes.EV_KEY, ecodes.EV_ABS]:
            
            # Joystick events have codes 0-5
            if event.code <= 5 and event.code in buttonNames:
                # Normalize joystick value: raw values are -32767 to 32767
                # We convert to -1.0 to 1.0 for easier use
                normalized_value = event.value / 32767
                onStick(buttonNames[event.code], normalized_value)
                
            # Button events have codes > 5
            elif event.code in buttonNames:
                # Button values: 0 = released, 1 = pressed
                # We normalize to 0.0 or 1.0 for consistency
                normalized_value = event.value / 32767
                onButton(buttonNames[event.code], normalized_value)
                
            # Uncomment this to see unmapped buttons/sticks:
            # else:
            #     print('Unknown event code:', event.code)
