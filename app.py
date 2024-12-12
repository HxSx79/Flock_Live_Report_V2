"""Main application file"""
from flask import Flask, render_template, Response, jsonify, request
from services.camera_service import CameraService
from services.detection_service import DetectionService
from services.data_service import DataService
import cv2
import os
from config import UPLOAD_FOLDER

app = Flask(__name__)
camera_service = CameraService()
detection_service = DetectionService()
data_service = DataService()

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', 
                         current_datetime=datetime.now().strftime("%A, %B %d, %Y %H:%M:%S"))

@app.route('/video_feed')
def video_feed():
    def generate_frames():
        while True:
            ret, frame = camera_service.read_frame()
            if not ret:
                break
            frame, detections = detection_service.process_frame(frame)
            data_service.update_production('line1', detections)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/production_data')
def production_data():
    return jsonify(data_service.get_production_data())

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'success': False, 'error': 'No video file'})
    
    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    
    video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
    video_file.save(video_path)
    camera_service.set_test_video(video_path)
    
    return jsonify({'success': True})

if __name__ == '__main__':
    camera_service.start()
    app.run(host='0.0.0.0', port=8080, debug=False)