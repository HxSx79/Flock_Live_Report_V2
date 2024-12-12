"""Configuration settings for the application"""
import os

# Camera settings
CAMERA_ID = 0
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
FPS = 30

# YOLO model settings
MODEL_PATH = "best.pt"
CONFIDENCE_THRESHOLD = 0.95

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
EXCEL_FILE = os.path.join(BASE_DIR, 'data', 'production_data.xlsx')

# Production settings
SHIFT_HOURS = 8
TARGET_PPH = {
    'line1': 100,
    'line2': 100
}