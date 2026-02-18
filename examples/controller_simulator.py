#!/usr/bin/env python3
"""
Controller Input Test (Advanced)
=================================
This script tests controller input WITHOUT requiring motor hardware.
It's perfect for:
- Verifying your controller is connected and working
- Learning what values controllers send
- Understanding mecanum wheel math (shows calculated motor values)
- Debugging controller issues

What it does:
-------------
1. Connects to your game controller
2. Displays button presses and releases
3. Shows joystick positions as numbers (-1.0 to 1.0)
4. Calculates and displays what motor powers WOULD be set (simulated)

Learning concepts:
------------------
- Event-driven programming (callbacks)
- Global state variables
- Simulating hardware for testing
- Vector mathematics for robot control

For simpler examples, see: example_read_controller.py

Usage: python3 example_controller_simulator.py
Press Ctrl+C to exit.
"""

from robot.controller import eventLoop, connectToController
from robot.mecanum import makeMotorVector

# Global variables to track controller state
# These represent the current movement commands from the controller
forward = 0  # Forward/backward: -1.0 (backward) to 1.0 (forward)
left = 0     # Strafe left/right: -1.0 (right) to 1.0 (left)
turn = 0     # Rotation: -1.0 (right) to 1.0 (left)

def simulateMotors(powerVec):
    """
    Display simulated motor power values.
    
    This function shows what motor powers WOULD be set if motors
    were connected, but doesn't actually control any hardware.
    
    Parameters:
    -----------
    powerVec : list of 4 floats
        Motor power values for [FL, BL, FR, BR] (Front/Back, Left/Right)
        Each value is in range -1.0 to 1.0
        
    Output format:
    --------------
    Motors: FL=+0.707, BL=+0.707, FR=+0.707, BR=+0.707
    """
    print(f"  → Motors: FL={powerVec[0]:6.3f}, BL={powerVec[1]:6.3f}, FR={powerVec[2]:6.3f}, BR={powerVec[3]:6.3f}")


def setMotors():
    """
    Calculate and display motor values without actually moving motors.
    
    This is the heart of the simulation. It:
    1. Takes current forward, left, and turn values
    2. Uses mecanum wheel math to calculate motor powers
    3. Displays what those powers would be
    
    This lets students see the relationship between controller input
    and motor output without needing physical hardware.
    """
    # Calculate motor power vector using mecanum wheel kinematics
    vec = makeMotorVector(forward, left, turn)
    
    # Display the calculated values
    simulateMotors(vec)


def onButton(button, value):
    """
    Callback for controller button events.
    
    This function is called automatically whenever a button is pressed
    or released on the controller.
    
    Parameters:
    -----------
    button : str
        Button name ('A', 'B', 'X', 'Y', 'start', 'LB', 'RB', etc.)
    value : float
        1.0 when pressed, 0.0 when released
        
    Educational note:
    -----------------
    This is an example of a "callback function" - a function you write
    that gets called automatically by other code (the event loop) when
    something happens (a button press).
    """
    state = "PRESSED" if value > 0 else "RELEASED"
    print(f"Button {button:8s} {state}")


def onStick(stick, value):
    """
    Callback for controller joystick events.
    
    This function is called automatically whenever a joystick (analog stick)
    is moved on the controller.
    
    Parameters:
    -----------
    stick : str
        Stick identifier ('stick1-X', 'stick1-Y', 'stick2-X', 'stick2-Y')
    value : float
        Stick position: -1.0 (left/up) to 1.0 (right/down)
        Center position is 0.0
        
    How it works:
    -------------
    1. Receive stick movement event with name and value
    2. Update the appropriate global variable (forward/left/turn)
    3. Recalculate and display motor values
    
    Why we negate values:
    ---------------------
    Stick "up" returns -1.0, but we want "up" to mean "forward" (+1.0)
    So we flip the sign: forward = -value
    """
    # Use 'global' because we're modifying module-level variables
    global forward, left, turn
    
    # Display the raw stick event
    print(f"Stick  {stick:9s} = {value:6.3f}", end="")
    
    if stick == 'stick1-Y':
        # Left stick vertical: controls forward/backward
        # Negate because stick up (-1.0) should mean forward (+1.0)
        forward = -value
        print(f"  → Forward: {forward:6.3f}")
        setMotors()  # Show updated motor values
        
    elif stick == 'stick1-X':
        # Left stick horizontal: controls left/right strafe
        # Negate because stick left (-1.0) should mean left (+1.0)
        left = -value
        print(f"  → Left:    {left:6.3f}")
        setMotors()
        
    elif stick == 'stick2-X':
        # Right stick horizontal: controls rotation
        # Negate because stick left should rotate left (counter-clockwise)
        turn = -value
        print(f"  → Turn:    {turn:6.3f}")
        setMotors()
    else:
        # Other sticks (stick2-Y, etc.) - just show the value
        print()


if __name__ == '__main__':
    """
    Main program entry point.
    
    The 'if __name__ == "__main__":' pattern means this code only runs
    when the script is executed directly (not when imported as a module).
    
    This is Python best practice for scripts that can be both:
    - Run directly: python3 example_controller_simulator.py
    - Imported by other code: import example_controller_simulator
    """
    print("=" * 60)
    print("Controller Input Test (No Hardware Required)")
    print("=" * 60)
    print("This script will display controller input without moving motors.")
    print()
    print("Controls:")
    print("  Left Stick Y  - Forward/Backward")
    print("  Left Stick X  - Left/Right strafe")
    print("  Right Stick X - Turn left/right")
    print("  All Buttons   - Display press/release events")
    print()
    print("What you'll see:")
    print("  - Raw stick values (-1.0 to 1.0)")
    print("  - Translated movement values (Forward, Left, Turn)")
    print("  - Calculated motor powers (FL, BL, FR, BR)")
    print()
    print("Waiting for controller to connect...")
    print()
    
    try:
        # Connect to the controller (waits until found)
        connectToController()
        print("✓ Controller connected!")
        print("Move sticks and press buttons to see input values.")
        print("Watch how motor values change based on your input!")
        print("Press Ctrl+C to exit.")
        print("-" * 60)
        print()
        
        # Start the event loop (runs forever until Ctrl+C)
        eventLoop(onButton, onStick)
        
    except KeyboardInterrupt:
        # User pressed Ctrl+C - clean exit
        print("\n")
        print("-" * 60)
        print("Test stopped by user.")
        print()
        print("What you learned:")
        print("  ✓ How to read controller input")
        print("  ✓ How joystick values work (-1.0 to 1.0)")
        print("  ✓ How mecanum wheel math combines movements")
        print("  ✓ Event-driven programming with callbacks")
        print("=" * 60)
        
    except Exception as e:
        # Something went wrong - show error
        print(f"\nError: {e}")
        print("Make sure your controller is connected.")
        print()
        print("Troubleshooting:")
        print("  - Is controller plugged in via USB?")
        print("  - Check: ls /dev/input/event* ")
        print("  - You may need to change controller_path in controller.py")
