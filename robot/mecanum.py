"""
Mecanum Wheel Drive System
===========================
This module calculates motor power values for a 4-wheel mecanum drive robot.
Mecanum wheels allow the robot to move in any direction without rotating,
and to rotate in place.

What are Mecanum Wheels?
-------------------------
Mecanum wheels have diagonal rollers at 45° angles. By controlling the speed
and direction of each wheel independently, the robot can:
- Move forward/backward
- Strafe left/right (move sideways)
- Rotate in place
- Move diagonally
- Combine all movements simultaneously!

Motor Layout:
-------------
    FRONT
  ┌─────────┐
  │  1   3  │   Motor 1: Front-Left
  │         │   Motor 2: Back-Left
  │  2   4  │   Motor 3: Front-Right
  └─────────┘   Motor 4: Back-Right
    BACK

Key Concepts:
-------------
- Vector: A direction and magnitude (like "move forward at 50% speed")
- Linear Combination: Adding multiple movements together (forward + left = diagonal)
- Normalization: Scaling values so motors don't exceed 100% power
"""

from .motor import moveMotor1, moveMotor2, moveMotor3, moveMotor4

# Base movement vectors for mecanum wheels
# Each vector shows how the 4 motors should spin for that movement
# Values: [Motor1, Motor2, Motor3, Motor4]
# Positive = forward/clockwise, Negative = backward/counter-clockwise

forwardVec = [1, 1, 1, 1]      # All wheels spin forward
leftVec = [-1, 1, 1, -1]       # Front-left & back-right backward, others forward
turnVec = [-1, -1, 1, 1]       # Left side backward, right side forward


def driveMotors(powerVec):
    """
    Apply power values to all 4 motors.
    
    Parameters:
    -----------
    powerVec : list of 4 floats
        Power for each motor [-1.0 to 1.0]
        Format: [Motor1, Motor2, Motor3, Motor4]
        
    Example:
    --------
    driveMotors([1.0, 1.0, 1.0, 1.0])  # Full speed forward
    driveMotors([0, 0, 0, 0])           # Stop all motors
    """
    moveMotor1(powerVec[0])
    moveMotor2(powerVec[1])
    moveMotor3(powerVec[2])
    moveMotor4(powerVec[3])


def stopMotors():
    """
    Stop all motors immediately.
    
    This is equivalent to driveMotors([0, 0, 0, 0])
    """
    driveMotors([0, 0, 0, 0])


def combinePower(index, forward, left, turn):
    """
    Calculate power for one motor by combining movement commands.
    
    This is the mathematical heart of mecanum drive control. It takes three
    movement commands (forward, left, turn) and combines them using the
    base vectors to determine how much power one specific motor needs.
    
    Parameters:
    -----------
    index : int
        Which motor (0=Motor1, 1=Motor2, 2=Motor3, 3=Motor4)
    forward : float
        Forward/backward command (-1.0 to 1.0)
    left : float
        Left/right strafe command (-1.0 to 1.0)
    turn : float
        Rotation command (-1.0 to 1.0)
        
    Returns:
    --------
    float : Power value for this motor (-1.0 to 1.0)
    
    How it works:
    -------------
    1. Multiply each movement by its base vector value for this motor
       Example for Motor 1:
       - forward * forwardVec[0] = forward * 1
       - left * leftVec[0] = left * -1
       - turn * turnVec[0] = turn * -1
       
    2. Add them all together (linear combination)
       
    3. Divide by the sum of absolute values to normalize
       This prevents the total from exceeding ±1.0
       
    Example:
    --------
    If forward=1.0, left=1.0, turn=0:
    - Without normalization: could be 2.0 (too much!)
    - With normalization: scaled to 1.0 (maximum safe value)
    """
    # Calculate the sum of absolute input values for normalization
    # max() with 1 ensures we never divide by zero
    divisor = max(abs(forward) + abs(left) + abs(turn), 1)
    
    # Combine the three movement vectors, weighted by their input values
    combined = (forwardVec[index] * forward + 
                leftVec[index] * left + 
                turnVec[index] * turn)
    
    # Normalize to keep values in the range -1.0 to 1.0
    return combined / divisor


def makeMotorVector(forward, left, turn):
    """
    Create a motor power vector from movement commands.
    
    This is the main function you'll use to control the robot. Give it
    three simple commands (forward, left, turn) and it calculates the
    exact power needed for each of the 4 motors.
    
    Parameters:
    -----------
    forward : float
        Forward (+) / Backward (-) speed (-1.0 to 1.0)
    left : float
        Strafe left (+) / Strafe right (-) speed (-1.0 to 1.0)
    turn : float
        Turn left (+) / Turn right (-) speed (-1.0 to 1.0)
        
    Returns:
    --------
    list : [Motor1_power, Motor2_power, Motor3_power, Motor4_power]
           Each value is between -1.0 and 1.0
           
    Examples:
    ---------
    makeMotorVector(1, 0, 0)      # Move forward
    makeMotorVector(0, 1, 0)      # Strafe left
    makeMotorVector(0, 0, 1)      # Rotate left
    makeMotorVector(0.5, 0.5, 0)  # Move forward-left diagonal
    makeMotorVector(0.7, 0, 0.3)  # Move forward while turning left
    """
    return [
        combinePower(0, forward, left, turn),  # Motor 1 (Front-Left)
        combinePower(1, forward, left, turn),  # Motor 2 (Back-Left)
        combinePower(2, forward, left, turn),  # Motor 3 (Front-Right)
        combinePower(3, forward, left, turn),  # Motor 4 (Back-Right)
    ]
