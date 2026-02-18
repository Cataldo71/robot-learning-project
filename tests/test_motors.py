#!/usr/bin/env python3
"""
Motor Test Script
=================
This script tests each motor individually to verify wiring and functionality.
It's useful for:
- Checking that motors are connected correctly
- Verifying motor directions (if a motor spins backwards, swap its wires)
- Testing that GPIO pins and motor controllers are working

The script will:
1. Spin each motor forward for 1 second
2. Spin each motor backward for 1 second
3. Move through all 4 motors in sequence
4. Stop and clean up

Use this BEFORE running the full robot to ensure all motors work correctly!
"""

from robot.motor import initMotors, moveMotor1, moveMotor2, moveMotor3, moveMotor4
import time

if __name__ == '__main__':
    print("=" * 60)
    print("Motor Test Program")
    print("=" * 60)
    print()
    print("This script will test each motor in sequence.")
    print("Watch the motors and verify they spin in the correct direction.")
    print()
    print("Motor Layout:")
    print("    FRONT")
    print("  ┌─────────┐")
    print("  │  1   3  │")
    print("  │         │")
    print("  │  2   4  │")
    print("  └─────────┘")
    print("    BACK")
    print()
    print("-" * 60)
    print()
    
    # Initialize the motor hardware
    print("Initializing motors...")
    initMotors()
    print()
    
    # Test each motor forward and backward
    motors = [
        (1, moveMotor1, "Motor 1 (Front-Left)"),
        (2, moveMotor2, "Motor 2 (Back-Left)"),
        (3, moveMotor3, "Motor 3 (Front-Right)"),
        (4, moveMotor4, "Motor 4 (Back-Right)")
    ]
    
    for motor_num, motor_func, motor_name in motors:
        # Test forward
        print(f"Testing {motor_name}:")
        print(f"  → Forward...", end="", flush=True)
        motor_func(1.0)  # Full speed forward
        time.sleep(1)
        
        # Test backward
        print(" Backward...", end="", flush=True)
        motor_func(-1.0)  # Full speed backward
        time.sleep(1)
        
        # Stop
        motor_func(0)
        print(" Stopped ✓")
        time.sleep(0.5)  # Brief pause between motors
    
    print()
    print("-" * 60)
    print("Motor test complete!")
    print()
    print("Troubleshooting:")
    print("  - If a motor doesn't move: Check wiring and power supply")
    print("  - If a motor spins backward: Swap the two motor wires")
    print("  - If all motors fail: Check enable jumpers on L298N boards")
    print()
    print("=" * 60)
