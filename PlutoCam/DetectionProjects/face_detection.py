import cv2
import numpy as np
import pylwdrone
import ffmpeg  # This is from ffmpeg-python
import sys

# Load the pre-trained cascade classifier for hand detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

drone = pylwdrone.LWDrone()
drone.set_time()

window_name = 'Drone Video Stream'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
for packet in drone.start_video_stream():
    try:
        out, _ = (
            ffmpeg
            .input('pipe:', format='h264')
            .output('pipe:', format='rawvideo', pix_fmt='bgr24', vframes=8)
            .run(input=packet.frame_bytes, capture_stdout=True, capture_stderr=True)
        )

        frame = np.frombuffer(out, np.uint8)
        height, width = 1152, 2048
        frame = frame.reshape((height, width, 3))

        # Convert frame to UMat
        frame_um = cv2.UMat(frame)

        # Decode frame and perform face detection
        gray = cv2.cvtColor(frame_um, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Draw rectangles around detected faces and handle face position logic
        for (x, y, w, h) in faces:
            cv2.rectangle(frame_um, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Calculate face position
            px, py = x + w // 2, y + h // 2
            
            # Draw text showing face position
            cv2.putText(frame_um, str((px, py)), (px + 10, py - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

        # Display video stream
        cv2.imshow(window_name, frame_um.get())

        # Check for 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except ffmpeg.Error as e:
        print('An error occurred:', e.stderr.decode(), file=sys.stderr)

cv2.destroyAllWindows()
drone.stop_video_stream()


cv2.destroyAllWindows()
drone.stop_video_stream()
