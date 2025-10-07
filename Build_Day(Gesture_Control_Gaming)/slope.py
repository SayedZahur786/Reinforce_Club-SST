import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector
import time

detector = HandDetector(detectionCon=0.6, maxHands=1)
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

left_pressed = False
right_pressed = False

print("Starting hand controller for Slope. Switch to your browser and make the game active!")
time.sleep(3)

while True:
    success, frame = cam.read()
    if not success:
        break

    hands, img = detector.findHands(frame)

    if hands:
        hand = hands[0]
        
        if hand['type'] == "Right":
            fingers = detector.fingersUp(hand)
            totalFingers = fingers.count(1)

            cv2.putText(img, f'Fingers: {totalFingers}', (20, 50),
                        cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            if totalFingers == 0:
                if not left_pressed:
                    print("ACTION: Turning Left")
                    pyautogui.keyDown('left')
                    left_pressed = True
                if right_pressed:
                    pyautogui.keyUp('right')
                    right_pressed = False

            elif totalFingers == 1:
                if not right_pressed:
                    print("ACTION: Turning Right")
                    pyautogui.keyDown('right')
                    right_pressed = True
                if left_pressed:
                    pyautogui.keyUp('left')
                    left_pressed = False

            else:
                if left_pressed:
                    pyautogui.keyUp('left')
                    left_pressed = False
                if right_pressed:
                    pyautogui.keyUp('right')
                    right_pressed = False

    cv2.imshow("Hand Control - Slope", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()
