"""
Motor Control Module
====================
This module controls 4 DC motors using PWM (Pulse Width Modulation) on Raspberry Pi GPIO pins.
Each motor can be driven forward or backward at variable speeds.

Hardware Setup:
- Uses L298N motor driver boards (2 boards controlling 2 motors each)
- Motor 1 & 2: Left side (Front-Left, Back-Left)
- Motor 3 & 4: Right side (Front-Right, Back-Right)

Key Concepts:
- GPIO: General Purpose Input/Output pins on Raspberry Pi
- PWM: Pulse Width Modulation - controls motor speed by rapidly switching power on/off
- Duty Cycle: Percentage of time power is ON (0-100%). Higher = faster motor speed
- H-Bridge: Circuit that allows motors to spin both directions
"""

import RPi.GPIO as GPIO
import time

# Global motor PWM objects
# These will be initialized by initMotors() and used by all motor functions
motor1_forward = None
motor1_backward = None
motor2_forward = None
motor2_backward = None
motor3_forward = None
motor3_backward = None
motor4_forward = None
motor4_backward = None


def initMotors():
    """
    Initialize GPIO pins and create PWM objects for all 4 motors.
    
    This function MUST be called before using any motor control functions.
    It sets up the GPIO pins and creates PWM (Pulse Width Modulation) objects
    that allow us to control motor speed and direction.
    
    GPIO Pin Assignments:
    ---------------------
    Motor 1 (Front-Left):  GPIO 21 (forward), GPIO 20 (backward)
    Motor 2 (Back-Left):   GPIO 16 (forward), GPIO 26 (backward)
    Motor 3 (Front-Right): GPIO 19 (forward), GPIO 13 (backward)
    Motor 4 (Back-Right):  GPIO 6 (forward),  GPIO 5 (backward)
    
    PWM Frequency: 100 Hz
    - This means the signal switches on/off 100 times per second
    - Higher frequency = smoother motor operation
    """
    # Use 'global' keyword to modify the module-level variables
    global motor1_forward, motor1_backward
    global motor2_forward, motor2_backward
    global motor3_forward, motor3_backward
    global motor4_forward, motor4_backward
    
    print('Initializing motors...')
    
    # Set GPIO numbering mode to BCM (Broadcom chip-specific pin numbers)
    # This means we use GPIO numbers (like GPIO 21) not physical pin numbers (like Pin 40)
    GPIO.setmode(GPIO.BCM)
    
    # Configure each GPIO pin as an OUTPUT pin
    # Motor 1 pins
    GPIO.setup(20, GPIO.OUT)  # Motor 1 backward
    GPIO.setup(21, GPIO.OUT)  # Motor 1 forward
    
    # Motor 2 pins
    GPIO.setup(16, GPIO.OUT)  # Motor 2 forward
    GPIO.setup(26, GPIO.OUT)  # Motor 2 backward
    
    # Motor 3 pins
    GPIO.setup(19, GPIO.OUT)  # Motor 3 forward
    GPIO.setup(13, GPIO.OUT)  # Motor 3 backward
    
    # Motor 4 pins
    GPIO.setup(6, GPIO.OUT)   # Motor 4 forward
    GPIO.setup(5, GPIO.OUT)   # Motor 4 backward

    # Create PWM objects for each motor direction
    # GPIO.PWM(pin, frequency) - frequency is in Hz (cycles per second)
    motor1_forward = GPIO.PWM(21, 100)
    motor1_backward = GPIO.PWM(20, 100)
    motor2_forward = GPIO.PWM(16, 100)
    motor2_backward = GPIO.PWM(26, 100)
    motor3_forward = GPIO.PWM(19, 100)
    motor3_backward = GPIO.PWM(13, 100)
    motor4_forward = GPIO.PWM(6, 100)
    motor4_backward = GPIO.PWM(5, 100)

    # Start all PWM signals at 0% duty cycle (motors stopped)
    # .start(duty_cycle) - duty_cycle is 0-100 percentage
    motor1_forward.start(0)
    motor1_backward.start(0)
    motor2_forward.start(0)
    motor2_backward.start(0)
    motor3_forward.start(0)
    motor3_backward.start(0)
    motor4_forward.start(0)
    motor4_backward.start(0)
    
    print('Motors initialized!')


def moveMotor1(amount):
    """
    Control Motor 1 (Front-Left wheel).
    
    Parameters:
    -----------
    amount : float
        Speed and direction: -1.0 (full backward) to 1.0 (full forward)
        0 = stopped
        
    How it works:
    -------------
    - Positive values: Set forward pin to PWM, backward pin to 0
    - Negative values: Set backward pin to PWM, forward pin to 0
    - Values near zero (±0.1): Turn off both pins (deadzone prevents motor hum)
    """
    if amount > 0.1:
        # Moving forward
        motor1_forward.ChangeDutyCycle(amount * 100)  # Convert 0-1 to 0-100%
        motor1_backward.ChangeDutyCycle(0)            # Turn off backward
    elif amount < -0.1:
        # Moving backward
        motor1_backward.ChangeDutyCycle(-amount * 100)  # Use absolute value
        motor1_forward.ChangeDutyCycle(0)               # Turn off forward
    else:
        # Stopped (deadzone: -0.1 to 0.1)
        motor1_forward.ChangeDutyCycle(0)
        motor1_backward.ChangeDutyCycle(0)


def moveMotor2(amount):
    """
    Control Motor 2 (Back-Left wheel).
    See moveMotor1() for parameter details.
    """
    if amount > 0.1:
        motor2_forward.ChangeDutyCycle(amount * 100)
        motor2_backward.ChangeDutyCycle(0)
    elif amount < -0.1:
        motor2_backward.ChangeDutyCycle(-amount * 100)
        motor2_forward.ChangeDutyCycle(0)
    else:
        motor2_forward.ChangeDutyCycle(0)
        motor2_backward.ChangeDutyCycle(0)


def moveMotor3(amount):
    """
    Control Motor 3 (Front-Right wheel).
    See moveMotor1() for parameter details.
    """
    if amount > 0.1:
        motor3_forward.ChangeDutyCycle(amount * 100)
        motor3_backward.ChangeDutyCycle(0)
    elif amount < -0.1:
        motor3_backward.ChangeDutyCycle(-amount * 100)
        motor3_forward.ChangeDutyCycle(0)
    else:
        motor3_forward.ChangeDutyCycle(0)
        motor3_backward.ChangeDutyCycle(0)


def moveMotor4(amount):
    """
    Control Motor 4 (Back-Right wheel).
    See moveMotor1() for parameter details.
    """
    if amount > 0.1:
        motor4_forward.ChangeDutyCycle(amount * 100)
        motor4_backward.ChangeDutyCycle(0)
    elif amount < -0.1:
        motor4_backward.ChangeDutyCycle(-amount * 100)
        motor4_forward.ChangeDutyCycle(0)
    else:
        motor4_forward.ChangeDutyCycle(0)
        motor4_backward.ChangeDutyCycle(0)


# Legacy functions for simple forward/backward control
# These are kept for compatibility with older code

def motorForward(amount):
    """
    Drive Motor 1 forward at specified speed.
    
    Parameters:
    -----------
    amount : float
        Speed from 0.0 (stopped) to 1.0 (full speed)
        
    Note: This is a simple function that only controls Motor 1.
    For full robot control, use moveMotor1-4 or the mecanum module.
    """
    motor1_backward.ChangeDutyCycle(0)
    motor1_forward.ChangeDutyCycle(amount * 100)


def motorBackward(amount):
    """
    Drive Motor 1 backward at specified speed.
    
    Parameters:
    -----------
    amount : float
        Speed from 0.0 (stopped) to 1.0 (full speed)
        
    Note: This is a simple function that only controls Motor 1.
    For full robot control, use moveMotor1-4 or the mecanum module.
    """
    motor1_forward.ChangeDutyCycle(0)
    motor1_backward.ChangeDutyCycle(amount * 100)
