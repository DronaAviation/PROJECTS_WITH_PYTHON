import cv2
import numpy as np
import subprocess
import plutocam

# Global variable to track capture state
capturing = False

# Function to start the video streaming process
def start_video_stream():
    process = subprocess.Popen(
        ["plutocam", "stream", "start", "--out-file", "-"],
        stdout=subprocess.PIPE
    )
    ffmpeg_process = subprocess.Popen(
        ["ffmpeg", "-i", "-", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
        stdin=process.stdout,
        stdout=subprocess.PIPE
    )
    return ffmpeg_process

# Function to capture video frames to a file
def capture_video(drone):
    global capturing
    capturing = True
    with open('out.h264', 'wb') as fp:
        for frame in drone.start_video_stream():
            if not capturing:
                break
            fp.write(frame.frame_bytes)
    capturing = False

# Main function to handle streaming and capture logic
def main():
    global capturing
    # Initialize drone and start streaming
    drone = plutocam.LWDrone()
    drone.set_time()
    ffmpeg_process = start_video_stream()

    while True:
        # Read the frame from ffmpeg output
        raw_frame = ffmpeg_process.stdout.read(2048 * 1152 * 3)
        if not raw_frame:
            break
        frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((1152, 2048, 3))

        # Display the frame using OpenCV
        cv2.imshow('Video Stream', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):  # Toggle 'c' for capture
            if capturing:
                capturing = False
            else:
                # Start capturing if not already capturing
                capture_video(drone)

    # Clean up: terminate the process and close all OpenCV windows
    ffmpeg_process.terminate()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
