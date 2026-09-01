class ComplianceAgent:
    REQUIRED_PPE = {
        "Hardhat": "Hardhat required",
        "Mask": "Mask required where applicable",
        "Safety Vest": "Safety vest required",
    }

    VIOLATION_RULES = {
        "NO-Hardhat": {
            "requirement": "Workers must wear hardhats.",
            "severity": "High",
            "action": "Provide hardhats and stop affected work until compliance is confirmed.",
        },
        "NO-Mask": {
            "requirement": "Workers must wear masks where required.",
            "severity": "Medium",
            "action": "Provide masks and verify that workers are using them correctly.",
        },
        "NO-Safety Vest": {
            "requirement": "Workers must wear high-visibility safety vests.",
            "severity": "High",
            "action": "Provide safety vests before affected workers continue work.",
        },
    }

    def assess_compliance(self, safety_report, worker_protection_report):
        confirmed_violations = (
            worker_protection_report["confirmed_violations"]
        )

        findings = []
        compliance_score = 100

        for violation in confirmed_violations:
            rule = self.VIOLATION_RULES.get(violation)

            if rule:
                findings.append({
                    "violation": violation,
                    "requirement": rule["requirement"],
                    "severity": rule["severity"],
                    "action": rule["action"],
                })

                if rule["severity"] == "High":
                    compliance_score -= 35
                else:
                    compliance_score -= 20

        compliance_score = max(compliance_score, 0)

        if compliance_score >= 80:
            compliance_status = "Compliant"
        elif compliance_score >= 50:
            compliance_status = "Partially Compliant"
        else:
            compliance_status = "Non-Compliant"

        return {
            "compliance_status": compliance_status,
            "compliance_score": compliance_score,
            "findings": findings,
            "evidence_count": len(safety_report["detections"]),
            "recommended_actions": [
                finding["action"] for finding in findings
            ],
        }