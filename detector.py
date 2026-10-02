from collections import Counter
import numpy as np
from PIL import Image
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt"):
        # Load pre-trained YOLO object detection model
        self.model = YOLO(model_path)

    def detect_and_count(self, image):
        """
        Runs YOLO object detection on the input image.
        Returns:
            annotated_img (PIL.Image): Image with bounding boxes drawn.
            object_counts (dict): Dictionary mapping detected class names to their quantities.
        """
        if isinstance(image, np.ndarray):
            pil_img = Image.fromarray(image)
        else:
            pil_img = image

        # Run model inference
        results = self.model(pil_img)
        result = results[0]

        # Tally counts for each detected object class
        counts = Counter()
        if result.boxes is not None:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                class_name = self.model.names[cls_id]
                counts[class_name] += 1

        # Render bounding boxes onto image
        res_plotted = result.plot()
        annotated_img = Image.fromarray(res_plotted[..., ::-1])  # Convert BGR to RGB

        return annotated_img, dict(counts)
