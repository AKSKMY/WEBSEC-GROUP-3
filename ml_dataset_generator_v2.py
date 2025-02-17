import pandas as pd
import numpy as np

def generate_synthetic_data(num_samples=10000, false_positive_rate=0.075):
    np.random.seed(42)

    # Number of samples per class
    num_keylogger = int(num_samples * 0.5)
    num_benign = num_samples - num_keylogger

    # Generate benign data with low values for keylogger-specific features
    benign_data = {
        "Encoded_Strings": np.random.normal(0.2, 0.1, num_benign),
        "Obfuscation_Usage": np.random.normal(0.1, 0.05, num_benign),
        "Keystroke_Hooks": np.random.normal(0.1, 0.05, num_benign),
        "External_Requests": np.random.normal(0.2, 0.1, num_benign),
        "Label": 0
    }

    # Generate keylogger data with higher values for keylogger-specific features
    keylogger_data = {
        "Encoded_Strings": np.random.normal(5, 2, num_keylogger),
        "Obfuscation_Usage": np.random.normal(4, 1, num_keylogger),
        "Keystroke_Hooks": np.random.normal(10, 3, num_keylogger),
        "External_Requests": np.random.normal(3, 1, num_keylogger),
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

# Generate and save the synthetic dataset
dataset = generate_synthetic_data()
dataset.to_csv("synthetic_keylogger_dataset_new.csv", index=False)
print("Synthetic dataset generated and saved as 'synthetic_keylogger_dataset.csv'")
