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
git clone https://github.com/arka-senpaii/Krishi_Mirtra
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
**Endpoint:** `https://9f21-34-28-95-124.ngrok-free.app/predict`  
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

## Project Images
![Krishi Mitra GUI](https://github.com/user-attachments/assets/b791ed32-5f3d-43cf-95dd-25f97eed3c8c)

## ML Training
![Training Image 1](https://github.com/user-attachments/assets/7e50597d-9008-4c22-97fe-16625205ff89)
![Training Image 2](https://github.com/user-attachments/assets/5add8f31-13d1-41d6-8558-8866effa4ad2)
![Training Image 3](https://github.com/user-attachments/assets/d7899f05-eb08-4677-862a-d390e499e164)
![Training Image 4](https://github.com/user-attachments/assets/ce70e1a7-6d37-487a-9c02-18d684d4e2fc)

## Project Image
![WhatsApp Image 2025-03-08 at 16 29 14_c6d2534c](https://github.com/user-attachments/assets/b791ed32-5f3d-43cf-95dd-25f97eed3c8c)
## ML Training 
![download (5)](https://github.com/user-attachments/assets/f6447acb-6dfc-4060-8f69-0f3592362b1e)
![download (6)](https://github.com/user-attachments/assets/1bec8303-3f20-479e-99e1-5773db65218c)
![download (7)](https://github.com/user-attachments/assets/e07e6195-a836-40f3-b1d7-34197526d2d4)
![download (8)](https://github.com/user-attachments/assets/579533ca-9d9d-45dd-a359-7b0d2a2a44a8)
![download (9)](https://github.com/user-attachments/assets/1771c055-8145-46b7-a40c-cca18c2306fd)
![download (10)](https://github.com/user-attachments/assets/3b9b12a5-2e96-4a94-a08c-78d84df57217)
![download (11)](https://github.com/user-attachments/assets/080c805c-1cf6-40ef-8cfc-b2322461a412)

