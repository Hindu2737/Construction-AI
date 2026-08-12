from pathlib import Path
from ultralytics import YOLO

data_path = Path(
    "datasets/contruction site safety image dataflow/css-data/data.yaml"
)

model = YOLO("yolov8n.pt")

model.train(
    data=str(data_path),
    epochs=50,
    imgsz=640,
    batch=8,
    project="models",
    name="safety_yolo",
)

print("Safety model training completed.")