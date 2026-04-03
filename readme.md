# Krishi Mitra — Raspberry Pi Edition
### Python-Based IoT Agro Car with On-Device Intelligence

---

## Overview

Krishi Mitra (Raspberry Pi Edition) is a fully self-contained precision agriculture platform built around a **Raspberry Pi 4B**. Unlike the original ESP32 build — where the Pi (or PC) acted as a secondary host receiving serial data — this edition runs **everything on the Pi itself**: sensor acquisition, GUI dashboard, ML inference calls, Firebase sync, and motor control. A 7" touchscreen directly attached to the Pi serves as the farmer's interface in the field.

---

## What Changed from the ESP32 Version

| Feature | Original (ESP32) | Raspberry Pi Edition |
|---|---|---|
| Sensor interface | ESP32 → PC via UART serial | Pi GPIO / SPI / I²C directly |
| GUI host | Separate PC | On-device (Pi + touchscreen) |
| Motor control | FS-i10B RC receiver | L298N driver via Pi GPIO PWM |
| ADC for soil sensor | Built into ESP32 | MCP3008 via SPI (Pi has no ADC) |
| Camera | None | Pi Camera Module v3 |
| Boot/auto-start | Manual | systemd service |
| Communication overhead | UART bridge required | Zero — single device |

---

## Hardware

### Core Platform
- **Raspberry Pi 4B** (4 GB RAM recommended)
- **Official 7" Raspberry Pi Touchscreen** (800×480)
- **MicroSD card** (32 GB+, Class 10)

### Sensors (connected directly to Pi GPIO)
| Sensor | Purpose | Interface |
|---|---|---|
| DHT22 | Temperature + Humidity | GPIO (single-wire) |
| Capacitive Soil Moisture Sensor v1.2 | Soil moisture % | SPI via MCP3008 |
| MCP3008 | 8-channel 10-bit ADC | SPI (SPI0, CE0) |
| Pi Camera Module v3 | Field imagery / visual monitoring | CSI ribbon cable |

### Actuation
| Component | Purpose | Interface |
|---|---|---|
| L298N Motor Driver | Drive two DC wheels | GPIO PWM (pins 12, 13, 18, 19) |
| Servo SG90 × 2 | Sensor mast pan/tilt | GPIO PWM (pins 20, 21) |
| 12 V LiPo 3S (5000 mAh) | Drive motors | L298N power input |
| Pi UPS HAT (Waveshare) | Power Pi + 5 V logic | USB-C to Pi |

### Eliminated Hardware
- ~~ESP32~~ — no longer needed
- ~~FS-i10B RC system~~ — replaced by direct GPIO motor control (optionally add a web remote or gamepad via USB)

---

## Software Architecture

```
┌─────────────────────────────────────────────┐
│             Raspberry Pi 4B                 │
│                                             │
│  ┌──────────┐    ┌────────────────────────┐ │
│  │ Sensor   │───▶│  main.py               │ │
│  │ daemon   │    │  (PyQt6 GUI)           │ │
│  │ (GPIO /  │    │  • Dashboard           │ │
│  │  SPI)    │    │  • Real-time charts    │ │
│  └──────────┘    │  • Prediction panel    │ │
│                  │  • Camera feed         │ │
│  ┌──────────┐    └────────┬───────────────┘ │
│  │ Motor    │◀────────────┘                 │
│  │ control  │    ┌────────▼───────────────┐ │
│  │ (GPIO    │    │  Firebase Realtime DB  │ │
│  │  PWM)    │    │  + ML API (HTTP POST)  │ │
│  └──────────┘    └────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### Key Libraries

| Library | Role |
|---|---|
| `PyQt6` | GUI framework (replaces Tkinter for better touchscreen UX) |
| `RPi.GPIO` / `gpiozero` | GPIO control for DHT22, motor driver, servos |
| `spidev` | SPI bus for MCP3008 ADC readings |
| `adafruit-circuitpython-dht` | DHT22 driver |
| `picamera2` | Camera Module v3 streaming |
| `firebase-admin` | Firebase Realtime Database + Auth |
| `requests` | HTTP POST to ML prediction endpoint |
| `pyqtgraph` | Real-time sensor graphs in PyQt6 |
| `evdev` (optional) | USB gamepad support for manual car control |

---

## GPIO Pin Map

```
Pi Pin   │ BCM GPIO │ Connected to
─────────┼──────────┼──────────────────────────
  3V3    │   —      │ DHT22 VCC
  GND    │   —      │ Common ground
  11     │  GPIO 17 │ DHT22 DATA
  19     │  GPIO 10 │ MCP3008 MOSI (SPI0)
  21     │  GPIO  9 │ MCP3008 MISO (SPI0)
  23     │  GPIO 11 │ MCP3008 CLK  (SPI0)
  24     │  GPIO  8 │ MCP3008 CE0  (SPI0 CS)
  32     │  GPIO 12 │ L298N ENA  (Motor A PWM)
  33     │  GPIO 13 │ L298N ENB  (Motor B PWM)
  35     │  GPIO 19 │ L298N IN1 / IN3
  36     │  GPIO 16 │ L298N IN2 / IN4
  38     │  GPIO 20 │ Servo pan (PWM)
  40     │  GPIO 21 │ Servo tilt (PWM)
```

---

## Installation

### 1. Flash Raspberry Pi OS

Use **Raspberry Pi OS Bookworm (64-bit)** with desktop. Enable SPI and Camera in `raspi-config`:

```bash
sudo raspi-config
# → Interface Options → SPI → Enable
# → Interface Options → Camera → Enable
sudo reboot
```

### 2. Clone the Repository

```bash
git clone https://github.com/arka-senpaii/Krishi_Mitra.git
cd Krishi_Mitra
git checkout raspberrypi-edition
```

### 3. Install System Dependencies

```bash
sudo apt update && sudo apt install -y \
  python3-pyqt6 python3-pyqtgraph \
  libgpiod2 python3-libgpiod \
  python3-picamera2 \
  python3-spidev
```

### 4. Install Python Dependencies

```bash
pip install --break-system-packages \
  adafruit-circuitpython-dht \
  RPi.GPIO \
  gpiozero \
  firebase-admin \
  requests \
  evdev
```

### 5. Configure Credentials

Copy the template and fill in your Firebase service account key and ML endpoint:

```bash
cp config/config.example.json config/config.json
nano config/config.json
```

```json
{
  "firebase": {
    "credential_path": "config/serviceAccountKey.json",
    "database_url": "https://your-project.firebaseio.com"
  },
  "ml_endpoint": "https://your-ml-api/predict",
  "farm_id": "farm_001"
}
```

### 6. Run the Application

```bash
python3 main.py
```

### 7. Auto-start on Boot (systemd)

```bash
sudo cp deploy/krishimitra.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable krishimitra
sudo systemctl start krishimitra
```

---

## Project Structure

```
Krishi_Mitra/
├── main.py                  # Entry point — launches PyQt6 GUI
├── config/
│   ├── config.example.json
│   └── config.json          # (gitignored — add your keys here)
├── hardware/
│   ├── sensors.py           # DHT22 + MCP3008 soil moisture reading
│   ├── motor.py             # L298N motor driver control
│   └── camera.py            # picamera2 capture + preview
├── ml/
│   └── predictor.py         # HTTP POST to ML endpoint, parse response
├── firebase/
│   └── uploader.py          # firebase-admin Realtime DB push
├── gui/
│   ├── dashboard.py         # Main PyQt6 window + sensor widgets
│   ├── prediction.py        # Crop prediction panel + probability chart
│   ├── camera_view.py       # Live camera feed widget
│   └── motor_control.py     # On-screen joystick / manual drive panel
├── deploy/
│   └── krishimitra.service  # systemd unit file
└── tests/
    ├── test_sensors.py
    └── test_motor.py
```

---

## Sensor Reading — Code Highlights

### DHT22 (Temperature + Humidity)

```python
# hardware/sensors.py
import adafruit_dht
import board

_dht = adafruit_dht.DHT22(board.D17)   # BCM GPIO 17

def read_dht():
    """Returns (temperature_c, humidity_pct) or raises RuntimeError."""
    return _dht.temperature, _dht.humidity
```

### Soil Moisture via MCP3008

```python
import spidev

_spi = spidev.SpiDev()
_spi.open(0, 0)       # SPI bus 0, CE0
_spi.max_speed_hz = 1_350_000

def read_adc(channel: int) -> int:
    """Read 10-bit value (0–1023) from MCP3008 channel 0–7."""
    assert 0 <= channel <= 7
    r = _spi.xfer2([1, (8 + channel) << 4, 0])
    return ((r[1] & 3) << 8) | r[2]

def soil_moisture_pct() -> float:
    """Convert raw ADC to moisture percentage (calibrate dry/wet values)."""
    DRY, WET = 870, 380          # calibrate for your sensor
    raw = read_adc(0)
    return max(0.0, min(100.0, (DRY - raw) / (DRY - WET) * 100))
```

### Motor Control (L298N)

```python
# hardware/motor.py
import RPi.GPIO as GPIO

ENA, IN1, IN2 = 12, 19, 16
ENB, IN3, IN4 = 13, 20, 21

GPIO.setmode(GPIO.BCM)
for pin in [ENA, ENB, IN1, IN2, IN3, IN4]:
    GPIO.setup(pin, GPIO.OUT)

pwm_a = GPIO.PWM(ENA, 1000)   # 1 kHz
pwm_b = GPIO.PWM(ENB, 1000)
pwm_a.start(0); pwm_b.start(0)

def drive(left: float, right: float):
    """left / right in range -1.0 (full reverse) to +1.0 (full forward)."""
    def _set(pwm, in_a, in_b, v):
        GPIO.output(in_a, v > 0)
        GPIO.output(in_b, v < 0)
        pwm.ChangeDutyCycle(abs(v) * 100)
    _set(pwm_a, IN1, IN2, left)
    _set(pwm_b, IN3, IN4, right)

def stop():
    drive(0, 0)
```

---

## ML Integration

The ML endpoint, model, and payload format are **identical** to the original build. The Raspberry Pi sends an HTTP POST over Wi-Fi:

```python
# ml/predictor.py
import requests, json

ENDPOINT = "https://your-ml-api/predict"

def predict(temperature, humidity, soil_type, irrigation, season):
    payload = {
        "Temperature": temperature,
        "Humidity": humidity,
        "Soil type": soil_type,
        "Irrigation": irrigation,
        "Season": season,
    }
    resp = requests.post(ENDPOINT, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()   # same response schema as original
```

### ML Response (unchanged)

```json
{
  "All Probabilities": {
    "Coconut": 39.12,
    "Paddy": 17.98,
    "Tea": 36.34,
    "Groundnut": 4.53,
    "..."
  },
  "Confidence (%)": 39.12,
  "Predicted Crop": "Coconut"
}
```

---

## Firebase Integration

```python
# firebase/uploader.py
import firebase_admin
from firebase_admin import credentials, db
import datetime, json

def init(credential_path, database_url):
    cred = credentials.Certificate(credential_path)
    firebase_admin.initialize_app(cred, {"databaseURL": database_url})

def push_reading(farm_id, sensor_data, prediction):
    ref = db.reference(f"farms/{farm_id}/readings")
    ref.push({
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "sensors": sensor_data,
        "prediction": prediction,
    })
```

Firebase schema:
```
farms/
  farm_001/
    readings/
      -NxABC123/
        timestamp: "2025-03-08T10:30:00Z"
        sensors:
          temperature: 29.4
          humidity: 68.0
          soil_moisture: 42.3
        prediction:
          crop: "Coconut"
          confidence: 39.12
```

---

## GUI Overview (PyQt6)

The PyQt6 interface runs fullscreen on the 7" touchscreen at 800×480:

- **Dashboard tab** — Live temperature, humidity, and soil moisture gauges updated every 5 s
- **Prediction tab** — Latest crop recommendation with a horizontal probability bar chart (pyqtgraph)
- **Camera tab** — Live Pi Camera v3 feed at 640×480, 15 fps
- **Drive tab** — On-screen D-pad / joystick for manual motor control; optionally maps to a USB gamepad

---

## Differences Summary

| Aspect | Original ESP32 build | Raspberry Pi build |
|---|---|---|
| Serial UART bridge | Required | Removed entirely |
| Sensor wiring | ESP32 ADC pins | Pi SPI (MCP3008) + GPIO |
| GUI framework | Tkinter / PyQt / Kivy (unspecified) | PyQt6 (specified) |
| Camera support | None | Pi Camera Module v3 via picamera2 |
| Motor control | FS-i10B RC system | L298N + GPIO PWM |
| Auto-start | Manual | systemd unit |
| Field deployment | Pi as display only | Pi as full standalone node |

---

## Future Enhancements

- **On-device ML inference** — deploy the trained model as a TFLite or ONNX file and run it locally on the Pi, removing the cloud ML dependency for offline field use
- **LoRa mesh** — add a RA-02 SX1278 LoRa module (SPI) for multi-car coordination without Wi-Fi
- **Web dashboard** — Flask/FastAPI served from the Pi so any phone on the same network can view live data
- **Multi-language UI** — Hindi, Bengali, Tamil locale files via Qt's i18n system
- **Automated irrigation relay** — add a 5 V relay module (GPIO-controlled) to trigger a solenoid valve based on soil moisture thresholds

---

## Contributors

- **Arka Mahajan** — Project Lead
- **Ishika Haldar** — Developer
- **Sayan Mukherjee** — Developer

## License

MIT License
