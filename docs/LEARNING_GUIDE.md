# Easy Robot - Learning Guide for Students

## 🎓 Welcome to Robotics Programming!

This project teaches you how to build and program a mecanum wheel robot using a Raspberry Pi. The code is organized to help you learn step by step.

---

## 📚 Learning Path

Follow these steps in order to build your understanding:

### Level 1: Understanding Controllers

Learn how game controllers work and how to read their input.

**File:** `examples/read_controller.py` ⭐ Start here
- **Purpose:** Simple controller input reading
- **Concepts:** Callbacks, event loops, controller buttons/sticks
- **Run:** `python3 examples/read_controller.py`
- **No hardware needed:** Just a USB controller

**File:** `examples/controller_simulator.py` ⭐ More advanced
- **Purpose:** Controller test with motor simulation
- **Concepts:** Global variables, mecanum math preview
- **Run:** `python3 examples/controller_simulator.py`
- **Shows:** What motor powers would be (simulated)

---

### Level 2: Controlling Motors

Learn how to control DC motors with PWM.

**File:** `robot/motor.py` (library)
- **Purpose:** Motor control functions
- **Concepts:** GPIO, PWM, H-bridges, duty cycle
- **Functions:**
  - `initMotors()` - Set up hardware
  - `moveMotor1()` through `moveMotor4()` - Control individual motors
  
**File:** `tests/test_motors.py` ⭐ Test your motors
- **Purpose:** Test each motor individually
- **Run:** `python3 tests/test_motors.py`
- **Requires:** Motors connected to Raspberry Pi
- **What it does:** Spins each motor forward and backward

---

### Level 3: Mecanum Wheel Math

Understand how mecanum wheels allow omnidirectional movement.

**File:** `robot/mecanum.py` (library)
- **Purpose:** Calculate motor powers for complex movements
- **Concepts:** Vectors, linear algebra, kinematics
- **Key Functions:**
  - `makeMotorVector(forward, left, turn)` - Main calculation
  - `driveMotors(powerVec)` - Apply calculated powers

**File:** `tests/test_movements.py` ⭐ See mecanum in action
- **Purpose:** Demonstrate various movements
- **Run:** `python3 tests/test_movements.py`
- **Requires:** Motors connected
- **Shows:** Forward, backward, strafe, rotate

---

### Level 4: Combining Everything

Put controller input and motor control together!

**File:** `examples/tank_drive.py` ⭐ Simple tank drive
- **Purpose:** Direct control (not mecanum)
- **Concepts:** Connecting input to output
- **Run:** `python3 examples/tank_drive.py`
- **Requires:** Motors + Controller

**File:** `robot/drive.py` (library)
- **Purpose:** Full mecanum drive control logic
- **Concepts:** State management, event handling
- **Functions:**
  - `start()` - Main entry point
  - `onButton()` - Handle button presses
  - `onStick()` - Handle joystick movements

**File:** `run_robot.py` ⭐ Full robot control
- **Purpose:** Complete robot operation
- **Run:** `python3 run_robot.py`
- **Requires:** Everything connected
- **This is the main program!**

---

## 🗂️ Project Structure

```
easy-robo/
├── Core Modules (Libraries)
│   ├── controller.py      - Game controller input handling
│   ├── motor.py           - DC motor control with PWM
│   ├── mecanum.py         - Mecanum wheel mathematics
│   └── driverobot.py      - Main robot control logic
│
├── Main Program
│   └── run_robot.py       - 🤖 Run the complete robot (USE THIS!)
│
├── Examples (No motors needed)
│   ├── example_read_controller.py    - Simple controller test
│   └── example_controller_simulator.py - Advanced controller test with simulation
│
├── Examples & Tests (Motors needed)
│   ├── test_motors.py        - Test individual motors
│   ├── test_movements.py     - Test mecanum movements
│   └── example_tank_drive.py - Simple tank drive example
│
└── Documentation
    ├── README.md           - Project overview
    ├── LEARNING_GUIDE.md   - This file!
    └── GPIO_WIRING_GUIDE.md - Hardware wiring instructions
```

---

## 🎮 Controller Mapping

Your game controller controls the robot like this:

```
┌─────────────────────────────────────┐
│  [LB]       Controller        [RB]  │
│                                      │
│   ◄►  Left Stick (stick1)            │
│   ▲▼  • Y-axis: Forward/Backward    │
│       • X-axis: Strafe Left/Right   │
│                                      │
│            [A] [B]                   │
│            [X] [Y]                   │
│                                      │
│              Right Stick (stick2) ◄► │
│              • X-axis: Rotate        │
│              • Y-axis: (not used)    │
│                                      │
└─────────────────────────────────────┘
```

---

## 🤖 How Mecanum Wheels Work

Mecanum wheels have diagonal rollers that create motion at 45° angles:

```
    FRONT
  ┌─────────┐
  │  ↖   ↗ │   Each wheel can push at 45°
  │         │   
  │  ↙   ↘ │   By combining wheels, we get:
  └─────────┘   - Forward/Backward
    BACK        - Left/Right (strafe)
                - Rotation
                - Any combination!
```

### Movement Examples:

**Forward:** All wheels spin forward
```
Motor1: +1    Motor3: +1
Motor2: +1    Motor4: +1
```

**Strafe Left:** Opposite diagonal pairs
```
Motor1: -1    Motor3: +1
Motor2: +1    Motor4: -1
```

**Rotate Left:** Left side backward, right side forward
```
Motor1: -1    Motor3: +1
Motor2: -1    Motor4: +1
```

**Diagonal Forward-Left:** Combination of forward + left
```
Motor1:  0    Motor3: +1
Motor2: +1    Motor4:  0
```

---

## 🔧 Hardware Setup

### What You Need:
- Raspberry Pi 5 (or Pi 4)
- 4× DC motors (with mecanum wheels)
- 2× L298N motor driver boards
- 12V power supply (at least 10A)
- USB game controller
- Jumper wires

### Wiring:
See `GPIO_WIRING_GUIDE.md` for complete wiring instructions!

**Quick Reference:**
- Motor 1 (Front-Left): GPIO 21 & 20
- Motor 2 (Back-Left):  GPIO 16 & 26
- Motor 3 (Front-Right): GPIO 19 & 13
- Motor 4 (Back-Right):  GPIO 6 & 5

---

## 🚀 Quick Start Guide

### Step 0: Install Required Libraries (First Time Only)

**For Raspberry Pi 5:**
```bash
sudo apt update
sudo apt install -y python3-evdev python3-rpi-lgpio
```

**For Raspberry Pi 4 and older:**
```bash
sudo apt update
sudo apt install -y python3-evdev python3-rpi.gpio
```

### Step 1: Test Without Hardware
```bash
# Test your controller (no motors needed)
python3 examples/read_controller.py
# Press buttons and move sticks
# Press Ctrl+C to exit
```

### Step 2: Test Motors
```bash
# Test each motor individually (requires sudo for GPIO)
sudo python3 tests/test_motors.py
# Watch motors spin forward then backward
```

### Step 3: Test Movements
```bash
# Test mecanum movements (requires sudo for GPIO)
sudo python3 tests/test_movements.py
# Watch robot perform different movements
```

### Step 4: Run the Robot!
```bash
# Full robot control with game controller (requires sudo for GPIO)
sudo python3 run_robot.py
# Drive around!
# Press Ctrl+C to stop
```

---

## 💡 Programming Concepts You'll Learn

### 1. **Modules and Imports**
```python
import motor                    # Import entire module
from motor import initMotors   # Import specific function
```

### 2. **Functions**
```python
def moveMotor1(amount):
    """Control motor 1 speed and direction"""
    # Function body here
```

### 3. **Callback Functions**
```python
def onButton(button, value):
    """Called automatically when button is pressed"""
    print(f"Button {button} = {value}")
```

### 4. **Global Variables**
```python
forward = 0  # Module-level variable

def updateForward(value):
    global forward  # Must declare to modify
    forward = value
```

### 5. **Pulse Width Modulation (PWM)**
```python
motor = GPIO.PWM(pin, frequency)  # Create PWM on a pin
motor.start(0)                     # Start at 0% duty cycle
motor.ChangeDutyCycle(50)          # Set to 50% power
```

### 6. **Event-Driven Programming**
```python
# Program waits for events, then responds
eventLoop(onButton, onStick)  # Calls your functions when events occur
```

### 7. **Vector Mathematics**
```python
# Combine multiple movements into motor powers
forward_vec = [1, 1, 1, 1]
left_vec = [-1, 1, 1, -1]
result = forward_vec[i] * forward + left_vec[i] * left
```

---

## 🐛 Troubleshooting

### Controller Not Found
```bash
# Check if controller is detected
ls /dev/input/event*

# If it's not event2, edit controller.py:
controller_path = '/dev/input/event3'  # or whatever you found
```

### Permission Denied (GPIO)
```bash
# Run with sudo for GPIO access
sudo python3 run_robot.py
```

### Motor Spins Wrong Direction
- Swap the two motor wires on that motor
- Don't change the code!

### Motor Doesn't Move
1. Check enable jumpers on L298N boards
2. Verify power supply is connected and ON
3. Check wiring with docs/GPIO_WIRING_GUIDE.md
4. Test with `python3 tests/test_motors.py`

### All Motors Too Fast/Slow
Edit the duty cycle values in motor.py:
```python
motor1_forward.ChangeDutyCycle(amount * 50)  # 50% max instead of 100%
```

---

## 🎯 Learning Challenges

Try these modifications to deepen your learning:

### Beginner Challenges:
1. **Change button behavior:** Make the 'A' button stop all motors
2. **Add speed control:** Use triggers to adjust maximum speed
3. **Print debug info:** Show motor values in the console

### Intermediate Challenges:
1. **Add LED indicators:** Light up LEDs when moving
2. **Create movement sequences:** Program autonomous routines
3. **Add sensor input:** Use ultrasonic sensor to detect obstacles

### Advanced Challenges:
1. **Implement PID control:** Smooth out motor response
2. **Add position tracking:** Estimate robot position (odometry)
3. **Create a web interface:** Control robot from a webpage
4. **Add computer vision:** Use camera for line following

---

## 📖 Key Files Explained

### `robot/controller.py` - Controller Interface
- Reads USB game controller input
- Converts raw event codes to friendly names
- Provides clean callback interface
- **Students learn:** Event handling, dictionaries, device I/O

### `robot/motor.py` - Motor Control
- Configures GPIO pins for PWM output
- Provides functions to control each motor
- Handles forward/backward logic with deadzone
- **Students learn:** GPIO, PWM, hardware control

### `robot/mecanum.py` - Robot Mathematics
- Implements mecanum wheel kinematics
- Combines movement vectors (forward, left, turn)
- Normalizes values to prevent motor overdrive
- **Students learn:** Vector math, algorithms, robotics

### `robot/drive.py` - Main Logic
- Connects controller input to motor output
- Maintains robot state (current forward/left/turn)
- Coordinates all subsystems
- **Students learn:** System integration, state management

---

## 🎓 Further Learning

### Robotics Concepts:
- **Kinematics:** How robot geometry affects movement
- **Odometry:** Estimating position from wheel rotations
- **PID Control:** Smooth, precise motor control
- **Sensor Fusion:** Combining multiple sensor inputs

### Programming Concepts:
- **Object-Oriented Programming:** Create Robot class
- **Threading:** Run multiple tasks simultaneously
- **Network Programming:** Remote control over WiFi
- **Computer Vision:** Process camera images

### Electronics:
- **H-Bridge Circuits:** How motor drivers work
- **PWM Theory:** Understanding duty cycle and frequency
- **Power Distribution:** Managing voltage and current
- **Sensor Integration:** Adding ultrasonic, IMU, cameras

---

## 📚 Additional Resources

- **Project Website:** https://messyprogress.substack.com/p/easy-robotics-with-a-3d-printer-and
- **Raspberry Pi GPIO:** https://pinout.xyz
- **Python Documentation:** https://docs.python.org/3/
- **L298N Datasheet:** Search "L298N motor driver"
- **Mecanum Wheels:** Search "mecanum wheel kinematics"

---

## 🎉 Congratulations!

You now have all the knowledge to:
- ✅ Control motors with PWM
- ✅ Read game controller input
- ✅ Implement mecanum wheel drive
- ✅ Build a complete robot control system

**What will you build next?**

---

## 📝 Quick Command Reference

```bash
# First Time Setup - Install required libraries
# For Raspberry Pi 5:
sudo apt install -y python3-evdev python3-rpi-lgpio
# For Raspberry Pi 4 and older:
sudo apt install -y python3-evdev python3-rpi.gpio

# Examples (No Hardware) - Can run from any directory
python3 examples/read_controller.py      # Simple controller test
python3 examples/controller_simulator.py # Advanced controller test

# Tests (Hardware Required) - Need sudo for GPIO access
sudo python3 tests/test_motors.py          # Test individual motors
sudo python3 tests/test_movements.py       # Test mecanum movements
sudo python3 examples/tank_drive.py        # Simple tank drive

# Main Program - Need sudo for GPIO access
sudo python3 run_robot.py                  # Full robot control ⭐

# Stop Any Program
Ctrl+C                                # Press in terminal
```

---

**Happy Building! 🤖**

*Made for students learning robotics and Python programming.*
