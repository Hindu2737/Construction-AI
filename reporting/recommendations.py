# ============================================================
# CONSTRUCTAI - RECOMMENDATION ENGINE
# ============================================================


def generate_recommendations(results):
    """
    Generate prioritized recommendations from
    Construction-AI agent outputs.

    Parameters
    ----------
    results : dict
        Complete output returned by main.run_analysis()

    Returns
    -------
    list
        List of recommendation dictionaries.
    """

    recommendations = []

    # ========================================================
    # EXTRACT AGENT REPORTS
    # ========================================================

    site_report = results.get(
        "site_report",
        {}
    )

    worker_report = results.get(
        "worker_protection_report",
        {}
    )

    compliance_report = results.get(
        "compliance_report",
        {}
    )

    insurance_report = results.get(
        "insurance_report",
        {}
    )

    equipment_mttf = results.get(
        "equipment_mttf",
        0
    )

    project_risk = str(
        results.get(
            "project_risk",
            ""
        )
    ).lower()

    weather = results.get(
        "weather_prediction",
        results.get(
            "weather",
            ""
        )
    )


    # ========================================================
    # 1. PROJECT RISK
    # ========================================================

    if project_risk == "high":

        recommendations.append({
            "category": "Project",
            "priority": "High",
            "action": (
                "Review project cost, schedule and "
                "structural risk factors immediately."
            )
        })

    elif project_risk == "medium":

        recommendations.append({
            "category": "Project",
            "priority": "Medium",
            "action": (
                "Monitor project schedule, cost and "
                "execution conditions closely."
            )
        })


    # ========================================================
    # 2. EQUIPMENT RISK
    # ========================================================

    try:

        mttf = float(
            equipment_mttf
        )

        if mttf < 100:

            recommendations.append({
                "category": "Equipment",
                "priority": "Critical",
                "action": (
                    "Schedule immediate equipment "
                    "inspection and maintenance."
                )
            })

        elif mttf < 300:

            recommendations.append({
                "category": "Equipment",
                "priority": "Medium",
                "action": (
                    "Plan preventive equipment maintenance "
                    "before expected failure."
                )
            })

    except (
        TypeError,
        ValueError
    ):

        pass


    # ========================================================
    # 3. WEATHER RISK
    # ========================================================

    bad_weather = {
        "Rain",
        "Light Rain",
        "Heavy Rain",
        "Windy",
        "Overcast"
    }

    if weather in bad_weather:

        recommendations.append({
            "category": "Weather",
            "priority": "High",
            "action": (
                f"Review outdoor construction activities "
                f"because of {weather} conditions."
            )
        })


    # ========================================================
    # 4. WORKER SAFETY / PPE
    # ========================================================

    violations = worker_report.get(
        "confirmed_violations",
        []
    )


    for violation in violations:

        if violation == "NO-Hardhat":

            action = (
                "Provide hardhats and prevent affected "
                "workers from entering unsafe areas."
            )

        elif violation == "NO-Mask":

            action = (
                "Provide required masks and verify "
                "correct usage."
            )

        elif violation == "NO-Safety Vest":

            action = (
                "Provide reflective safety vests "
                "before work continues."
            )

        else:

            action = (
                f"Resolve detected safety violation: "
                f"{violation}."
            )


        recommendations.append({
            "category": "Worker Safety",
            "priority": "High",
            "action": action
        })


    # ========================================================
    # 5. SITE RISK
    # ========================================================

    site_score = site_report.get(
        "site_risk_score",
        0
    )

    try:

        site_score = float(
            site_score
        )

    except (
        TypeError,
        ValueError
    ):

        site_score = 0


    if site_score >= 60:

        recommendations.append({
            "category": "Site Risk",
            "priority": "High",
            "action": (
                "Conduct an additional site inspection "
                "and restrict unsafe work areas."
            )
        })

    elif site_score >= 30:

        recommendations.append({
            "category": "Site Risk",
            "priority": "Medium",
            "action": (
                "Increase site monitoring and review "
                "identified hazards."
            )
        })


    # ========================================================
    # 6. COMPLIANCE
    # ========================================================

    compliance_status = compliance_report.get(
        "compliance_status",
        "Unknown"
    )


    if compliance_status == "Non-Compliant":

        recommendations.append({
            "category": "Compliance",
            "priority": "Critical",
            "action": (
                "Immediately resolve compliance findings "
                "before affected work continues."
            )
        })

    elif compliance_status == "Partially Compliant":

        recommendations.append({
            "category": "Compliance",
            "priority": "High",
            "action": (
                "Resolve outstanding compliance findings "
                "and verify PPE requirements."
            )
        })


    # ========================================================
    # 7. INSURANCE RISK
    # ========================================================

    insurance_level = insurance_report.get(
        "insurance_risk_level",
        "Unknown"
    )


    if insurance_level == "High":

        recommendations.append({
            "category": "Insurance",
            "priority": "High",
            "action": (
                "Perform an immediate operational risk "
                "review and resolve safety and "
                "maintenance issues."
            )
        })

    elif insurance_level == "Medium":

        recommendations.append({
            "category": "Insurance",
            "priority": "Medium",
            "action": (
                "Monitor operational risks and address "
                "outstanding safety or maintenance issues."
            )
        })


    # ========================================================
    # 8. REMOVE DUPLICATES
    # ========================================================

    unique_recommendations = []

    seen = set()


    for recommendation in recommendations:

        key = (
            recommendation["category"],
            recommendation["action"]
        )

        if key not in seen:

            seen.add(key)

            unique_recommendations.append(
                recommendation
            )


    recommendations = unique_recommendations


    # ========================================================
    # 9. DEFAULT RECOMMENDATION
    # ========================================================

    if not recommendations:

        recommendations.append({
            "category": "General",
            "priority": "Low",
            "action": (
                "Continue routine monitoring, inspections "
                "and preventive safety controls."
            )
        })


    # ========================================================
    # RETURN
    # ========================================================

    return recommendations