from cvzone.FaceMeshModule import FaceMeshDetector
import cv2

def overlay_mask(mask_img, img, face_points):
    x_min = min(point[0] for point in face_points)
    y_min = min(point[1] for point in face_points)
    x_max = max(point[0] for point in face_points)
    y_max = max(point[1] for point in face_points)
    
    width = x_max - x_min
    height = y_max - y_min

    mask_resized = cv2.resize(mask_img, (width, height))

    mask_alpha = mask_resized[:, :, 3] / 255.0
    mask_rgb = mask_resized[:, :, :3]

    for c in range(0, 3):
        img[y_min:y_max, x_min:x_max, c] = mask_alpha * mask_rgb[:, :, c] + (1 - mask_alpha) * img[y_min:y_max, x_min:x_max, c]

    return img

mask_img = cv2.imread('ironman.png', cv2.IMREAD_UNCHANGED)
#mask_img = cv2.imread('spiderman.png', cv2.IMREAD_UNCHANGED)


cap = cv2.VideoCapture("http://127.0.0.1:5000/video_feed")

detector = FaceMeshDetector(staticMode=False, maxFaces=2, minDetectionCon=0.5, minTrackCon=0.5)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image")
        break

    img, faces = detector.findFaceMesh(img, draw=True)

    if faces:
        for face in faces:
            img = overlay_mask(mask_img, img, face)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
