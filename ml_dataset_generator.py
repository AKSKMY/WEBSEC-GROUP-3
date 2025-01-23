import pandas as pd
import numpy as np

def generate_synthetic_data(num_samples=10000, false_positive_rate=0.075):
    np.random.seed(42)

    # Number of samples per class
    num_keylogger = int(num_samples * 0.5)
    num_benign = num_samples - num_keylogger

    # Generate benign data
    benign_data = {
        "Time_Interval": np.random.normal(0.15, 0.05, num_benign),
        "Key_Frequency": np.random.normal(20, 5, num_benign),
        "API_Call_Count": np.random.normal(10, 3, num_benign),
        "Memory_Usage": np.random.normal(150, 30, num_benign),
        "CPU_Usage": np.random.normal(5, 2, num_benign),
        "Label": 0
    }

    # Generate keylogger data
    keylogger_data = {
        "Time_Interval": np.random.normal(0.05, 0.02, num_keylogger),
        "Key_Frequency": np.random.normal(60, 10, num_keylogger),
        "API_Call_Count": np.random.normal(50, 10, num_keylogger),
        "Memory_Usage": np.random.normal(500, 100, num_keylogger),
        "CPU_Usage": np.random.normal(20, 5, num_keylogger),
        "Label": 1
    }

    # Combine data into a DataFrame
    benign_df = pd.DataFrame(benign_data)
    keylogger_df = pd.DataFrame(keylogger_data)
    dataset = pd.concat([benign_df, keylogger_df]).sample(frac=1).reset_index(drop=True)

    # Introduce false positives by modifying a percentage of benign samples
    num_false_positives = int(num_benign * false_positive_rate)
    false_positive_indices = dataset[dataset['Label'] == 0].sample(n=num_false_positives, random_state=42).index
    dataset.loc[false_positive_indices, 'Label'] = 1

    return dataset

# Generate and save the dataset
dataset = generate_synthetic_data()
dataset.to_csv("synthetic_keylogger_dataset.csv", index=False)
print("Synthetic dataset generated and saved as 'synthetic_keylogger_dataset.csv'")
