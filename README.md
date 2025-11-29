
# Driver Drowsiness Detection System

This project combines **Computer Vision (Python / MediaPipe)** with **Physical Hardware (Arduino)** to create a real-time system that detects driver drowsiness and triggers an alarm.

---

## Hardware & Software Requirements

### Hardware Components
- Arduino Board (e.g., Uno, Nano)
- Webcam (USB or built-in)
- OLED Display (128x64, I2C, e.g., SSD1306)
- Buzzer
- LED (with current-limiting resistor, typically 220 Ohm)
- Jumper wires, breadboard

### Software Dependencies
- Arduino IDE
- Python 3.8+ (Python 3.12 recommended for MediaPipe stability)
- Required Python Packages (listed in `requirement.txt`)

---

## Setup Guide: Step-by-Step

### Step 1: Install Arduino Libraries
1. Open the Arduino IDE.
2. Go to **Sketch → Include Library → Manage Libraries**.
3. Install:
   - Adafruit GFX Library
   - Adafruit SSD1306

---

### Step 2: Wire the Hardware

| Component | Arduino Pin | Notes |
|--------|------------|------|
| Buzzer | Digital Pin 8 | Positive (+) to Pin 8, Negative (-) to GND |
| LED | Digital Pin 9 | Connect via resistor, then to GND |
| OLED SDA | Analog Pin A4 | I2C Data |
| OLED SCL | Analog Pin A5 | I2C Clock |
| OLED VCC / GND | +5V / GND | Power supply |

**OLED Address Check**  
If the display does not light up, check:
```cpp
#define SCREEN_ADDRESS 0x3C
```
(Some OLED models use `0x3D`)

---

### Step 3: Flash the Arduino Code
1. Open the Arduino sketch in Arduino IDE.
2. Select the correct **Board** and **COM Port** under **Tools**.
3. Click **Upload**.

After upload, the OLED should display:
- `Driver Sleep Detection SYSTEM`
- `All Ok / Drive Safe`

---

### Step 4: Configure Python Environment
1. Identify Arduino COM port (e.g., `COM10`).
2. Update Python script configuration:
```python
COM_PORT = 'COM10'   # Change this
BAUDRATE = 9600
```
3. Save the Python script.

---

### Step 5: Install Python Dependencies
Ensure `requirement.txt` contains:
```
opencv-python
mediapipe
pyserial
```

Run:
```bash
python -m pip install -r requirement.txt
```

---

### Step 6: Run the Drowsiness Detector
```bash
python in.py
```

---

## System Operation

- **AWAKE State ('b')**
  - Eyes open
  - Buzzer & LED OFF
  - OLED: *All Ok / Drive Safe*

- **DROWSY State ('a')**
  - EAR below threshold for 20 consecutive frames
  - Buzzer & LED ON
  - Warning message on OLED

- **Recovered**
  - Eyes open again
  - Alarm turns OFF

**Exit Program:**  
Select the video window and press **q**.

---
