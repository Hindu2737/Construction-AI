def create_risk_summary(results):
    """
    Convert all Construction-AI agent outputs
    into one unified reporting structure.
    """

    # ========================================================
    # GET AGENT RESULTS
    # ========================================================

    project_risk = results["project_risk"]
    equipment_mttf = results["equipment_mttf"]
    weather = results["weather_prediction"]

    safety_report = results["safety_report"]

    worker_protection = results[
        "worker_protection_report"
    ]

    site_report = results[
        "site_report"
    ]

    compliance_report = results[
        "compliance_report"
    ]

    insurance_report = results[
        "insurance_report"
    ]


    # ========================================================
    # PROJECT RISK SCORE
    # ========================================================

    project_risk_text = str(
        project_risk
    ).lower()

    if project_risk_text == "high":
        project_score = 80

    elif project_risk_text == "medium":
        project_score = 50

    else:
        project_score = 20


    # ========================================================
    # SAFETY RISK SCORE
    # ========================================================
    # SafetyIntelligenceAgent gives a PROTECTION score:
    #
    # 100 = good protection
    # 0   = poor protection
    #
    # For risk reporting we reverse it:
    #
    # 0   = low risk
    # 100 = high risk
    # ========================================================

    protection_score = worker_protection[
        "safety_score"
    ]

    safety_risk_score = 100 - protection_score


    # ========================================================
    # SITE RISK SCORE
    # ========================================================

    site_score = site_report[
        "site_risk_score"
    ]


    # ========================================================
    # WEATHER RISK SCORE
    # ========================================================

    bad_weather = {
        "Rain",
        "Light Rain",
        "Heavy Rain",
        "Windy",
        "Overcast",
    }

    if weather in bad_weather:
        weather_score = 70

    else:
        weather_score = 20


    # ========================================================
    # RESOURCE RISK SCORE
    # ========================================================

    if equipment_mttf < 100:
        resource_score = 80

    elif equipment_mttf < 300:
        resource_score = 50

    else:
        resource_score = 20


    # ========================================================
    # OVERALL RISK SCORE
    # ========================================================

    overall_score = round(
        (
            project_score * 0.20
            + safety_risk_score * 0.25
            + site_score * 0.25
            + weather_score * 0.15
            + resource_score * 0.15
        )
    )


    # ========================================================
    # OVERALL RISK LEVEL
    # ========================================================

    if overall_score >= 80:
        overall_level = "Critical"

    elif overall_score >= 60:
        overall_level = "High"

    elif overall_score >= 30:
        overall_level = "Medium"

    else:
        overall_level = "Low"


    # ========================================================
    # KEY FINDINGS
    # ========================================================

    findings = []


    if project_risk_text == "high":

        findings.append(
            "High project risk predicted."
        )


    if safety_report["status"] == "Unsafe":

        findings.append(
            "PPE or worker safety violations detected."
        )


    for hazard in site_report.get(
        "hazards",
        []
    ):

        if hazard not in findings:
            findings.append(hazard)


    if compliance_report[
        "compliance_status"
    ] != "Compliant":

        findings.append(
            "Site is not fully PPE compliant."
        )


    if insurance_report[
        "insurance_risk_level"
    ] == "High":

        findings.append(
            "High operational and insurance risk identified."
        )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    recommendations = []


    # Site Risk recommendations

    recommendations.extend(
        site_report.get(
            "recommended_actions",
            []
        )
    )


    # Worker Protection recommendations

    recommendations.extend(
        worker_protection.get(
            "recommended_actions",
            []
        )
    )


    # Compliance recommendations

    recommendations.extend(
        compliance_report.get(
            "recommended_actions",
            []
        )
    )


    # Insurance recommendation

    insurance_recommendation = (
        insurance_report.get(
            "recommendation"
        )
    )

    if insurance_recommendation:

        recommendations.append(
            insurance_recommendation
        )


    # ========================================================
    # REMOVE DUPLICATE RECOMMENDATIONS
    # ========================================================

    recommendations = list(
        dict.fromkeys(
            recommendations
        )
    )


    # ========================================================
    # FINAL UNIFIED REPORT
    # ========================================================

    return {

        "overall_score":
            overall_score,

        "overall_level":
            overall_level,


        "risk_breakdown": {

            "project":
                project_score,

            "safety":
                safety_risk_score,

            "site":
                site_score,

            "weather":
                weather_score,

            "resources":
                resource_score,
        },


        "project_risk":
            project_risk,

        "equipment_mttf":
            equipment_mttf,

        "weather":
            weather,


        "safety_status":
            safety_report["status"],


        "worker_protection_level":
            worker_protection[
                "worker_protection_level"
            ],


        "compliance_status":
            compliance_report[
                "compliance_status"
            ],


        "compliance_score":
            compliance_report[
                "compliance_score"
            ],


        "insurance_risk":
            insurance_report[
                "insurance_risk_level"
            ],


        "insurance_score":
            insurance_report[
                "insurance_risk_score"
            ],


        "findings":
            findings,


        "recommendations":
            recommendations,
    }