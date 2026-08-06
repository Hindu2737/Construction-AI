import joblib
import pandas as pd


class ProjectAgent:
    def __init__(self):
        self.model = joblib.load("models/project_risk_pipeline.pkl")

    def predict_risk(self, project_data):
        project_df = pd.DataFrame([project_data])
        return self.model.predict(project_df)[0]