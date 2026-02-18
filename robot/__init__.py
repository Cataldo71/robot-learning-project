"""
Robot Control Library
=====================
A Python package for controlling a mecanum wheel robot with Raspberry Pi.

This package provides:
- controller: Game controller input handling
- motor: DC motor control with PWM
- mecanum: Mecanum wheel kinematics
- drive: Main robot control logic

Example usage:
--------------
    from robot.motor import initMotors, moveMotor1
    from robot.controller import connectToController, eventLoop
    from robot.mecanum import makeMotorVector, driveMotors
    from robot.drive import start
    
    # Run the complete robot
    start()
"""

# Make key components easily accessible
from robot import controller, motor, mecanum, drive

__version__ = "1.0.0"
__all__ = ['controller', 'motor', 'mecanum', 'drive']
