import joblib
import pandas as pd


class WeatherAgent:
    def __init__(self):
        self.model = joblib.load("models/weather_summary_pipeline.pkl")

    def predict_weather(self, weather_data):
        df = pd.DataFrame([weather_data])
        return self.model.predict(df)[0]