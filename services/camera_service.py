"""Camera handling service"""
import cv2
from config import CAMERA_ID, CAMERA_WIDTH, CAMERA_HEIGHT, FPS

class CameraService:
    def __init__(self):
        self.cap = None
        self.test_video = None
        
    def start(self):
        """Start camera capture"""
        self.cap = cv2.VideoCapture(CAMERA_ID)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, FPS)
        
    def read_frame(self):
        """Read a frame from camera or test video"""
        if self.test_video:
            return self.test_video.read()
        if self.cap:
            return self.cap.read()
        return False, None
        
    def set_test_video(self, video_path):
        """Set a test video for processing"""
        if self.test_video:
            self.test_video.release()
        self.test_video = cv2.VideoCapture(video_path)
        
    def release(self):
        """Release all video captures"""
        if self.cap:
            self.cap.release()
        if self.test_video:
            self.test_video.release()