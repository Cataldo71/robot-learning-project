# Xbox Controller Bluetooth Setup for Raspberry Pi

## 🎮 Connecting Your Xbox Controller via Bluetooth

This guide shows you how to pair an Xbox One/Series controller to your Raspberry Pi using Bluetooth instead of USB. This gives you wireless control of your robot!

---

## ✅ Compatible Controllers

This guide works with:
- **Xbox One Controller** (Model 1708 and newer - has Bluetooth)
- **Xbox One S Controller** (white with textured grip)
- **Xbox Series X|S Controller** (latest model)

**Note:** The original Xbox One controller (Model 1537, released 2013) does NOT have Bluetooth. Check if yours has a plastic piece around the Xbox button - if it does, it's the older model without Bluetooth.

---

## 📋 Prerequisites

- Raspberry Pi with built-in Bluetooth (Pi 3, 4, 5, Zero W)
- Xbox controller with Bluetooth support
- Fresh AA batteries or charged battery pack
- Updated Raspberry Pi OS

---

## 🚀 Quick Start Guide

### Step 1: Update Your System

Open a terminal and run:

```bash
# Update package lists
sudo apt update

# Upgrade packages (optional but recommended)
sudo apt upgrade -y

# Install Bluetooth tools (usually pre-installed)
sudo apt install -y bluetooth bluez bluez-tools
```

---

### Step 2: Start Bluetooth Service

Ensure Bluetooth is running:

```bash
# Start Bluetooth service
sudo systemctl start bluetooth

# Enable Bluetooth to start on boot
sudo systemctl enable bluetooth

# Check Bluetooth status
sudo systemctl status bluetooth
```

You should see "active (running)" in green.

---

### Step 3: Enter Bluetooth Control Mode

Launch the Bluetooth control tool:

```bash
bluetoothctl
```

You'll see a `[bluetooth]#` prompt. All following commands are entered here.

---

### Step 4: Prepare Bluetooth for Pairing

In the `bluetoothctl` prompt:

```bash
# Turn on the Bluetooth controller
power on

# Make Pi discoverable
discoverable on

# Enable agent for authentication
agent on

# Set agent as default
default-agent

# Start scanning for devices
scan on
```

You should see:
```
[bluetooth]# scan on
Discovery started
[CHG] Controller ... Discovering: yes
```

---

### Step 5: Put Xbox Controller in Pairing Mode

**For Xbox One/Series Controllers:**

1. Turn on the controller by pressing the **Xbox button**
2. Press and hold the small **Pair button** on top of the controller (next to the USB port)
3. The Xbox button will start **flashing rapidly** - this means pairing mode is active
4. Keep holding for 3-5 seconds, then release

**Pair button locations:**
- **Xbox One S/X:** Small circular button on top edge, between LB and RB
- **Xbox Series X|S:** Small button on the front face, between the USB-C port and shoulder buttons

---

### Step 6: Find the Controller

In the `bluetoothctl` terminal, you'll see devices appear:

```
[NEW] Device B8:27:EB:XX:XX:XX Xbox Wireless Controller
```

Look for "Xbox Wireless Controller" or similar. Copy the MAC address (the XX:XX:XX:XX:XX:XX part).

**Tip:** If you don't see it after 10 seconds:
- Put controller back in pairing mode (step 5)
- Make sure controller batteries are fresh
- Move controller closer to Raspberry Pi

---

### Step 7: Pair the Controller

Replace `XX:XX:XX:XX:XX:XX` with your controller's MAC address:

```bash
# Stop scanning
scan off

# Pair with the controller
pair XX:XX:XX:XX:XX:XX

# Trust the device (auto-connect in future)
trust XX:XX:XX:XX:XX:XX

# Connect to the controller
connect XX:XX:XX:XX:XX:XX
```

Example:
```bash
pair B8:27:EB:12:34:56
trust B8:27:EB:12:34:56
connect B8:27:EB:12:34:56
```

You should see:
```
[CHG] Device XX:XX:XX:XX:XX:XX Connected: yes
[CHG] Device XX:XX:XX:XX:XX:XX Paired: yes
```

The controller's Xbox button should be **solid white** (not flashing).

---

### Step 8: Exit Bluetooth Control

```bash
# Exit bluetoothctl
exit
```

Your controller is now paired and connected!

---

## 🔍 Verify Connection

Check if the controller appears as an input device:

```bash
# List input devices
ls /dev/input/
```

You should see `event0`, `event1`, `event2`, etc. Your controller is typically one of these.

To find which one:

```bash
# Show detailed input device info
cat /proc/bus/input/devices
```

Look for an entry with:
```
N: Name="Xbox Wireless Controller"
H: Handlers=js0 event2
```

The `event2` (or similar) is your controller's device path.

---

## 🔧 Update Controller Path in Code

If your controller is NOT at `/dev/input/event2`, update the code:

Edit [robot/controller.py](../robot/controller.py):

```bash
nano robot/controller.py
```

Find this line (near the top):
```python
controller_path = '/dev/input/event2'
```

Change to your actual path (e.g., `event3`, `event4`):
```python
controller_path = '/dev/input/event3'
```

Save and exit (Ctrl+X, Y, Enter).

---

## ✅ Test the Controller

Run a simple test:

```bash
# Test controller input (no motors needed)
python3 examples/read_controller.py
```

Press buttons and move sticks - you should see output in the terminal.

**If it works:** Your controller is ready! Proceed to run the robot.

**If nothing happens:** See troubleshooting section below.

---

## 🔄 Auto-Connect on Startup

Your controller should auto-connect when turned on (because we used `trust`).

To connect manually if needed:

```bash
bluetoothctl
connect XX:XX:XX:XX:XX:XX
exit
```

Or use this shortcut:

```bash
echo "connect XX:XX:XX:XX:XX:XX" | bluetoothctl
```

---

## 🔋 Power Management

Xbox controllers will auto-sleep after ~15 minutes of inactivity to save battery.

To wake it up:
- Press the **Xbox button**
- It should reconnect within 5 seconds

If it doesn't reconnect:
- Check Bluetooth is running: `sudo systemctl status bluetooth`
- Manually reconnect: `echo "connect XX:XX:XX:XX:XX:XX" | bluetoothctl`

---

## 🐛 Troubleshooting

### Controller Won't Enter Pairing Mode

**Symptoms:** Xbox button won't flash when holding pair button

**Solutions:**
- Replace batteries (must be at least 50% charged)
- Try a different Xbox controller
- Make sure it's a Bluetooth-enabled model (see Compatible Controllers section)

---

### Controller Not Discovered During Scan

**Symptoms:** Controller flashing but not appearing in `bluetoothctl`

**Solutions:**
1. **Start over:**
   ```bash
   scan off
   scan on
   ```
   Then put controller back in pairing mode

2. **Check Bluetooth status:**
   ```bash
   sudo systemctl restart bluetooth
   bluetoothctl
   power on
   scan on
   ```

3. **Move closer:** Bluetooth has limited range (~10 meters), move controller next to Pi

4. **Remove old pairings:** On the controller, hold pair button for 15+ seconds to reset

---

### Pairing Fails with "Failed to pair: org.bluez.Error.AuthenticationFailed"

**Solutions:**
1. **Remove existing pairing:**
   ```bash
   bluetoothctl
   remove XX:XX:XX:XX:XX:XX
   scan on
   ```
   Then try pairing again

2. **Restart Bluetooth:**
   ```bash
   sudo systemctl restart bluetooth
   ```
   Then retry pairing

---

### Controller Connects but Python Script Shows "Controller not found"

**Solutions:**
1. **Find correct event device:**
   ```bash
   cat /proc/bus/input/devices | grep -A 5 "Xbox"
   ```
   Look for `Handlers=event3` (or similar)

2. **Update controller_path in code:**
   Edit `robot/controller.py` and change:
   ```python
   controller_path = '/dev/input/event3'  # Your actual device
   ```

3. **Check permissions:**
   ```bash
   ls -l /dev/input/event*
   ```
   You should have read permission. If not:
   ```bash
   sudo chmod a+r /dev/input/event*
   ```
   Or run your Python script with `sudo`:
   ```bash
   sudo python3 run_robot.py
   ```

---

### Controller Disconnects Frequently

**Solutions:**
- **Battery check:** Replace with fresh batteries
- **Interference:** Move away from WiFi routers, microwaves, other Bluetooth devices
- **Range:** Keep controller within 5 meters of Pi
- **Power management:** Disable Pi's Bluetooth power saving:
  ```bash
  sudo nano /etc/bluetooth/main.conf
  ```
  Add or change:
  ```
  [Policy]
  AutoEnable=true
  ```
  Restart Bluetooth:
  ```bash
  sudo systemctl restart bluetooth
  ```

---

### "Device not available" Error After Reboot

**Symptoms:** Controller was working, but after reboot the script fails

**Solutions:**
1. **Turn controller on first:** Press Xbox button before running script
2. **Wait for connection:** Wait 5-10 seconds for auto-connect
3. **Manually connect:**
   ```bash
   echo "connect XX:XX:XX:XX:XX:XX" | bluetoothctl
   ```

---

## 📝 Quick Command Reference

```bash
# Enter Bluetooth control
bluetoothctl

# Inside bluetoothctl:
power on                      # Enable Bluetooth
discoverable on              # Make Pi discoverable
agent on                     # Enable pairing agent
default-agent               # Set default agent
scan on                     # Scan for devices
scan off                    # Stop scanning
pair XX:XX:XX:XX:XX:XX      # Pair with device
trust XX:XX:XX:XX:XX:XX     # Trust device (auto-connect)
connect XX:XX:XX:XX:XX:XX   # Connect to device
disconnect XX:XX:XX:XX:XX:XX # Disconnect device
remove XX:XX:XX:XX:XX:XX    # Remove pairing
devices                     # List paired devices
exit                        # Exit bluetoothctl

# Outside bluetoothctl:
sudo systemctl status bluetooth    # Check Bluetooth status
sudo systemctl restart bluetooth   # Restart Bluetooth
ls /dev/input/                    # List input devices
cat /proc/bus/input/devices       # Detailed device info
```

---

## 🚀 Using USB vs Bluetooth

### USB Mode (Current Default)
- **Pros:** Plug and play, no setup, no batteries needed
- **Cons:** Wired, limits robot movement range

### Bluetooth Mode (This Guide)
- **Pros:** Wireless freedom, no cables, ~10m range
- **Cons:** Needs pairing, requires batteries, slight input latency

**Recommendation:** Start with USB for learning, switch to Bluetooth when you're comfortable.

---

## 🔗 Additional Resources

- **Raspberry Pi Bluetooth Guide:** https://www.raspberrypi.com/documentation/computers/configuration.html#using-bluetooth
- **Xbox Controller Support:** https://support.xbox.com/help/hardware-network/controller/connect-xbox-wireless-controller-to-pc
- **BlueZ Documentation:** http://www.bluez.org/
- **evdev Library:** https://python-evdev.readthedocs.io/

---

## 📊 Expected Behavior Summary

| Step | Controller LED | Bluetooth Status |
|------|---------------|-----------------|
| Off | Dark | Not connected |
| Pairing Mode | Flashing rapidly | Discoverable |
| Connected | Solid on | Connected |
| Idle/Sleeping | Slow pulse | Connected but sleeping |
| Low Battery | Flashing slowly | Connected |

---

## 💡 Pro Tips

1. **Label your controller:** Write the MAC address on a piece of tape on the controller for easy reference

2. **Create a connection script:**
   ```bash
   nano ~/connect_controller.sh
   ```
   Add:
   ```bash
   #!/bin/bash
   echo "connect B8:27:EB:12:34:56" | bluetoothctl
   echo "Controller connected!"
   ```
   Make executable:
   ```bash
   chmod +x ~/connect_controller.sh
   ```
   Run anytime:
   ```bash
   ~/connect_controller.sh
   ```

3. **Auto-connect on boot:** Add to `/etc/rc.local` (before `exit 0`):
   ```bash
   sleep 10
   echo "connect XX:XX:XX:XX:XX:XX" | bluetoothctl
   ```

4. **Multiple controllers:** You can pair multiple controllers and use one at a time. The last one to connect will be the active device.

---

## 🎓 What You Learned

- ✅ How Bluetooth pairing works
- ✅ Using `bluetoothctl` for device management
- ✅ Finding input devices in Linux
- ✅ Troubleshooting wireless connectivity
- ✅ Battery and power management

---

**Ready to drive your robot wirelessly! 🤖🎮**

*Last Updated: February 17, 2026*
*For the Easy-Robo educational robotics project*
