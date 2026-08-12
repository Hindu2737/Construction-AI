from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv("datasets/resource/resource_processed.csv")

X = df.drop(columns=["MTTF"])
y = df["MTTF"]

categorical_columns = ["ProductType"]
numeric_columns = [
    column for column in X.columns
    if column not in categorical_columns
]

preprocessor = ColumnTransformer([
    ("categories", OneHotEncoder(handle_unknown="ignore"), categorical_columns),
    ("numbers", "passthrough", numeric_columns),
])

model = Pipeline([
    ("preprocessing", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=300,
        random_state=42,
    )),
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("Mean absolute error:", mean_absolute_error(y_test, predictions))
print("R² score:", r2_score(y_test, predictions))

model_path = Path("models/resource_mttf_pipeline.pkl")
model_path.parent.mkdir(exist_ok=True)
joblib.dump(model, model_path)

print(f"\nSaved model: {model_path}")