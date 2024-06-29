# Press 'R' for Red color
# Press 'G' for Green color
# # Press 'Y' for Yellow color
# # Press 'B' for Blue color

import cv2
import numpy as np
import subprocess
import threading
import os

# Start streaming from the drone
process = subprocess.Popen(
    ["pylwdrone", "stream", "start", "--out-file", "-"],
    stdout=subprocess.PIPE
)

# Use ffmpeg to process the stream
ffmpeg_process = subprocess.Popen(
    ["ffmpeg", "-i", "-", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
    stdin=process.stdout,
    stdout=subprocess.PIPE
)

def process_frame():
    color_ranges = {
        'R': ([0, 120, 70], [10, 255, 255], [170, 120, 70], [180, 255, 255], [0, 0, 255]),
        'G': ([36, 25, 25], [86, 255, 255], [0, 0, 0], [0, 0, 0], [0, 255, 0]),
        'B': ([94, 80, 2], [126, 255, 255], [0, 0, 0], [0, 0, 0], [255, 0, 0]),
        'Y': ([25, 150, 150], [35, 255, 255], [0, 0, 0], [0, 0, 0], [0, 255, 255])
    }

    current_color = 'R'

    while True:
        # Read a raw frame from the ffmpeg output
        raw_frame = ffmpeg_process.stdout.read(2048 * 1152 * 3)
        if not raw_frame:
            break

        # Convert the raw frame to a NumPy array and reshape
        frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((1152, 2048, 3))

        # Resize frame to a smaller resolution to increase processing speed
        frame_resized = cv2.resize(frame, (1024, 576))

        # Apply Gaussian Blur to reduce noise
        blurred = cv2.GaussianBlur(frame_resized, (11, 11), 0)

        # Convert frame to HSV color space for color detection
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # Get the current color range
        lower1, upper1, lower2, upper2, highlight_color = color_ranges[current_color]

        # Create masks for the selected color
        mask1 = cv2.inRange(hsv, np.array(lower1), np.array(upper1))
        mask2 = cv2.inRange(hsv, np.array(lower2), np.array(upper2))
        mask = mask1 + mask2

        # Apply morphological transformations to refine the mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Highlight the detected color in the frame
        result = frame_resized.copy()
        result[mask > 0] = highlight_color  # Highlight detected color

        # Count the number of non-zero pixels in the mask
        num_detected_pixels = cv2.countNonZero(mask)
        text = f"{current_color} color pixels detected: {num_detected_pixels}"
        cv2.putText(result, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the frame with highlighted color
        cv2.imshow('Color Detection', result)

        # Check for key presses and update the current color
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key in [ord('R'), ord('G'), ord('B'), ord('Y')]:
            current_color = chr(key)

    # Terminate the subprocess and close OpenCV windows
    process.terminate()
    cv2.destroyAllWindows()

# Run frame processing in a separate thread
thread = threading.Thread(target=process_frame)
thread.start()
thread.join()
