import pandas as pd

df = pd.read_csv("synthetic_keylogger_dataset.csv")
print(df['Label'].value_counts())  # Count `0`s vs. `1`s
