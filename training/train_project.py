from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Load your processed dataset
df = pd.read_csv("datasets/project_management/project_processed.csv")

# Separate input columns (X) and answer column (y)
X = df.drop(columns=["Risk_Level"])
y = df["Risk_Level"]

# Text columns that must be converted to numbers
categorical_columns = [
    "Project_Type",
    "Location",
    "Weather_Condition",
]

# All remaining columns are already numeric
numeric_columns = [
    column for column in X.columns
    if column not in categorical_columns
]

# Convert text inputs automatically during training/prediction
preprocessor = ColumnTransformer(
    transformers=[
        ("categories", OneHotEncoder(handle_unknown="ignore"), categorical_columns),
        ("numbers", "passthrough", numeric_columns),
    ]
)

# Combine preprocessing and ML model into one saved object
model = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=300,
        random_state=42
    ))
])

# Split dataset, train, and evaluate
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predictions))
print("\nClassification report:")
print(classification_report(y_test, predictions))

# Save the trained model
model_path = Path("models/project_risk_pipeline.pkl")
model_path.parent.mkdir(exist_ok=True)

joblib.dump(model, model_path)
print(f"\nModel saved successfully: {model_path}")