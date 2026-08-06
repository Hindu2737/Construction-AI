from pathlib import Path
import pandas as pd

# Original untouched dataset
input_path = Path(r"C:\Users\hindu\Downloads\bim_cost_schedule_cleaned.csv")

# New processed dataset; never overwrite the original
output_path = Path(
    "datasets/project_management/project_processed.csv"
)

df = pd.read_csv(input_path)

columns_to_drop = ["Project_ID", "Start_Date", "End_Date"]
df = df.drop(columns=columns_to_drop)

print("Missing values:")
print(df.isnull().sum())

output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print(f"\nPreprocessing complete. Saved: {output_path}")