import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from google.colab import drive
drive.mount('/content/drive')

# Load dataset
file_path = "/content/drive/MyDrive/data_season.csv"  # Update with correct path if needed
df = pd.read_csv(file_path)

# Drop the 'Rainfall' column
df = df.drop(columns=['Rainfall'])

# Fill missing values in 'Soil type' with the most common value (mode)
df['Soil type'].fillna(df['Soil type'].mode()[0], inplace=True)

# Encode categorical columns
label_encoders = {}
categorical_columns = ['Soil type', 'Irrigation', 'Season', 'Crops']

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Store encoders for later use

# Define features (X) and target variable (y)
X = df[['Temperature', 'Humidity', 'Soil type', 'Irrigation', 'Season']]
y = df['Crops']

# Split data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Initial accuracy check
y_pred = rf_model.predict(X_test)
initial_accuracy = accuracy_score(y_test, y_pred)
print(f"Initial Accuracy: {initial_accuracy:.2%}")

# Hyperparameter tuning using GridSearchCV
param_grid = {
    'n_estimators': [100, 150, 200],
    'max_depth': [10, 15, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, n_jobs=-1, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Best model after tuning
best_model = grid_search.best_estimator_
best_params = grid_search.best_params_

# Final accuracy check
y_pred_best = best_model.predict(X_test)
final_accuracy = accuracy_score(y_test, y_pred_best)
print(f"Final Accuracy after tuning: {final_accuracy:.2%}")

# Save the best model and encoders
joblib.dump(best_model, "/content/drive/MyDrive/ML/crop_prediction_model.pkl")
joblib.dump(label_encoders, "/content/drive/MyDrive/ML/label_encoders.pkl")

print("Model and encoders saved successfully!")
