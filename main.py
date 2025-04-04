import tkinter as tk
from tkinter import ttk, messagebox
import firebase_admin
from firebase_admin import credentials, db
import requests
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from deep_translator import GoogleTranslator
from collections import deque
from PIL import Image, ImageTk

# Firebase Configuration
cred = credentials.Certificate("krishi-mitra-e45d0-firebase-adminsdk-fbsvc-8fc9c09035.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://krishi-mitra-e45d0-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

API_URL = "https://2558-35-243-205-21.ngrok-free.app/predict"

# Dropdown Options
soil_types = ['Alluvial', 'Red', 'Black', 'Loam', 'Sandy loam', 'Red laterite', 'Black cotton', 'Sandy', 'Laterite',
              'Teelah', 'Clay', 'Clay loam', 'Arid and Desert', 'Loamy sand', 'River basins', 'Light sandy',
              'Heavy clay', 'Dry sandy', 'Heavy cotton', 'Sandy clay loam', 'Well drained', 'Drained loam',
              'Gravelly sand', 'Medium textured clay', 'Medium textured']
seasons = ['Kharif', 'Rabi', 'Zaid']
irrigation_methods = ['Drip', 'Basin', 'Spray']
languages = {'English': 'en', 'Hindi': 'hi', 'Bengali': 'bn'}

# Real-time graph data storage
time_series = deque(maxlen=20)
temp_series = deque(maxlen=20)
humid_series = deque(maxlen=20)

def translate_text(text, lang):
    if lang != "en":
        try:
            return GoogleTranslator(source='auto', target=lang).translate(text)
        except:
            return text
    return text

def update_time():
    time_label.config(text=f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    root.after(1000, update_time)

def fetch_sensor_data():
    try:
        ref = db.reference("ESP32_SensorData")
        data = ref.get()

        if data:
            temp = data.get("Temperature", "N/A")
            humid = data.get("Humidity", "N/A")

            temperature.set(temp)
            humidity.set(humid)

            current_time = time.strftime('%H:%M:%S')
            if temp != "N/A" and humid != "N/A":
                time_series.append(current_time)
                temp_series.append(float(temp))
                humid_series.append(float(humid))
                update_realtime_graph()
        else:
            temperature.set("N/A")
            humidity.set("N/A")

    except Exception as e:
        messagebox.showerror("Sensor Error", f"Failed to fetch data: {e}")

    root.after(5000, fetch_sensor_data)

def update_realtime_graph():
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(time_series, temp_series, label="Temperature (°C)", color="red", marker='o')
    ax.plot(time_series, humid_series, label="Humidity (%)", color="blue", marker='o')
    ax.set_title("Real-time Temperature & Humidity")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True)

    for widget in realtime_graph_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=realtime_graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def plot_top_3(top_3):
    crops, probabilities = zip(*top_3)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(crops, probabilities, color=['#4CAF50', '#FF9800', '#2196F3'])
    ax.set_ylabel("Probability (%)")
    ax.set_title("Top 3 Crop Probabilities")

    for widget in graph_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def predict_crop():
    try:
        if any(widget.get() in ["Select Soil Type", "Select Irrigation Method", " Select Season"]
               for widget in [soil_type, irrigation_type, season]):
            messagebox.showwarning("Input Error", "Please select all parameters")
            return

        payload = {
            "Temperature": float(temperature.get()) if temperature.get() != "N/A" else 0,
            "Humidity": float(humidity.get()) if humidity.get() != "N/A" else 0,
            "Soil type": soil_type.get(),
            "Irrigation": irrigation_type.get(),
            "Season": season.get()
        }

        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        if "error" in result:
            messagebox.showerror("Prediction Error", result["error"])
            return

        predicted_crop = result['Predicted Crop']
        confidence = result['Confidence (%)']
        all_probs = result['All Probabilities']
        top_3 = sorted(all_probs.items(), key=lambda x: x[1], reverse=True)[:3]

        selected_lang = language.get()
        lang_code = languages[selected_lang]

        result_text = f"Predicted Crop: {predicted_crop}\nConfidence: {confidence:.2f}%\n\nTop 3 Probabilities:\n"
        result_text += "\n".join([f"{crop}: {prob:.2f}%" for crop, prob in top_3])

        translated_result = translate_text(result_text, lang_code)

        result_label.config(
            text=translated_result,
            font=("Arial", 12, "bold"),
            fg="#2E7D32"
        )

        plot_top_3(top_3)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"Failed to connect: {e}")
    except ValueError:
        messagebox.showerror("API Error", "Invalid JSON response")
    except Exception as e:
        messagebox.showerror("Error", f"Prediction Failed: {e}")

# GUI Setup
root = tk.Tk()
root.title("कृषि मित्र - Smart Farming Assistant")
root.geometry("800x800")
root.configure(bg="#E8F5E9")

# Load and show logo
logo_image = Image.open("logo.png")
logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=logo_photo, bg="#E8F5E9")
logo_label.image = logo_photo
logo_label.pack(pady=(10, 0))

# Header
header_label = tk.Label(root, text="Krishi Mitra - Smart Farming Assistant", font=("Arial", 20, "bold"), bg="#A5D6A7")
header_label.pack(fill='x')

time_label = tk.Label(root, text="Time: ", font=("Arial", 12), bg="#E8F5E9")
time_label.pack(pady=5)

# Sensor Frame
sensor_frame = tk.LabelFrame(root, text="Sensor Readings", font=("Arial", 12, "bold"), bg="#E8F5E9")
sensor_frame.pack(fill='x', pady=10)

temperature = tk.StringVar()
humidity = tk.StringVar()
soil_type = tk.StringVar(value="Select Soil Type")
irrigation_type = tk.StringVar(value="Select Irrigation Method")
season = tk.StringVar(value="Select Season")
language = tk.StringVar(value="English")

temp_label = tk.Label(sensor_frame, text="Temperature: ", font=("Arial", 12), bg="#E8F5E9")
temp_label.pack(side='left')
tk.Entry(sensor_frame, textvariable=temperature, font=("Arial", 12), state="readonly", width=10).pack(side='left', padx=5)

humid_label = tk.Label(sensor_frame, text="Humidity: ", font=("Arial", 12), bg="#E8F5E9")
humid_label.pack(side='left')
tk.Entry(sensor_frame, textvariable=humidity, font=("Arial", 12), state="readonly", width=10).pack(side='left', padx=5)

# Dropdowns
selection_frame = tk.Frame(root, bg="#E8F5E9")
selection_frame.pack()

for text, var, values in [("Soil Type", soil_type, soil_types), ("Irrigation", irrigation_type, irrigation_methods), ("Season", season, seasons)]:
    ttk.Label(selection_frame, text=text, font=("Arial", 12), background="#E8F5E9").pack()
    ttk.Combobox(selection_frame, textvariable=var, values=values, state="readonly").pack()

ttk.Label(selection_frame, text="Select Language:", font=("Arial", 12), background="#E8F5E9").pack()
ttk.Combobox(selection_frame, textvariable=language, values=list(languages.keys()), state="readonly").pack()

# Predict Button
tk.Button(root, text="Predict Best Crop", font=("Arial", 12), bg="#4CAF50", fg="white", command=predict_crop).pack(pady=10)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#E8F5E9")
result_label.pack(pady=10)

# Frame for Side-by-Side Graphs
graphs_frame = tk.Frame(root, bg="#E8F5E9")
graphs_frame.pack(pady=10)

# Bar Graph for Top 3 Crops
graph_frame = tk.Frame(graphs_frame, bg="#E8F5E9")
graph_frame.pack(side='left', padx=10)

# Real-time Graph Frame
realtime_graph_frame = tk.Frame(graphs_frame, bg="#E8F5E9")
realtime_graph_frame.pack(side='right', padx=10)

# Start real-time updates
update_time()
fetch_sensor_data()

root.mainloop()
