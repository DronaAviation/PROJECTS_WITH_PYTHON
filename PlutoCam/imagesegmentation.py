import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import cv2

cap = cv2.VideoCapture("http://127.0.0.1:5000/video_feed")

cap.set(3, 640)
cap.set(4, 480)

# Initialize the SelfiSegmentation class. It will be used for background removal.
# model is 0 or 1 - 0 is general 1 is landscape(faster)
segmentor = SelfiSegmentation(model=0)

while True:
    success, img = cap.read()

    # Use the SelfiSegmentation class to remove the background
    # Replace it with a magenta background (255, 0, 255)
    imgOut = segmentor.removeBG(img, imgBg=(255, 0, 255), cutThreshold=0.1)

    cv2.imshow("Image", imgOut)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
