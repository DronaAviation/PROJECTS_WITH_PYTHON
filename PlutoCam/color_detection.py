import cv2

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape
    cx, cy = width // 2, height // 2
    hue_value = hsv_frame[cy, cx][0]
    
    color = ("RED" if hue_value < 5 or hue_value >= 167 else
             "ORANGE" if hue_value < 22 else
             "YELLOW" if hue_value < 33 else
             "GREEN" if hue_value < 78 else
             "BLUE" if hue_value < 131 else
             "VIOLET")
    
    b, g, r = map(int, frame[cy, cx])
    cv2.putText(frame, color, (10, 70), 0, 1.5, (b, g, r), 2)
    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)
    
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
