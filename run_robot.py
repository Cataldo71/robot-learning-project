#!/usr/bin/env python3
"""
Run Robot - Full Mecanum Drive Control
=======================================
This is the main program to run your complete robot with hardware.

What it does:
-------------
1. Initializes GPIO pins and motor controllers
2. Connects to your game controller
3. Starts the main control loop
4. Translates controller input into mecanum wheel movements

Requirements:
-------------
- Raspberry Pi with GPIO access
- 4 DC motors with L298N motor controllers
- 12V power supply for motors
- USB game controller
- All wiring completed per GPIO_WIRING_GUIDE.md

Controls:
---------
- Left Stick Y:  Move Forward/Backward
- Left Stick X:  Strafe Left/Right
- Right Stick X: Rotate Left/Right

Advanced: All three can be used simultaneously for diagonal
movement while rotating!

Safety:
-------
- Keep the robot on a non-slip surface
- Have emergency stop ready (Ctrl+C or power switch)
- Start with small stick movements to test
- Don't let it drive off tables!

Usage:
------
python3 run_robot.py

Press Ctrl+C to stop the robot and exit.

Learning Path:
--------------
If this is your first time:
1. Test motors individually: python3 tests/test_motors.py
2. Test controller input: python3 examples/controller_simulator.py
3. Test movements: python3 tests/test_movements.py (if safe to run)
4. Finally, run this script!
"""

from robot import drive as driverobot
import time

if __name__ == '__main__':
    print("=" * 60)
    print("Robot Control System - Full Hardware Mode")
    print("=" * 60)
    print()
    print("⚠️  WARNING: This will control real motors!")
    print()
    print("Make sure:")
    print("  ✓ Robot is on the ground or elevated safely")
    print("  ✓ Power supply is connected")
    print("  ✓ You can reach the stop button/plug")
    print("  ✓ Motors are wired correctly (test with tests/test_motors.py)")
    print("  ✓ Controller is connected (USB or Bluetooth)")
    print()
    print("Controls:")
    print("  Left Stick Y  → Forward/Backward")
    print("  Left Stick X  → Strafe Left/Right")
    print("  Right Stick X → Rotate")
    print()
    print("Controller Setup:")
    print("  USB: Plug in controller and it should work automatically")
    print("  Bluetooth: Turn on controller (see docs/XBOX_CONTROLLER_BLUETOOTH.md)")
    print()
    print("To stop: Press Ctrl+C")
    print()
    print("-" * 60)
    print()
    print("Waiting for controller to connect...")
    print("(If using Bluetooth, turn on your controller now)")
    print()
    
    # Brief delay to allow Bluetooth controllers to auto-connect
    time.sleep(2)
    
    try:
        # Start the robot (initializes hardware and begins event loop)
        # This function call will not return until the program is stopped
        driverobot.start()
        
    except KeyboardInterrupt:
        # User pressed Ctrl+C - this is the normal way to stop
        print("\n")
        print("-" * 60)
        print("Robot stopped by user.")
        print("Motors should now be stopped.")
        print("It's safe to disconnect power.")
        print("=" * 60)
        
    except Exception as e:
        # Something went wrong - show error and stop
        print(f"\n⚠️  ERROR: {e}")
        print()
        print("The robot has been stopped due to an error.")
        print()
        print("Common issues:")
        print("  - Controller not connected (USB or Bluetooth)")
        print("  - Wrong controller path (check docs/XBOX_CONTROLLER_BLUETOOTH.md)")
        print("  - GPIO permissions (try: sudo python3 run_robot.py)")
        print("  - Motor controller wiring")
        print("  - Power supply not connected")
        print()
        print("Guides:")
        print("  - Wiring: docs/GPIO_WIRING_GUIDE.md")
        print("  - Bluetooth: docs/XBOX_CONTROLLER_BLUETOOTH.md")
