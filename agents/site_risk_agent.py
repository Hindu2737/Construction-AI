class SiteRiskAgent:
    BAD_WEATHER = {
        "Rain",
        "Light Rain",
        "Heavy Rain",
        "Windy",
        "Overcast",
    }

    def assess_site(self, project_risk, equipment_mttf, weather, safety_report):
        score = 0
        hazards = []
        actions = []

        # Project-model result
        if project_risk == "High":
            score += 40
            hazards.append("High project risk predicted")
            actions.append("Review cost, schedule, and structural risks.")
        elif project_risk == "Medium":
            score += 20

        # Equipment-model result: lower MTTF means earlier failure risk
        if equipment_mttf < 100:
            score += 30
            hazards.append("Equipment may fail soon")
            actions.append("Schedule immediate equipment inspection.")
        elif equipment_mttf < 300:
            score += 15
            hazards.append("Equipment maintenance required soon")
            actions.append("Plan preventive maintenance.")

        # Weather-model result
        if weather in self.BAD_WEATHER:
            score += 15
            hazards.append(f"Unsafe weather condition: {weather}")
            actions.append("Review outdoor-work and visibility precautions.")

        # YOLO Safety Agent result
        if safety_report["status"] == "Unsafe":
            score += 30
            hazards.extend(
                f"PPE violation: {item['label']}"
                for item in safety_report["violations"]
            )
            actions.append("Stop affected work and provide required PPE.")

        score = min(score, 100)

        if score >= 60:
            level = "High"
        elif score >= 30:
            level = "Medium"
        else:
            level = "Low"

        return {
            "site_risk_level": level,
            "site_risk_score": score,
            "hazards": hazards,
            "recommended_actions": actions,
        }