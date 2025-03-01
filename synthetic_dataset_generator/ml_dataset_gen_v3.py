import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_samples=10000, false_positive_rate=0.075):
    np.random.seed(42)

    # Number of samples per class
    num_keylogger = int(num_samples * 0.5)
    num_benign = num_samples - num_keylogger

    # Generate benign data with low values for keylogger-specific features
    benign_data = {
        "Event_Listeners": np.random.normal(0.2, 0.1, num_benign),
        "Key_Code_Conversion": np.random.normal(0.1, 0.05, num_benign),
        "Data_Accumulation": np.random.normal(0.2, 0.1, num_benign),
        "Data_Transmission": np.random.normal(0.3, 0.1, num_benign),
        "Special_Key_Handling": np.random.normal(0.1, 0.05, num_benign),
        "Cross_Domain_Requests": np.random.normal(0.2, 0.1, num_benign),
        "Error_Handling": np.random.normal(0.1, 0.05, num_benign),
        "Label": 0
    }

    # Generate keylogger data with higher values for keylogger-specific features
    keylogger_data = {
        "Event_Listeners": np.random.normal(6, 2, num_keylogger),
        "Key_Code_Conversion": np.random.normal(4, 1, num_keylogger),
        "Data_Accumulation": np.random.normal(5, 2, num_keylogger),
        "Data_Transmission": np.random.normal(6, 2, num_keylogger),
        "Special_Key_Handling": np.random.normal(3, 1, num_keylogger),
        "Cross_Domain_Requests": np.random.normal(5, 1.5, num_keylogger),
        "Error_Handling": np.random.normal(2, 1, num_keylogger),
        "Label": 1
    }

    # Combine data into a DataFrame and shuffle
    benign_df = pd.DataFrame(benign_data)
    keylogger_df = pd.DataFrame(keylogger_data)
    dataset = pd.concat([benign_df, keylogger_df]).sample(frac=1).reset_index(drop=True)

    # Introduce false positives by modifying a percentage of benign samples to label as keylogger (1)
    num_false_positives = int(num_benign * false_positive_rate)
    false_positive_indices = dataset[dataset['Label'] == 0].sample(n=num_false_positives, random_state=42).index
    dataset.loc[false_positive_indices, 'Label'] = 1

    return dataset

# Ensure "Synthetic_Dataset" directory exists
output_dir = "Synthetic_Dataset"
os.makedirs(output_dir, exist_ok=True)

# Generate and save the synthetic dataset
dataset = generate_synthetic_data()
file_path = os.path.join(output_dir, "synthetic_keylogger_dataset_v3.csv")
dataset.to_csv(file_path, index=False)

print(f"✅ Synthetic dataset generated and saved at '{file_path}'")