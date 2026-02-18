# GPIO Wiring Guide - Raspberry Pi 5 with L298N Motor Controllers

## Hardware Overview
- **Raspberry Pi 5** - Main controller
- **2x L298N Motor Driver Boards** - Dual H-bridge motor controllers
- **4x DC Motors** - Mecanum wheel configuration
- **Power Supply** - 12V for motors (L298N can handle 5-35V)

---

## Motor Layout (Mecanum Wheels)

```
    FRONT
  ┌─────────┐
  │  1   3  │
  │         │
  │  2   4  │
  └─────────┘
    BACK

Motor 1: Front-Left
Motor 2: Back-Left
Motor 3: Front-Right
Motor 4: Back-Right
```

---

## Raspberry Pi 5 GPIO Pinout (Relevant Pins)

```
        3.3V  [ 1] [ 2]  5V
              [ 3] [ 4]  5V
              [ 5] [ 6]  GND
              [ 7] [ 8]  
         GND  [ 9] [10]  
    GPIO 17  [11] [12]  
    GPIO 27  [13] [14]  GND
    GPIO 22  [15] [16]  
        3.3V [17] [18]  
              [19] [20]  GND
              [21] [22]  
              [23] [24]  
         GND  [25] [26]  
              [27] [28]  
     GPIO 5  [29] [30]  GND
     GPIO 6  [31] [32]  
    GPIO 13  [33] [34]  GND
    GPIO 19  [35] [36]  GPIO 16
    GPIO 26  [37] [38]  GPIO 20
         GND [39] [40]  GPIO 21
```

---

## GPIO Pin Assignments (From Code)

| GPIO Pin | Physical Pin | Function | Motor Controller |
|----------|--------------|----------|------------------|
| GPIO 21  | Pin 40       | Motor 1 Forward | Controller A - IN1 |
| GPIO 20  | Pin 38       | Motor 1 Backward | Controller A - IN2 |
| GPIO 16  | Pin 36       | Motor 2 Forward | Controller A - IN3 |
| GPIO 26  | Pin 37       | Motor 2 Backward | Controller A - IN4 |
| GPIO 19  | Pin 35       | Motor 3 Forward | Controller B - IN1 |
| GPIO 13  | Pin 33       | Motor 3 Backward | Controller B - IN2 |
| GPIO 6   | Pin 31       | Motor 4 Forward | Controller B - IN3 |
| GPIO 5   | Pin 29       | Motor 4 Backward | Controller B - IN4 |

---

## L298N Motor Controller Pinout

Each L298N has these connections:

```
L298N Motor Driver Board
┌────────────────────────────────┐
│                                │
│  Motor A  [OUT1] [OUT2]        │  ← Connect to Motor 1 or 3
│  Motor B  [OUT3] [OUT4]        │  ← Connect to Motor 2 or 4
│                                │
│  Control  [IN1]  [IN2]         │  ← PWM signals from Pi
│  Inputs   [IN3]  [IN4]         │  ← PWM signals from Pi
│                                │
│  Enable   [ENA]  [ENB]         │  ← Jumpers ON (or PWM for speed)
│                                │
│  Power    [12V]  [GND] [5V]    │  
│                                │
└────────────────────────────────┘
```

---

## Wiring Diagram

### Controller A (Left Side Motors - Motors 1 & 2)

```
Raspberry Pi          L298N Controller A          Motors
GPIO 21 (Pin 40) ──→ IN1  ──→ OUT1 ──┐
GPIO 20 (Pin 38) ──→ IN2  ──→ OUT2 ──┴─→ Motor 1 (Front-Left)

GPIO 16 (Pin 36) ──→ IN3  ──→ OUT3 ──┐
GPIO 26 (Pin 37) ──→ IN4  ──→ OUT4 ──┴─→ Motor 2 (Back-Left)

GND (Pin 39)     ──→ GND
                     12V  ←─── 12V Power Supply (+)
                     GND  ←─── 12V Power Supply (-)
```

### Controller B (Right Side Motors - Motors 3 & 4)

```
Raspberry Pi          L298N Controller B          Motors
GPIO 19 (Pin 35) ──→ IN1  ──→ OUT1 ──┐
GPIO 13 (Pin 33) ──→ IN2  ──→ OUT2 ──┴─→ Motor 3 (Front-Right)

GPIO 6  (Pin 31) ──→ IN3  ──→ OUT3 ──┐
GPIO 5  (Pin 29) ──→ IN4  ──→ OUT4 ──┴─→ Motor 4 (Back-Right)

GND (Pin 30)     ──→ GND
                     12V  ←─── 12V Power Supply (+)
                     GND  ←─── 12V Power Supply (-)
```

---

## Complete Wiring Checklist

### For Each L298N Motor Controller:

✅ **Power Connections:**
- [ ] Connect 12V from power supply to **12V** terminal
- [ ] Connect GND from power supply to **GND** terminal
- [ ] Connect Raspberry Pi GND to motor controller **GND** (share common ground)
- [ ] Leave **5V** output disconnected (or use for Pi if PSU doesn't have built-in 5V out)

✅ **Enable Jumpers:**
- [ ] Place jumpers on **ENA** and **ENB** pins (enables motors)
- [ ] Alternative: Connect to GPIO for speed control (not used in current code)

✅ **GPIO Connections:**
- [ ] IN1, IN2, IN3, IN4 to respective GPIO pins (see table above)
- [ ] Use Female-to-Female jumper wires

✅ **Motor Connections:**
- [ ] Connect motor wires to OUT1/OUT2 for Motor A
- [ ] Connect motor wires to OUT3/OUT4 for Motor B
- [ ] If motor spins backwards, swap the two motor wires

---

## Power Supply Requirements

- **Voltage:** 6-12V DC (typical for hobby DC motors)
- **Current:** At least 2A per motor = 8A total minimum
- **Recommended:** 12V 10A power supply with barrel connector
- **Important:** Do NOT power motors from Raspberry Pi's 5V pins!

---

## Safety Notes

⚠️ **CRITICAL:**
1. **NEVER** connect motor power directly to Raspberry Pi
2. **ALWAYS** share common ground between Pi and motor controllers
3. **CHECK** polarity before connecting power supply
4. **TEST** one motor at a time initially
5. **FUSE** your power supply if possible (10A fuse recommended)

---

## Testing Sequence

1. **Power OFF** - Wire everything with power disconnected
2. **Visual Check** - Verify all connections against this diagram
3. **Power ON** - Connect power supply (motors should NOT move)
4. **Test Controller** - Run `python3 examples/controller_simulator.py` (no motor movement)
5. **Test Motors** - Run `python3 tests/test_motors.py` to test individual motors
6. **Full Test** - Run `python3 run_robot.py` with controller

---

## Troubleshooting

### Motor doesn't move:
- Check enable jumpers (ENA/ENB) are in place
- Verify GPIO pin connections
- Test motor directly with power supply
- Check motor controller has power (LED should be on)

### Motor spins wrong direction:
- Swap the two motor wires on OUT terminals
- Or modify code to invert the PWM signal

### Multiple motors don't work:
- Check power supply can provide enough current
- Verify common ground connection
- Test each motor controller independently

---

## Reference Links

- **Project Page:** https://messyprogress.substack.com/p/easy-robotics-with-a-3d-printer-and
- **Motor Controllers:** https://www.amazon.com/dp/B07BK1QL5T
- **Raspberry Pi GPIO:** https://pinout.xyz

---

## Quick Reference: GPIO to Pin Mapping

```python
# Motor 1 (Front-Left)
GPIO 21 (Pin 40) → Forward
GPIO 20 (Pin 38) → Backward

# Motor 2 (Back-Left)  
GPIO 16 (Pin 36) → Forward
GPIO 26 (Pin 37) → Backward

# Motor 3 (Front-Right)
GPIO 19 (Pin 35) → Forward
GPIO 13 (Pin 33) → Backward

# Motor 4 (Back-Right)
GPIO 6  (Pin 31) → Forward
GPIO 5  (Pin 29) → Backward

# Ground connections
Pin 30, 39 (or any GND pin) → Motor Controller GND
```

---

**Last Updated:** February 16, 2026  
**Hardware:** Raspberry Pi 5 + 2x L298N + 4x Mecanum Motors
