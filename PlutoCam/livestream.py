import cv2
import numpy as np
import subprocess

# Starting the drone video stream and setting up ffmpeg to convert the video stream
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
    raw_frame = ffmpeg_process.stdout.read(2048 * 1152 * 3) # Adjust dimensions based on your camera's resolution
    if not raw_frame:
        break

    # Convert the byte data to a numpy array
    frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((1152, 2048, 3))

    # Display the frame using OpenCV
    cv2.imshow('Video Stream', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up: terminate the process and close all OpenCV windows
process.terminate()
ffmpeg_process.terminate()
cv2.destroyAllWindows()
