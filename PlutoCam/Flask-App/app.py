import cv2
import numpy as np
import subprocess
import threading
from flask import Flask, render_template, Response

#cap = cv2.VideoCapture("http://127.0.0.1:5000/video_feed")  # Use the URL as the video source


app = Flask(__name__)

frame = None  # Global variable to store the current frame

def capture_video():
    global frame
    process = subprocess.Popen(
        ["plutocam", "stream", "start", "--out-file", "-"],
        stdout=subprocess.PIPE
    )

    ffmpeg_process = subprocess.Popen(
        ["ffmpeg", "-i", "-", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
        stdin=process.stdout,
        stdout=subprocess.PIPE
    )

    while True:
        # Read the frame from ffmpeg output
        raw_frame = ffmpeg_process.stdout.read(2048 * 1152 * 3)  # Adjust dimensions based on your camera's resolution
        if not raw_frame:
            break

        # Convert the byte data to a numpy array
        frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((1152, 2048, 3))

        # Display the frame using OpenCV
        #cv2.imshow('Video Stream', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up: terminate the process and close all OpenCV windows
    process.terminate()
    ffmpeg_process.terminate()
    cv2.destroyAllWindows()

# Flask route to serve the video feed
@app.route('/video_feed')
def video_feed():
    def generate():
        global frame
        while True:
            if frame is None:
                continue
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Start video capture thread
    video_thread = threading.Thread(target=capture_video)
    video_thread.daemon = True
    video_thread.start()

    # Start Flask app
    app.run(host='0.0.0.0', port=5000)
