"""
Drive Robot Main Program
=========================
This is the main program that connects controller input to motor output.
It reads joystick movements from a game controller and translates them
into motor commands for a mecanum wheel robot.

Program Flow:
-------------
1. Import all necessary modules (controller, motor, mecanum)
2. Define callback functions for button and stick events
3. Initialize hardware (motors and controller)
4. Start event loop (runs forever, processing controller input)

Controls:
---------
Left Stick Y-axis:  Forward/Backward movement
Left Stick X-axis:  Left/Right strafing
Right Stick X-axis: Rotation (turning)
Buttons: Currently just print to console (you can add functionality!)
"""

from . import controller
from . import motor
from .controller import eventLoop, connectToController
from .motor import motorForward, motorBackward, moveMotor1, moveMotor2, initMotors
import time
from .mecanum import makeMotorVector, driveMotors

# Global variables to track current movement commands
# These are updated by controller input and used to calculate motor powers
left = 0       # Strafe left/right (-1.0 to 1.0)
forward = 0    # Move forward/backward (-1.0 to 1.0)
turn = 0       # Rotate left/right (-1.0 to 1.0)


# Example function for testing motors (currently commented out)
# def doHelloDance():
#     """Make the robot 'dance' by moving motors in a pattern."""
#     moveMotor1(1)
#     moveMotor2(1)
#     time.sleep(1)
#     moveMotor1(-1)
#     moveMotor2(-1)
#     time.sleep(1)
#     moveMotor1(0)
#     moveMotor2(0)


x = 0  # Legacy variables (not currently used)
y = 0


def onButton(button, value):
    """
    Callback function for controller button presses.
    
    This function is called automatically by the controller event loop
    whenever a button is pressed or released.
    
    Parameters:
    -----------
    button : str
        Name of the button ('A', 'B', 'X', 'Y', 'start', etc.)
    value : float
        1.0 if pressed, 0.0 if released
        
    Current behavior:
    -----------------
    Just prints the button event to the console.
    
    Ideas for expansion:
    --------------------
    - Use 'A' button to switch between speed modes (slow/fast)
    - Use 'B' button to stop all motors
    - Use 'start' button to reset robot position
    - Use triggers to control a robot arm or gripper
    """
    print('button', button, value)


def clipValue(value):
    """
    Limit a value to the range -1.0 to 1.0.
    
    This prevents motor commands from exceeding safe limits.
    Currently not used because mecanum.makeMotorVector() handles
    normalization automatically.
    
    Parameters:
    -----------
    value : float
        Any numeric value
        
    Returns:
    --------
    float : Value clamped to range [-1.0, 1.0]
    """
    return min(1, max(-1, value))


def setMotors():
    """
    Calculate and apply motor powers based on current movement commands.
    
    This function combines the current forward, left, and turn values
    into a motor power vector using the mecanum wheel math, then applies
    those powers to the actual motors.
    
    Flow:
    -----
    1. Call makeMotorVector() with current forward, left, turn values
    2. Get back a list of 4 motor power values
    3. Pass that list to driveMotors() to actually move the motors
    
    Why this is separate:
    ---------------------
    By having this in one function, we ensure all motors are updated
    together and consistently. Any time a control input changes, we
    call setMotors() to recalculate everything.
    """
    # Uncomment this line to see the current control values:
    # print('values', forward, left, turn)
    
    # Calculate motor powers using mecanum wheel kinematics
    vec = makeMotorVector(forward, left, turn)
    
    # Apply the calculated powers to the motors
    driveMotors(vec)
    
    # Alternative simple two-motor control (commented out):
    # moveMotor1(clipValue(y - x))
    # moveMotor2(-clipValue(y + x))


def onStick(stick, value):
    """
    Callback function for controller joystick movements.
    
    This function is called automatically by the controller event loop
    whenever a joystick (analog stick) is moved.
    
    Parameters:
    -----------
    stick : str
        Name of the stick ('stick1-X', 'stick1-Y', 'stick2-X', etc.)
    value : float
        Position of the stick (-1.0 to 1.0)
        - For Y axes: -1.0 = up, 1.0 = down
        - For X axes: -1.0 = left, 1.0 = right
        
    Stick Mapping:
    --------------
    stick1-Y (Left stick vertical):   Forward/Backward
    stick1-X (Left stick horizontal): Left/Right strafe
    stick2-X (Right stick horizontal): Rotation
    
    Why 'global'?
    -------------
    We use the 'global' keyword because we need to modify the module-level
    variables (forward, left, turn) that are defined outside this function.
    Without 'global', Python would create new local variables instead.
    """
    # Uncomment this line to see all stick movements:
    # print('stick', stick, value)
    
    # Declare that we're modifying the global variables
    global forward
    global left
    global turn
    
    if stick == 'stick1-Y':
        # Left stick vertical axis controls forward/backward
        # We negate the value because stick up (-1.0) should mean forward (+1.0)
        forward = -value
        setMotors()  # Recalculate and apply new motor powers
        
    elif stick == 'stick1-X':
        # Left stick horizontal axis controls left/right strafe
        # We negate because stick left (-1.0) should mean left (+1.0)
        left = -value
        setMotors()
        
    elif stick == 'stick2-X':
        # Right stick horizontal axis controls rotation
        # We negate because stick left should rotate left (counter-clockwise)
        turn = -value
        setMotors()


def start():
    """
    Initialize hardware and start the robot control loop.
    
    This is the main entry point for the robot program. It performs
    all initialization steps and then enters the event loop.
    
    Steps:
    ------
    1. Print startup message
    2. Initialize motor hardware (GPIO pins and PWM)
    3. Connect to the game controller
    4. Print ready message
    5. Enter event loop (runs forever until program is stopped)
    
    The event loop will continuously call onButton() and onStick()
    as controller events occur.
    
    To stop:
    --------
    Press Ctrl+C to exit the program
    """
    print('Starting: Drive Robot')
    
    # Initialize motors (sets up GPIO pins and PWM)
    initMotors()
    
    # Connect to controller (waits until controller is found)
    connectToController()
    print('Connected to Controller')
    
    print('Ready to drive!')
    
    # Start the event loop (this function never returns)
    # It will call onButton() and onStick() as events occur
    eventLoop(onButton, onStick)
