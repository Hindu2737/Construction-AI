from pathlib import Path
import pandas as pd

input_path = Path("datasets/weather/weatherHistory_cleaned.csv")
output_path = Path("datasets/weather/weather_processed.csv")

df = pd.read_csv(input_path)

# Turn the timestamp into useful numerical features.
df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
df["Hour"] = df["Timestamp"].dt.hour
df["Month"] = df["Timestamp"].dt.month
df["Day_Of_Week"] = df["Timestamp"].dt.dayofweek

# Do not use the original timestamp or the daily text summary.
df = df.drop(columns=["Timestamp", "Daily Summary"])

print("Missing values:")
print(df.isnull().sum())

output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print(f"\nSaved: {output_path}")