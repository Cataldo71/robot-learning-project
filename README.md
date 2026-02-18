# easy-robo
Code for Simple Raspberry Pi Robots

## 🤖 Mecanum Wheel Robot Controller

A complete beginner-friendly robotics project for building and programming a mecanum wheel robot using:
- Raspberry Pi 5 (or Pi 4)
- 4× DC motors with mecanum wheels
- 2× L298N motor driver boards
- USB game controller

## 🚀 Quick Start

### 1. Software Setup (First Time Only)

**For Raspberry Pi 5:**
```bash
# Install required libraries
sudo apt update
sudo apt install -y python3-evdev python3-rpi-lgpio
```

**For Raspberry Pi 4 and older:**
```bash
# Install required libraries
sudo apt update
sudo apt install -y python3-evdev python3-rpi.gpio
```

**Note:** Raspberry Pi 5 uses `rpi-lgpio` which is a drop-in replacement for the older `RPi.GPIO` library. The code works with both!

### 2. For Students Learning Robotics:
See **[docs/LEARNING_GUIDE.md](docs/LEARNING_GUIDE.md)** for complete learning path from beginner to advanced!

### 3. For Hardware Setup:
See **[docs/GPIO_WIRING_GUIDE.md](docs/GPIO_WIRING_GUIDE.md)** for complete wiring instructions.

### 4. To Run the Robot:
```bash
# 1. Test controller (no motors needed)
python3 examples/read_controller.py

# 2. Test motors (requires sudo for GPIO access)
sudo python3 tests/test_motors.py

# 3. Run the robot!
sudo python3 run_robot.py
```

## 📁 Project Structure

```
easy-robo/
├── robot/                    # Core library package
│   ├── __init__.py
│   ├── controller.py         # Game controller input
│   ├── motor.py              # Motor control with PWM
│   ├── mecanum.py            # Mecanum wheel math
│   └── drive.py              # Main robot logic
│
├── examples/                 # Learning examples (no motors needed)
│   ├── read_controller.py
│   ├── controller_simulator.py
│   └── tank_drive.py
│
├── tests/                    # Hardware tests
│   ├── test_motors.py
│   └── test_movements.py
│
├── docs/                     # Documentation
│   ├── LEARNING_GUIDE.md
│   └── GPIO_WIRING_GUIDE.md
│
├── run_robot.py              # Main program - run the robot!
├── README.md
└── LICENSE
```

## 🎮 Controls

- **Left Stick Y** - Forward/Backward
- **Left Stick X** - Strafe Left/Right
- **Right Stick X** - Rotate Left/Right

All three can be used simultaneously for complex movements!

## 📚 Learning Path

1. Progress through `examples/` to understand controller input
2. Test motors individually with `tests/test_motors.py`
3. Run the full robot with `run_robot.py`!

See [docs/LEARNING_GUIDE.md](docs/LEARNING_GUIDE.md) for detailed instructions.

## 🔗 Resources

- **Project Website**: https://messyprogress.substack.com/p/easy-robotics-with-a-3d-printer-and
- **Motor Controllers**: https://www.amazon.com/dp/B07BK1QL5T

## 📄 License

See [LICENSE](LICENSE) file for details.
