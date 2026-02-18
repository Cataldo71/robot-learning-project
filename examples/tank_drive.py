"""
Simple Controller to Motor Example (Intermediate Level)
========================================================
This script shows how to use controller input to control motors directly.
It's a simplified version that controls just 2 motors (left and right)
using the controller joysticks.

This is an educational stepping stone between:
- example_read_controller.py (just reading input)
- run_robot.py (full mecanum drive control)

Concepts demonstrated:
- Connecting controller input to motor output
- Simple tank-drive style control (not mecanum)
- Direct motor control without vector math

Requirements:
- 2 motors minimum (Motor 1 and Motor 2)
- Game controller

Controls:
- Left stick Y-axis: Controls Motor 1 (left side)
- Right stick Y-axis: Controls Motor 2 (right side)

Note: This does NOT use mecanum wheel math. For full mecanum control,
use run_robot.py instead.
"""

from robot import controller
from robot import motor
from robot.controller import eventLoop
from robot.motor import motorForward, motorBackward, moveMotor1, moveMotor2, initMotors

print('Controller to Motor Example')
print('=' * 60)
print()
print('Initializing motors...')

# Initialize the motor hardware
initMotors()

print('Motors ready!')
print()
print('This example uses simple tank-drive control:')
print('  - Left stick Y:  Controls Motor 1 (left side)')
print('  - Right stick Y: Controls Motor 2 (right side)')
print()
print('Press Ctrl+C to exit')
print('-' * 60)
print()


def onButton(button, value):
    """
    Handle button presses.
    Currently just prints to console - you could add functionality here!
    
    Ideas:
    - Emergency stop button
    - Speed mode selector
    - Motor enable/disable
    """
    print('button', button, value)


def onStick(stick, value):
    """
    Handle joystick movements and control motors.
    
    This maps each stick directly to a motor:
    - Left stick (stick1-Y) → Motor 1
    - Right stick (stick2-Y) → Motor 2
    
    This creates "tank drive" style control where each side
    is controlled independently, like a tank or bulldozer.
    """
    print('stick', stick, value)
    
    if stick == 'stick1-Y':
        # Left stick controls Motor 1
        # We pass 'value' directly - positive = forward, negative = backward
        moveMotor1(value)
        
    elif stick == 'stick2-Y':
        # Right stick controls Motor 2
        # We negate the value because this motor faces opposite direction
        # (This depends on your wiring - adjust if needed)
        moveMotor2(-value)


# Start the event loop
# This will continuously read controller input and call our functions
eventLoop(onButton, onStick)
