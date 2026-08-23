class SafetyIntelligenceAgent:
    MIN_CONFIDENCE = 0.50

    ACTIONS = {
        "NO-Hardhat": "Provide hardhats and prevent entry until workers wear them.",
        "NO-Mask": "Provide required masks and verify workers are wearing them.",
        "NO-Safety Vest": "Provide reflective safety vests before work continues.",
    }

    def analyze_worker_protection(self, safety_report):
        confirmed_violations = [
            item
            for item in safety_report["violations"]
            if item["confidence"] >= self.MIN_CONFIDENCE
        ]

        # Keep each violation type once; multiple boxes can detect the same issue.
        violation_types = sorted({
            item["label"] for item in confirmed_violations
        })

        safety_score = 100 - (len(violation_types) * 25)
        safety_score = max(safety_score, 0)

        if safety_score >= 80:
            protection_level = "Good"
        elif safety_score >= 50:
            protection_level = "Needs Attention"
        else:
            protection_level = "Critical"

        actions = [
            self.ACTIONS[violation]
            for violation in violation_types
        ]

        return {
            "worker_protection_level": protection_level,
            "safety_score": safety_score,
            "confirmed_violations": violation_types,
            "recommended_actions": actions,
            "workers_detected": sum(
                1
                for item in safety_report["detections"]
                if item["label"] == "Person"
                and item["confidence"] >= self.MIN_CONFIDENCE
            ),
        }