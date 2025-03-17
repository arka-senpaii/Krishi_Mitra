from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
from pyngrok import ngrok
ngrok authtoken cr_2uO4Iw5ULRRHhtf14lYV69Bg2cr

# Load trained model and encoders
model = joblib.load("crop_prediction_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        # Convert input values
        temperature = float(data['Temperature'])
        humidity = float(data['Humidity'])
        soil_type = label_encoders['Soil type'].transform([data['Soil type']])[0]
        irrigation = label_encoders['Irrigation'].transform([data['Irrigation']])[0]
        season = label_encoders['Season'].transform([data['Season']])[0]

        input_features = np.array([[temperature, humidity, soil_type, irrigation, season]])

        # Predict
        predicted_crop_idx = model.predict(input_features)[0]
        predicted_crop = label_encoders['Crops'].inverse_transform([predicted_crop_idx])[0]

        # Get probability
        probabilities = model.predict_proba(input_features)[0] * 100
        crop_probabilities = {label_encoders['Crops'].inverse_transform([i])[0]: round(prob, 2) for i, prob in enumerate(probabilities)}

        return jsonify({
            "Predicted Crop": predicted_crop,
            "Confidence (%)": crop_probabilities[predicted_crop],
            "All Probabilities": crop_probabilities
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    # Start ngrok tunnel for Flask app
    public_url = ngrok.connect(5000).public_url
    print(f"Public URL: {public_url}")
    
    app.run(debug=True)
