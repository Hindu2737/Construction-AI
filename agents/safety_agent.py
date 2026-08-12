from ultralytics import YOLO


class SafetyAgent:
    VIOLATION_CLASSES = {
        "NO-Hardhat",
        "NO-Mask",
        "NO-Safety Vest",
    }

    def __init__(self):
        self.model = YOLO("models/safety_yolo/weights/best.pt")

    def inspect_image(self, image_path):
        results = self.model(image_path, verbose=False)

        detections = []

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                label = result.names[class_id]

                detections.append({
                    "label": label,
                    "confidence": round(confidence, 2),
                })

        violations = [
            item for item in detections
            if item["label"] in self.VIOLATION_CLASSES
        ]

        return {
            "status": "Unsafe" if violations else "Safe",
            "detections": detections,
            "violations": violations,
        }