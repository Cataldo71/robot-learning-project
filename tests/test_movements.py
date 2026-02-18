#!/usr/bin/env python3
"""
Mecanum Drive Movement Test
============================
This script demonstrates the different movement capabilities of a mecanum
wheel robot by executing a sequence of movements.

Requires: Motor hardware to be connected

Movements demonstrated:
- Forward
- Backward  
- Strafe left
- Strafe right
- Rotate left (counter-clockwise)
- Rotate right (clockwise)

This is useful for:
- Testing that all motors are wired correctly
- Verifying mecanum wheel math is working
- Demonstrating robot capabilities
- Learning about vector-based robot control
"""

from robot.mecanum import makeMotorVector, driveMotors, stopMotors
from robot.motor import initMotors
import time

if __name__ == '__main__':
    print("=" * 60)
    print("Mecanum Drive Movement Test")
    print("=" * 60)
    print()
    print("This script will demonstrate various mecanum wheel movements.")
    print("The robot will perform each movement for 2 seconds.")
    print()
    print("-" * 60)
    print()
    
    # Initialize motor hardware
    initMotors()
    
    # List of test movements: (forward, left, turn, description)
    movements = [
        (1, 0, 0, "Moving FORWARD"),
        (-1, 0, 0, "Moving BACKWARD"),
        (0, 1, 0, "Strafing LEFT"),
        (0, -1, 0, "Strafing RIGHT"),
        (0, 0, 1, "Rotating LEFT (counter-clockwise)"),
        (0, 0, -1, "Rotating RIGHT (clockwise)")
    ]
    
    # Execute each movement
    for forward, left, turn, description in movements:
        print(f"{description}...")
        
        # Calculate motor powers for this movement
        motor_vector = makeMotorVector(forward, left, turn)
        print(f"  Motor powers: {[f'{v:+.2f}' for v in motor_vector]}")
        
        # Apply the motor powers
        driveMotors(motor_vector)
        
        # Hold this movement for 2 seconds
        time.sleep(2)
        
        # Stop between movements
        stopMotors()
        print(f"  Stopped")
        print()
        time.sleep(0.5)
    
    # Final stop
    stopMotors()
    
    print("-" * 60)
    print("Movement test complete!")
    print()
    print("Next steps:")
    print("  - Try combining movements: makeMotorVector(0.5, 0.5, 0)")
    print("  - Test with controller: python3 run_robot.py")
    print("=" * 60)



