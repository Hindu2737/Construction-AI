class InsuranceIntelligenceAgent:
    def assess_insurance_risk(
        self,
        site_report,
        compliance_report,
        equipment_mttf,
    ):
        insurance_risk_score = site_report["site_risk_score"]

        # Non-compliance increases the likelihood of safety claims.
        if compliance_report["compliance_status"] == "Non-Compliant":
            insurance_risk_score += 25
        elif compliance_report["compliance_status"] == "Partially Compliant":
            insurance_risk_score += 10

        # Equipment likely to fail soon increases operational risk.
        if equipment_mttf < 100:
            insurance_risk_score += 15
        elif equipment_mttf < 300:
            insurance_risk_score += 5

        insurance_risk_score = min(insurance_risk_score, 100)

        if insurance_risk_score >= 70:
            insurance_risk_level = "High"
            recommendation = (
                "Immediate risk review is recommended. Resolve compliance "
                "findings and schedule equipment maintenance."
            )
        elif insurance_risk_score >= 40:
            insurance_risk_level = "Medium"
            recommendation = (
                "Monitor the site closely and resolve outstanding safety "
                "or maintenance issues."
            )
        else:
            insurance_risk_level = "Low"
            recommendation = (
                "Maintain current controls and continue regular inspections."
            )

        return {
            "insurance_risk_level": insurance_risk_level,
            "insurance_risk_score": insurance_risk_score,
            "recommendation": recommendation,
            "note": (
                "This is an internal risk-support indicator, not an "
                "insurance quote, policy decision, or legal determination."
            ),
        }