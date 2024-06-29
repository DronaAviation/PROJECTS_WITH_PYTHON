import cv2
import numpy as np
import subprocess
import threading
import os
from cvzone.FaceDetectionModule import FaceDetector

# Define the resolution of the video stream
frame_width = 2048
frame_height = 1152
frame_size = frame_width * frame_height * 3

# Start streaming from the drone
process = subprocess.Popen(
    ["plutocam", "stream", "start", "--out-file", "-"],
    stdout=subprocess.PIPE
)

# Use ffmpeg to process the stream
ffmpeg_process = subprocess.Popen(
    ["ffmpeg", "-i", "-", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
    stdin=process.stdout,
    stdout=subprocess.PIPE
)

def process_frame():
    detector = FaceDetector()
    while True:
        # Read a raw frame from the ffmpeg output
        raw_frame = ffmpeg_process.stdout.read(frame_size)
        if not raw_frame:
            break

        # Convert the raw frame to a NumPy array and reshape
        frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((frame_height, frame_width, 3))

        # Resize frame to a smaller resolution to increase processing speed
        frame_resized = cv2.resize(frame, (1024, 576))

        # Apply face detection
        frame_resized, bboxs = detector.findFaces(frame_resized, draw=False)

        if bboxs:
            # Get the coordinates of the first detected face
            fx, fy = bboxs[0]["center"][0], bboxs[0]["center"][1]
            pos = [fx, fy]
            cv2.circle(frame_resized, (fx, fy), 80, (0, 0, 255), 2)
            cv2.putText(frame_resized, str(pos), (fx + 15, fy - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.line(frame_resized, (0, fy), (1024, fy), (0, 0, 0), 2)  # x line
            cv2.line(frame_resized, (fx, 576), (fx, 0), (0, 0, 0), 2)  # y line
            cv2.circle(frame_resized, (fx, fy), 15, (0, 0, 255), cv2.FILLED)
            cv2.putText(frame_resized, "TARGET LOCKED", (650, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        else:
            cv2.putText(frame_resized, "NO TARGET", (650, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            cv2.circle(frame_resized, (512, 288), 80, (0, 0, 255), 2)
            cv2.circle(frame_resized, (512, 288), 15, (0, 0, 255), cv2.FILLED)
            cv2.line(frame_resized, (0, 288), (1024, 288), (0, 0, 0), 2)  # x line
            cv2.line(frame_resized, (512, 576), (512, 0), (0, 0, 0), 2)  # y line

        # Display the frame with face detection
        cv2.imshow('Face Detection', frame_resized)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Terminate the subprocess and close OpenCV windows
    process.terminate()
    cv2.destroyAllWindows()

# Run frame processing in a separate thread
thread = threading.Thread(target=process_frame)
thread.start()
thread.join()
