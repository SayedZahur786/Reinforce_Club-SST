import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time

detector = HandDetector(detectionCon=0.7, maxHands=1)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    hands, img = detector.findHands(frame)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        totalFingers = fingers.count(1)

        cv2.putText(img, f'Fingers: {totalFingers}', (50, 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        if totalFingers == 5:
            pyautogui.press('space')
    time.sleep(0.1)
    cv2.imshow("Hand Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
