import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
detector = HandDetector(detectionCon=0.5, maxHands=1)
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

while True:
    success, frame = cam.read()
    img = cv2.flip(frame, 1)
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        totalfingers = fingers.count(1)

        cv2.putText(img, f'Fingers: {totalfingers}', (30, 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        if totalfingers == 5:
            pyautogui.press("space")

    cv2.imshow("Flappy Bird Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
