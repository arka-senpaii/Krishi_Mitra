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
import os

# Firebase Configuration
cred = credentials.Certificate("krishi-mitra-e45d0-firebase-adminsdk-fbsvc-8fc9c09035.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://krishi-mitra-e45d0-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

API_URL = "https://1e7c-35-245-69-74.ngrok-free.app/predict"

# Dropdown Options
soil_types = ['Alluvial', 'Red', 'Black', 'Loam', 'Sandy loam', 'Red laterite', 'Black cotton', 'Sandy', 'Laterite',
              'Teelah', 'Clay', 'Clay loam', 'Arid and Desert', 'Loamy sand', 'River basins', 'Light sandy',
              'Heavy clay', 'Dry sandy', 'Heavy cotton', 'Sandy clay loam', 'Well drained', 'Drained loam',
              'Gravelly sand', 'Medium textured clay', 'Medium textured']
seasons = ['Kharif', 'Rabi', 'Zaid']
irrigation_methods = ['Drip', 'Basin', 'Spray']
languages = {
    'English': 'en',
    'Hindi': 'hi',
    'Bengali': 'bn',
    'Marathi': 'mr',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Gujarati': 'gu',
    'Kannada': 'kn',
    'Malayalam': 'ml'
}


# Enhanced Color scheme
COLORS = {
    "primary": "#1B5E20",       # Darker Green
    "secondary": "#43A047",     # Medium Green
    "accent": "#66BB6A",        # Light Green
    "background": "#F9FBF7",    # Very Light Green with slight texture
    "text": "#212121",          # Almost Black
    "text_light": "#FFFFFF",    # White
    "highlight": "#FF6D00",     # Vibrant Orange
    "card_bg": "#FFFFFF",       # Pure White for cards
    "card_shadow": "#E0E0E0",   # Light Gray for shadows
    "chart_colors": ["#43A047", "#FF6D00", "#1E88E5", "#FFC107", "#9C27B0"]  # Green, Orange, Blue, Yellow, Purple
}

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
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    time_label.config(text=f"Time: {current_time}")
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

            # Update sensor indicators with colors and tooltips
            if temp != "N/A":
                temp_value = float(temp)
                if temp_value > 30:
                    temp_indicator.config(bg="red")
                    temp_status.set("High")
                elif temp_value < 15:
                    temp_indicator.config(bg="blue")
                    temp_status.set("Low")
                else:
                    temp_indicator.config(bg="#4CAF50")  # Brighter green
                    temp_status.set("Normal")
            
            if humid != "N/A":
                humid_value = float(humid)
                if humid_value > 70:
                    humid_indicator.config(bg="blue")
                    humid_status.set("High")
                elif humid_value < 30:
                    humid_indicator.config(bg="orange")
                    humid_status.set("Low")
                else:
                    humid_indicator.config(bg="#4CAF50")  # Brighter green
                    humid_status.set("Normal")

            current_time = time.strftime('%H:%M:%S')
            if temp != "N/A" and humid != "N/A":
                time_series.append(current_time)
                temp_series.append(float(temp))
                humid_series.append(float(humid))
                update_realtime_graph()
        else:
            temperature.set("N/A")
            humidity.set("N/A")
            temp_status.set("--")
            humid_status.set("--")

    except Exception as e:
        messagebox.showerror("Sensor Error", f"Failed to fetch data: {e}")

    root.after(5000, fetch_sensor_data)

def update_realtime_graph():
    try:
        fig, ax = plt.subplots(figsize=(8, 4))  # Increased width for better visibility
        
        # Set style for the plot
        plt.style.use('ggplot')
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor("#F8F9FA")
        
        # Plot data with improved styling
        if len(time_series) > 1:  # Only plot if we have at least 2 data points
            ax.plot(list(range(len(time_series))), list(temp_series), label="Temperature (°C)", 
                    color="#FF5722", marker='o', linewidth=2, markersize=4)
            ax.plot(list(range(len(time_series))), list(humid_series), label="Humidity (%)", 
                    color="#2196F3", marker='s', linewidth=2, markersize=4)
            
            # Customize plot
            ax.set_title("Real-time Temperature & Humidity", fontsize=12, fontweight='bold')
            ax.set_xlabel("Time", fontsize=10)
            ax.set_ylabel("Value", fontsize=10)
            
            # Show only a few x-tick labels to avoid overcrowding
            if len(time_series) > 5:
                indices = list(range(0, len(time_series), max(1, len(time_series) // 5)))
                plt.xticks(indices, [list(time_series)[i] for i in indices], rotation=45)
            else:
                plt.xticks(range(len(time_series)), list(time_series), rotation=45)
            
            ax.legend(frameon=True, fancybox=True, shadow=True, loc='upper right')
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Add some padding
            plt.subplots_adjust(bottom=0.2)
        else:
            ax.text(0.5, 0.5, "Collecting data...", 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes, fontsize=12)
        
        plt.tight_layout()

        for widget in realtime_graph_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=realtime_graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    except Exception as e:
        print(f"Error updating real-time graph: {e}")

def plot_top_3(top_3):
    try:
        crops, probabilities = zip(*top_3)
        
        fig, ax = plt.subplots(figsize=(6, 3))
        plt.style.use('ggplot')
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor("#F8F9FA")
        
        # Create horizontal bars instead of vertical for better readability
        y_pos = range(len(crops))
        bars = ax.barh(y_pos, probabilities, color=COLORS["chart_colors"][:len(crops)])
        
        # Add percentage labels inside or next to bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                    f'{width:.1f}%', va='center', fontweight='bold')
        
        # Set labels and title
        ax.set_yticks(y_pos)
        ax.set_yticklabels(crops)
        ax.set_xlabel("Probability (%)", fontsize=10)
        ax.set_title("Top Crop Recommendations", fontsize=12, fontweight='bold')
        
        # Remove spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()

        # Clear previous contents
        for widget in graph_frame.winfo_children():
            widget.destroy()

        # Create and pack the canvas
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    except Exception as e:
        print(f"Error plotting top 3: {e}")

def predict_crop():
    try:
        if any(widget.get() in ["Select Soil Type", "Select Irrigation Method", "Select Season"] 
               for widget in [soil_type, irrigation_type, season]):
            messagebox.showwarning("Input Error", "Please select all parameters")
            return

        # Show loading indication
        result_label.config(text="Processing... Please wait", fg=COLORS["highlight"])
        root.update()

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

        # Format with emojis for better visual appeal
        result_text = f"🌾 Predicted Crop: {predicted_crop}\n"
        result_text += f"✓ Confidence: {confidence:.2f}%\n\n"
        result_text += "Top 3 Recommendations:\n"
        
        # Add medal emojis for top 3
        medals = ["🥇", "🥈", "🥉"]
        result_text += "\n".join([f"{medals[i]} {crop}: {prob:.2f}%" for i, (crop, prob) in enumerate(top_3)])

        translated_result = translate_text(result_text, lang_code)

        result_label.config(
            text=translated_result,
            font=("Arial", 12, "bold"),
            fg=COLORS["primary"]
        )

        # Show crop icon if available (placeholder)
        show_crop_icon(predicted_crop)
        
        # Update the graph
        plot_top_3(top_3)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"Failed to connect: {e}")
    except ValueError:
        messagebox.showerror("API Error", "Invalid JSON response")
    except Exception as e:
        messagebox.showerror("Error", f"Prediction Failed: {e}")

def show_crop_icon(crop_name):
    # This function would ideally show an icon for the predicted crop
    # For now, we'll just update the label
    crop_icon_label.config(text="🌱")  # Default plant icon

def create_tooltip(widget, text):
    def enter(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        
        # Create a toplevel window
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tooltip, text=text, justify='left',
                         background=COLORS["primary"], relief='solid', borderwidth=1,
                         font=("Arial", "10", "normal"), fg=COLORS["text_light"])
        label.pack(ipadx=5, ipady=3)
        
        widget.tooltip = tooltip
        
    def leave(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

def create_styled_ttk():
    # Create a custom style for ttk widgets
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure TCombobox style
    style.configure('TCombobox', 
                    background=COLORS["background"],
                    fieldbackground=COLORS["text_light"],
                    foreground=COLORS["text"],
                    arrowcolor=COLORS["primary"])
    
    # Configure TLabel style
    style.configure('TLabel', 
                    background=COLORS["card_bg"],
                    foreground=COLORS["text"],
                    font=('Arial', 11))
    
    # Configure TButton style
    style.configure('TButton', 
                    background=COLORS["primary"],
                    foreground=COLORS["text_light"],
                    font=('Arial', 11, 'bold'))
    
    style.map('TButton',
              background=[('active', COLORS["secondary"])],
              foreground=[('active', COLORS["text_light"])])
    
    # Create a frame style
    style.configure('Card.TFrame', 
                    background=COLORS["card_bg"],
                    relief='raised',
                    borderwidth=2)
    
    return style

# GUI Setup
root = tk.Tk()
root.title("कृषि मित्र - Smart Farming Assistant")
root.geometry("1200x750")  # Wider window for better layout
root.configure(bg=COLORS["background"])

# Configure custom styles
create_styled_ttk()

# Create a container frame
main_container = tk.Frame(root, bg=COLORS["background"], padx=15, pady=15)
main_container.pack(fill='both', expand=True)

# Create a header frame with gradient effect
header_frame = tk.Frame(main_container, bg=COLORS["primary"], padx=10, pady=8)
header_frame.pack(fill='x', pady=(0, 10))

# Load and show logo
try:
    logo_image = Image.open("logo.png")
    logo_image = logo_image.resize((60, 60))  # Slightly smaller logo
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(header_frame, image=logo_photo, bg=COLORS["primary"])
    logo_label.image = logo_photo
    logo_label.pack(side='left', padx=(5, 15))
except Exception as e:
    print(f"Logo loading error: {e}")
    # Fallback text logo
    logo_label = tk.Label(header_frame, text="KM", font=("Arial", 20, "bold"), 
                         bg=COLORS["primary"], fg=COLORS["text_light"],
                         width=2, height=1, relief=tk.RAISED)
    logo_label.pack(side='left', padx=(5, 15))

# Header with title and subtitle
title_frame = tk.Frame(header_frame, bg=COLORS["primary"])
title_frame.pack(side='left')

header_label = tk.Label(title_frame, text="कृषि मित्र", 
                        font=("Arial", 22, "bold"), 
                        bg=COLORS["primary"], 
                        fg=COLORS["text_light"])
header_label.pack(anchor='w')

subtitle_label = tk.Label(title_frame, text="Smart Farming Assistant", 
                          font=("Arial", 12), 
                          bg=COLORS["primary"], 
                          fg=COLORS["text_light"])
subtitle_label.pack(anchor='w')

# Time display
time_frame = tk.Frame(header_frame, bg=COLORS["primary"])
time_frame.pack(side='right', padx=10)

time_label = tk.Label(time_frame, text="Time: ", 
                      font=("Arial", 11), 
                      bg=COLORS["primary"], 
                      fg=COLORS["text_light"])
time_label.pack()

# Create card-like frames with shadows and rounded corners (simulated)
def create_card(parent, title):
    # Shadow effect frame
    outer_frame = tk.Frame(parent, bg=COLORS["card_shadow"], bd=1)
    outer_frame.pack(fill='x', pady=8, padx=5)
    
    # Main card frame with title
    inner_frame = tk.LabelFrame(outer_frame, text=title, 
                               font=("Arial", 12, "bold"), 
                               bg=COLORS["card_bg"],
                               fg=COLORS["primary"],
                               bd=2, relief=tk.GROOVE)
    inner_frame.pack(fill='x', padx=1, pady=1, ipady=5)
    
    return inner_frame

# Define variables
temperature = tk.StringVar()
humidity = tk.StringVar()
temp_status = tk.StringVar(value="--")
humid_status = tk.StringVar(value="--")
soil_type = tk.StringVar(value="Select Soil Type")
irrigation_type = tk.StringVar(value="Select Irrigation Method")
season = tk.StringVar(value="Select Season")
language = tk.StringVar(value="English")

# Top section with sensor and parameters in a horizontal layout
top_section = tk.Frame(main_container, bg=COLORS["background"])
top_section.pack(fill='x', pady=5)

# Sensor Frame - left side
sensor_frame_outer = tk.Frame(top_section, bg=COLORS["background"])
sensor_frame_outer.pack(side='left', fill='x', expand=True)

sensor_card = create_card(sensor_frame_outer, "Sensor Readings")

sensor_frame = tk.Frame(sensor_card, bg=COLORS["card_bg"], padx=10, pady=5)
sensor_frame.pack(fill='x')

# Temperature frame with icon and indicator
temp_frame = tk.Frame(sensor_frame, bg=COLORS["card_bg"])
temp_frame.pack(side='left', padx=(0, 20))

temp_icon_label = tk.Label(temp_frame, text="🌡️", font=("Arial", 16), bg=COLORS["card_bg"])
temp_icon_label.pack(side='left')

temp_data_frame = tk.Frame(temp_frame, bg=COLORS["card_bg"])
temp_data_frame.pack(side='left')

temp_label = tk.Label(temp_data_frame, text="Temperature:", font=("Arial", 10), bg=COLORS["card_bg"])
temp_label.pack(anchor='w')

temp_value_frame = tk.Frame(temp_data_frame, bg=COLORS["card_bg"])
temp_value_frame.pack(fill='x')

temp_entry = tk.Entry(temp_value_frame, textvariable=temperature, font=("Arial", 11, "bold"), 
                      state="readonly", width=6, readonlybackground=COLORS["card_bg"])
temp_entry.pack(side='left')

temp_unit = tk.Label(temp_value_frame, text="°C", font=("Arial", 10), bg=COLORS["card_bg"])
temp_unit.pack(side='left')

# Add status indicator with text
temp_status_frame = tk.Frame(temp_frame, bg=COLORS["card_bg"])
temp_status_frame.pack(side='left', padx=5)

temp_indicator = tk.Frame(temp_status_frame, width=12, height=12, bg="gray", bd=1, relief=tk.SUNKEN)
temp_indicator.pack(side='left', padx=5)

temp_status_label = tk.Label(temp_status_frame, textvariable=temp_status, 
                           font=("Arial", 9), bg=COLORS["card_bg"], width=6)
temp_status_label.pack(side='left')

create_tooltip(temp_indicator, "Green: Normal (15-30°C)\nBlue: Cold (<15°C)\nRed: Hot (>30°C)")

# Humidity frame with icon and indicator
humid_frame = tk.Frame(sensor_frame, bg=COLORS["card_bg"])
humid_frame.pack(side='left')

humid_icon_label = tk.Label(humid_frame, text="💧", font=("Arial", 16), bg=COLORS["card_bg"])
humid_icon_label.pack(side='left')

humid_data_frame = tk.Frame(humid_frame, bg=COLORS["card_bg"])
humid_data_frame.pack(side='left')

humid_label = tk.Label(humid_data_frame, text="Humidity:", font=("Arial", 10), bg=COLORS["card_bg"])
humid_label.pack(anchor='w')

humid_value_frame = tk.Frame(humid_data_frame, bg=COLORS["card_bg"])
humid_value_frame.pack(fill='x')

humid_entry = tk.Entry(humid_value_frame, textvariable=humidity, font=("Arial", 11, "bold"), 
                       state="readonly", width=6, readonlybackground=COLORS["card_bg"])
humid_entry.pack(side='left')

humid_unit = tk.Label(humid_value_frame, text="%", font=("Arial", 10), bg=COLORS["card_bg"])
humid_unit.pack(side='left')

# Add status indicator with text
humid_status_frame = tk.Frame(humid_frame, bg=COLORS["card_bg"])
humid_status_frame.pack(side='left', padx=5)

humid_indicator = tk.Frame(humid_status_frame, width=12, height=12, bg="gray", bd=1, relief=tk.SUNKEN)
humid_indicator.pack(side='left', padx=5)

humid_status_label = tk.Label(humid_status_frame, textvariable=humid_status,
                            font=("Arial", 9), bg=COLORS["card_bg"], width=6)
humid_status_label.pack(side='left')

create_tooltip(humid_indicator, "Green: Normal (30-70%)\nBlue: Humid (>70%)\nOrange: Dry (<30%)")

# Parameters Frame - right side, in one line
params_frame_outer = tk.Frame(top_section, bg=COLORS["background"])
params_frame_outer.pack(side='right', fill='x', expand=True)

params_card = create_card(params_frame_outer, "Farm Parameters")

# All parameters in a single row
selection_frame = tk.Frame(params_card, bg=COLORS["card_bg"], padx=10, pady=5)
selection_frame.pack(fill='x')

# Function to create compact parameter selectors for one line
def create_compact_selector(parent, column, label_text, variable, values, icon):
    frame = tk.Frame(parent, bg=COLORS["card_bg"], padx=5)
    frame.grid(row=0, column=column, sticky='ns')
    
    # Icon and label in the same row
    label_frame = tk.Frame(frame, bg=COLORS["card_bg"])
    label_frame.pack(anchor='w')
    
    icon_label = tk.Label(label_frame, text=icon, font=("Arial", 14), bg=COLORS["card_bg"])
    icon_label.pack(side='left', padx=(0, 3))
    
    ttk.Label(label_frame, text=label_text).pack(side='left')
    
    combo = ttk.Combobox(frame, textvariable=variable, values=values, state="readonly", width=15)
    combo.pack(pady=(2, 0), fill='x')
    
    return combo

# Parameter selectors with icons - all in one row
soil_combo = create_compact_selector(selection_frame, 0, "Soil Type", soil_type, soil_types, "🌱")
irrigation_combo = create_compact_selector(selection_frame, 1, "Irrigation", irrigation_type, irrigation_methods, "💦")
season_combo = create_compact_selector(selection_frame, 2, "Season", season, seasons, "🍂")
lang_combo = create_compact_selector(selection_frame, 3, "Language", language, list(languages.keys()), "🔤")

# Button below parameters
button_frame = tk.Frame(params_card, bg=COLORS["card_bg"], pady=5)
button_frame.pack(fill='x')

predict_button = tk.Button(
    button_frame, 
    text="🔍 Predict Best Crop", 
    font=("Arial", 11, "bold"), 
    bg=COLORS["primary"], 
    fg=COLORS["text_light"], 
    activebackground=COLORS["secondary"],
    activeforeground=COLORS["text_light"],
    command=predict_crop,
    padx=15,
    pady=5,
    relief=tk.RAISED,
    bd=2,
    cursor="hand2"
)
predict_button.pack(side='right', padx=10)

# Middle section - Real-time Graph (given more space)
realtime_section = tk.Frame(main_container, bg=COLORS["background"])
realtime_section.pack(fill='both', expand=True, pady=5)

sensor_graph_card = create_card(realtime_section, "Real-time Sensor Data")
realtime_graph_frame = tk.Frame(sensor_graph_card, bg=COLORS["card_bg"], bd=1, height=250)  # Fixed height
realtime_graph_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Bottom section - Results and Crop Graph
results_section = tk.Frame(main_container, bg=COLORS["background"])
results_section.pack(fill='both', expand=True, pady=5)

# Left side: Result Card (1/3 width)
result_column = tk.Frame(results_section, bg=COLORS["background"], width=400)
result_column.pack(side='left', fill='both', expand=True, padx=(0, 5))
result_column.pack_propagate(False)  # Maintain fixed width

result_card = create_card(result_column, "Prediction Results")

# Result content with improved layout
result_content = tk.Frame(result_card, bg=COLORS["card_bg"], pady=5)
result_content.pack(fill='both', expand=True)

# Add crop icon placeholder
crop_icon_frame = tk.Frame(result_content, bg=COLORS["card_bg"])
crop_icon_frame.pack(anchor='center', pady=(5, 5))

crop_icon_label = tk.Label(
    crop_icon_frame,
    text="🌾",
    font=("Arial", 32),
    bg=COLORS["card_bg"],
    fg=COLORS["primary"]
)
crop_icon_label.pack()

result_label = tk.Label(
    result_content, 
    text="Your prediction results will appear here", 
    font=("Arial", 11), 
    bg=COLORS["card_bg"],
    fg=COLORS["text"],
    justify=tk.LEFT,
    padx=10,
    pady=5,
    wraplength=300  # Allow text wrapping for better display
)
result_label.pack(fill='both', expand=True)

# Right side: Top Crops Graph
graph_column = tk.Frame(results_section, bg=COLORS["background"])
graph_column.pack(side='right', fill='both', expand=True, padx=(5, 0))

crop_card = create_card(graph_column, "Top Crop Recommendations")
graph_frame = tk.Frame(crop_card, bg=COLORS["card_bg"], bd=1)
graph_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Footer with improved design
footer_frame = tk.Frame(main_container, bg=COLORS["primary"], padx=8, pady=6)
footer_frame.pack(fill='x', side='bottom', pady=(10, 0))

footer_text = tk.Label(
    footer_frame, 
    text="© 2025 कृषि मित्र - Smart agricultural solutions for Indian farmers", 
    font=("Arial", 9), 
    bg=COLORS["primary"],
    fg=COLORS["text_light"]
)
footer_text.pack()

# Start real-time updates
update_time()
fetch_sensor_data()

# Add placeholder messages in graph frames with icons
placeholder_msg = tk.Label(realtime_graph_frame, 
                         text="📊 Sensor data will appear here...", 
                         bg=COLORS["card_bg"], 
                         fg=COLORS["primary"],
                         font=("Arial", 12))
placeholder_msg.pack(pady=50)

placeholder_msg2 = tk.Label(graph_frame, 
                          text="🌾 Prediction chart will appear here...", 
                          bg=COLORS["card_bg"], 
                          fg=COLORS["primary"],
                          font=("Arial", 12))
placeholder_msg2.pack(pady=50)

# Set minimum window size to ensure graphs are visible
root.minsize(900, 650)

# Window size adjustment for different display modes
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))
    
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

root.mainloop()
