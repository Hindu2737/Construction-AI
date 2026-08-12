from pathlib import Path
import pandas as pd

input_path = Path(
    "datasets/resource/equipment_maintenance_combined_cleaned.csv"
)
output_path = Path("datasets/resource/resource_processed.csv")

df = pd.read_csv(input_path)

df = df.drop(columns=[
    "Equipment_Record_ID",
    "Source_UID",
    "Data_Split",
])

# MTTF is the value the model must learn to predict.
# Rows without it cannot be used for supervised training.
before = len(df)
df = df.dropna(subset=["MTTF"])
after = len(df)

print(f"Removed {before - after} rows with missing MTTF.")
print(f"Rows available for training: {after}")

print("\nMissing values:")
print(df.isnull().sum())

output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print(f"\nSaved: {output_path}")