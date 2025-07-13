// Firebase configuration and data handling
// This file manages Firebase Realtime Database connections and data retrieval

// Import Firebase modules
import { initializeApp } from 'firebase/app';
import { getDatabase, ref, onValue, off } from 'firebase/database';

// Firebase configuration object
const firebaseConfig = {
    apiKey: "AIzaSyCTYrddSfIkL3r8MYx5OYF5mVnHEQacm8s",
    authDomain: "krishi-mitra-e45d0.firebaseapp.com",
    databaseURL: "https://krishi-mitra-e45d0-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "krishi-mitra-e45d0",
    storageBucket: "krishi-mitra-e45d0.firebasestorage.app",
    messagingSenderId: "285192945015",
    appId: "1:285192945015:web:9b3b17a692d243c580b572"
};

// Initialize Firebase app
let app = null;
let database = null;
let isFirebaseConnected = false;

try {
    app = initializeApp(firebaseConfig);
    database = getDatabase(app);
    isFirebaseConnected = true;
    console.log('Firebase initialized successfully');
} catch (error) {
    console.warn('Firebase initialization failed:', error.message);
    console.log('Using mock data instead');
}

// Mock data for demonstration when Firebase is not configured
const mockData = {
    temperature: 28.5,
    humidity: 65,
    soilMoisture: 45,
    rainfall: 0,
    lastUpdated: new Date().toISOString()
};

// Function to generate realistic mock sensor data
function generateMockData() {
    return {
        temperature: (20 + Math.random() * 15).toFixed(1), // 20-35°C
        humidity: (40 + Math.random() * 40).toFixed(0),    // 40-80%
        soilMoisture: (30 + Math.random() * 50).toFixed(0), // 30-80%
        rainfall: Math.random() > 0.8 ? (Math.random() * 10).toFixed(1) : 0, // Occasional rain
        lastUpdated: new Date().toISOString()
    };
}

// Class to handle sensor data operations
class SensorDataManager {
    constructor() {
        this.listeners = [];
        this.currentData = mockData;
        this.dataUpdateCallback = null;
    }

    // Set callback function for data updates
    setDataUpdateCallback(callback) {
        this.dataUpdateCallback = callback;
    }

    // Start listening for data updates
    startListening() {
        if (isFirebaseConnected) {
            this.listenToFirebaseData();
        } else {
            this.startMockDataUpdates();
        }
    }

    // Listen to Firebase Realtime Database
    listenToFirebaseData() {
        try {
            const dataRef = ref(database, 'ESP32_SensorData');
            
            onValue(dataRef, (snapshot) => {
                const data = snapshot.val();
                if (data) {
                    this.currentData = {
                        temperature: data.Temperature || 0,
                        humidity: data.Humidity || 0,
                        soilMoisture: data.soilMoisture || 0,
                        rainfall: data.rainfall || 0,
                        lastUpdated: data.timestamp || new Date().toISOString()
                    };
                    
                    if (this.dataUpdateCallback) {
                        this.dataUpdateCallback(this.currentData);
                    }
                    
                    console.log('Firebase data received:', this.currentData);
                } else {
                    console.log('No data available in Firebase');
                    this.startMockDataUpdates();
                }
            }, (error) => {
                console.error('Firebase read failed:', error);
                this.startMockDataUpdates();
            });
            
        } catch (error) {
            console.error('Error setting up Firebase listener:', error);
            this.startMockDataUpdates();
        }
    }

    // Start mock data updates (for demo purposes)
    startMockDataUpdates() {
        // Initial data update
        if (this.dataUpdateCallback) {
            this.dataUpdateCallback(generateMockData());
        }

        // Update data every 5 seconds with new mock values
        this.mockDataInterval = setInterval(() => {
            const newData = generateMockData();
            this.currentData = newData;
            
            if (this.dataUpdateCallback) {
                this.dataUpdateCallback(newData);
            }
            
            console.log('Mock data updated:', newData);
        }, 5000);
    }

    // Stop listening for updates
    stopListening() {
        if (this.mockDataInterval) {
            clearInterval(this.mockDataInterval);
        }
        
        if (isFirebaseConnected && database) {
            const dataRef = ref(database, 'ESP32_SensorData');
            off(dataRef);
        }
    }

    // Get current sensor data
    getCurrentData() {
        return this.currentData;
    }

    // Manually trigger a data fetch (for testing)
    async fetchData() {
        if (isFirebaseConnected) {
            try {
                const dataRef = ref(database, 'ESP32_SensorData');
                return new Promise((resolve) => {
                    onValue(dataRef, (snapshot) => {
                        const data = snapshot.val();
                        resolve(data || generateMockData());
                    }, { onlyOnce: true });
                });
            } catch (error) {
                console.error('Error fetching Firebase data:', error);
                return generateMockData();
            }
        } else {
            return generateMockData();
        }
    }
}

// Export the sensor data manager instance
export const sensorManager = new SensorDataManager();

// Export utility functions
export { generateMockData, isFirebaseConnected };

// Example Firebase data structure:
/*
{
  "ESP32_SensorData": {
    "Temperature": 25,
    "Humidity": 20,
    "soilMoisture": 45,
    "rainfall": 0,
    "timestamp": "2025-01-08T10:30:00.000Z"
  }
}
*/