import joblib
import pandas as pd


class ResourceAgent:
    def __init__(self):
        self.model = joblib.load("models/resource_mttf_pipeline.pkl")

    def predict_mttf(self, equipment_data):
        df = pd.DataFrame([equipment_data])
        return self.model.predict(df)[0]