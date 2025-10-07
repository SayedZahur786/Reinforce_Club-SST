# pip install opencv-python cvzone pyautogui mediapipe

import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time

# NOTE: This program can also be used to play chrome Dino!! 

# Initialize Hand Detector
detector = HandDetector(detectionCon=0.85, maxHands=1)

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Lower resolution for faster processing - NO LAG!!!!!!!!!!!!
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

last_press_time = 0
press_cooldown = 0.5  # seconds

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    hands, img = detector.findHands(frame)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        totalFingers = fingers.count(1)

        cv2.putText(img, f'Fingers: {totalFingers}', (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Space key press with cooldown
        current_time = time.time()
        if totalFingers == 5 and current_time - last_press_time > press_cooldown:
            pyautogui.press('space')
            last_press_time = current_time

    cv2.imshow("Hand Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
