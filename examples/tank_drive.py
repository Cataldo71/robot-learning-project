"""
Simple Controller to Motor Example (Intermediate Level)
========================================================
This script shows how to use controller input to control motors directly.
It's a simplified tank-drive example for the full 4-motor robot,
where each joystick controls one side of the drivetrain.

This is an educational stepping stone between:
- example_read_controller.py (just reading input)
- run_robot.py (full mecanum drive control)

Concepts demonstrated:
- Connecting controller input to motor output
- Simple tank-drive style control (not mecanum)
- Direct motor control without vector math

Requirements:
- 4 motors (Motor 1-4)
- Game controller

Controls:
- Left stick Y-axis: Controls left side (Motor 1 + Motor 2)
- Right stick Y-axis: Controls right side (Motor 3 + Motor 4)

Note: This does NOT use mecanum wheel math. For full mecanum control,
use run_robot.py instead.
"""

import sys
import os
# Add parent directory to path so we can import robot package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from robot import controller
from robot import motor
from robot.controller import eventLoop
from robot.motor import motorForward, motorBackward, moveMotor1, moveMotor2, moveMotor3, moveMotor4, initMotors

print('Controller to Motor Example')
print('=' * 60)
print()
print('Initializing motors...')

# Initialize the motor hardware
initMotors()

print('Motors ready!')
print()
print('This example uses simple tank-drive control:')
print('  - Left stick Y:  Controls left side (Motor 1 + Motor 2)')
print('  - Right stick Y: Controls right side (Motor 3 + Motor 4)')
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
    
    This maps each stick to one side of the robot:
    - Left stick (stick1-Y) → Left side (Motor 1 + Motor 2)
    - Right stick (stick2-Y) → Right side (Motor 3 + Motor 4)
    
    This creates "tank drive" style control where each side
    is controlled independently, like a tank or bulldozer.
    """
    print('stick', stick, value)
    
    if stick == 'stick1-Y':
        # Left stick controls LEFT side motors
        # Positive = forward, negative = backward
        moveMotor1(value)
        moveMotor2(value)
        
    elif stick == 'stick2-Y':
        # Right stick controls RIGHT side motors
        # Note: if right side runs opposite, invert these values in wiring or code
        moveMotor3(value)
        moveMotor4(value)


# Start the event loop
# This will continuously read controller input and call our functions
eventLoop(onButton, onStick)
