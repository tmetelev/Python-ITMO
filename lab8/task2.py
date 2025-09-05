import cv2
import time
import numpy as np


cap = cv2.VideoCapture(2)   # Obs virtual camera

while True:
    ret, frame = cap.read()
    # frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    contours = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        1.7,
        1000,
        maxRadius=200,
        minRadius=10)

    if contours is not None:
        contours = np.uint16(np.around(contours))
        (x, y, r) = contours[0, 0]
        cv2.circle(frame, (x, y), r, (0, 255, 0), 1)
        cv2.circle(frame, (x, y), 2, (0, 0, 255), 2)
        # modification var 7
        cv2.line(frame, (640, 360), (x, y), (0, 255, 0), 1)
        dist = np.sqrt((x - 640) ** 2 + (y - 360) ** 2)
        cv2.putText(frame, f'Dist: {dist:.2f} px', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 100))
        # print(x, y, r)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.05)

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
