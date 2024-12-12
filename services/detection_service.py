"""YOLO detection service"""
from ultralytics import YOLO
import cv2
import numpy as np
from config import MODEL_PATH, CONFIDENCE_THRESHOLD

class DetectionService:
    def __init__(self):
        self.model = YOLO(MODEL_PATH)
        self.model.conf = CONFIDENCE_THRESHOLD
        
    def process_frame(self, frame):
        """Process a frame and return detections"""
        results = self.model(frame)
        return self._parse_results(results, frame)
        
    def _parse_results(self, results, frame):
        """Parse YOLO results and draw on frame"""
        detections = []
        if results[0].boxes is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            classes = results[0].boxes.cls.cpu().numpy()
            
            for box, cls in zip(boxes, classes):
                x1, y1, x2, y2 = map(int, box[:4])
                class_name = self.model.names[int(cls)]
                detections.append({
                    'class': class_name,
                    'box': (x1, y1, x2, y2)
                })
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, class_name, (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
        return frame, detections