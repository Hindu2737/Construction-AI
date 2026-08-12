from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv("datasets/weather/weather_processed.csv")

# The value the Weather Agent predicts.
X = df.drop(columns=["Summary"])
y = df["Summary"]

categorical_columns = ["Precip Type"]
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
    ("classifier", RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced",
    )),
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
)

model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predictions))
print("\nClassification report:")
print(classification_report(y_test, predictions, zero_division=0))

model_path = Path("models/weather_summary_pipeline.pkl")
model_path.parent.mkdir(exist_ok=True)
joblib.dump(model, model_path)

print(f"\nSaved model: {model_path}")