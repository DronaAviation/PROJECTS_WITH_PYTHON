from cvzone.FaceMeshModule import FaceMeshDetector
import cv2

cap = cv2.VideoCapture("http://127.0.0.1:5000/video_feed")

detector = FaceMeshDetector(staticMode=False, maxFaces=2, minDetectionCon=0.5, minTrackCon=0.5)

while True:
    success, img = cap.read()

    img, faces = detector.findFaceMesh(img, draw=True)

    if faces:
        for face in faces:
            leftEyeUpPoint = face[159]
            leftEyeDownPoint = face[23]
            leftEyeVerticalDistance, info = detector.findDistance(leftEyeUpPoint, leftEyeDownPoint)
            print(leftEyeVerticalDistance)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
