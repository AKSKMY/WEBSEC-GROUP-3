# ml.py: Keylogger Detection System with Critical Feature Detection

# 1. Import Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime
from imblearn.over_sampling import SMOTE

# 2. Load and Preprocess Data
def load_data(file_path):
    """Loads and preprocesses the data."""
    try:
        data = pd.read_csv(file_path)
        
        # Expected feature columns
        expected_columns = ["Encoded_Strings", "Obfuscation_Usage", "Keystroke_Hooks", "External_Requests", "Label"]

        # Ensure dataset contains required features
        if not set(expected_columns).issubset(data.columns):
            raise ValueError("Dataset missing required features!")

        # Split data into features and labels
        X = data.drop(columns=['Label'])  # Features
        y = data['Label']  # Labels
        return X, y
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

# 3. Feature Engineering & Save Scaler
def preprocess_features(X):
    """Scales features for better learning and saves scaler."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Save the scaler so it can be used during predictions
    joblib.dump(scaler, "scaler.pkl")
    print("✅ Scaler saved as scaler.pkl")

    return pd.DataFrame(X_scaled, columns=X.columns)

# 4. Apply SMOTE to balance keylogger samples
def balance_dataset(X, y):
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    return X_resampled, y_resampled

# 5. Train Model
def train_model(X, y):
    """Trains a Random Forest model with critical feature detection."""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    model = RandomForestClassifier(random_state=42, class_weight={0: 1, 1: 2}, n_estimators=100)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Evaluation
    print("\n� Model Evaluation:")
    print(classification_report(y_test, y_pred))
    print("\n� Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Print feature importances
    print("\n� Feature Importances:")
    feature_importances = pd.Series(model.feature_importances_, index=X.columns)
    print(feature_importances.sort_values(ascending=False))

    return model

# 6. Save the Model
def save_model(model, directory="Keylogger Model"):
    """Saves the trained model with a timestamp in the specified directory."""
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%m-%d_%H%M")
    filename = f"keylogger_model_{timestamp}_obfuscation.pkl"
    filepath = os.path.join(directory, filename)

    joblib.dump(model, filepath)
    print(f"✅ Model saved as {filepath}")

# 7. Main Function
if __name__ == "__main__":
    dataset_path = "synthetic_keylogger_dataset_new.csv"

    print("� Loading data...")
    X, y = load_data(dataset_path)

    if X is not None and y is not None:
        print("⚙️ Preprocessing features...")
        X = preprocess_features(X)  # Saves scaler

        print("� Training model...")
        model = train_model(X, y)

        print("� Saving model...")
        save_model(model)
    else:
        print("❌ Failed to load data. Exiting.")
