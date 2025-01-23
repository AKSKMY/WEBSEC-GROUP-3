# ml.py: Keylogger Detection System

# 1. Import Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os
from datetime import datetime

# 2. Load and Preprocess Data
def load_data(file_path):
    """Loads and preprocesses the data."""
    try:
        data = pd.read_csv(file_path)
        # Assuming 'Label' column contains 0 (benign) and 1 (keylogger)
        X = data.drop(columns=['Label'])  # Features
        y = data['Label']  # Labels
        return X, y
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

# 3. Feature Engineering
def preprocess_features(X):
    """Placeholder for feature engineering. Modify as needed."""
    # Normalize or scale features if necessary
    return X  # Currently passing features as-is

# 4. Train Model
def train_model(X, y):
    """Trains a Random Forest model."""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Evaluation
    print("Model Evaluation:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return model

# 5. Save the Model
def save_model(model, directory="Keylogger Model"):
    """Saves the trained model with a timestamp in the specified directory."""
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Get the current date and time
    timestamp = datetime.now().strftime("%m-%d_%H%M")
    
    # Construct the filename
    filename = f"keylogger_model_{timestamp}.pkl"
    filepath = os.path.join(directory, filename)

    # Save the model
    joblib.dump(model, filepath)
    print(f"Model saved as {filepath}")

# 6. Main Function
if __name__ == "__main__":
    # Update dataset path
    dataset_path = "synthetic_keylogger_dataset.csv"

    print("Loading data...")
    X, y = load_data(dataset_path)

    if X is not None and y is not None:
        print("Preprocessing features...")
        X = preprocess_features(X)

        print("Training model...")
        model = train_model(X, y)

        print("Saving model...")
        save_model(model, directory="Keylogger Model")
    else:
        print("Failed to load data. Exiting.")
