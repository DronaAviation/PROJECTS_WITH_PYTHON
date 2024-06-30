#press C to capture images
import cv2
import numpy as np
import subprocess

process = subprocess.Popen(
    ["plutocam", "stream", "start", "--out-file", "-"],
    stdout=subprocess.PIPE
)

ffmpeg_process = subprocess.Popen(
    ["ffmpeg", "-i", "-", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
    stdin=process.stdout,
    stdout=subprocess.PIPE
)

image_counter = 0

while True:
    raw_frame = ffmpeg_process.stdout.read(2048 * 1152 * 3)
    if not raw_frame:
        break

    frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((1152, 2048, 3))
    cv2.imshow('Video Stream', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        image_filename = f'pluto{image_counter}.png'
        cv2.imwrite(image_filename, frame)
        print(f'Image captured and saved as {image_filename}')
        image_counter += 1

process.terminate()
ffmpeg_process.terminate()
cv2.destroyAllWindows()
