import cvzone
from cvzone.FaceDetectionModule import FaceDetector
import cv2

cap = cv2.VideoCapture("http://127.0.0.1:5000/video_feed")
#cap = cv2.VideoCapture(0)

# minDetectionCon: Minimum detection confidence threshold
# modelSelection: 0 for short-range detection (2 meters), 1 for long-range detection (5 meters)
detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)

# Run the loop to continually get frames from the webcam
while True:
    success, img = cap.read()
    img, bboxs = detector.findFaces(img, draw=False)
    if bboxs:
        for bbox in bboxs:
            center = bbox["center"]
            x, y, w, h = bbox['bbox']
            score = int(bbox['score'][0] * 100)

            cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
            cvzone.putTextRect(img, f'{score}%', (x, y - 10))
            cvzone.cornerRect(img, (x, y, w, h))

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
