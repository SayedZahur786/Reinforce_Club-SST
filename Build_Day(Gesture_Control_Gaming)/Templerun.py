import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.7, maxHands=1)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

prev_x = None

while True:
    success, frame = cap.read()
    img = cv2.flip(frame, 1)
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        totalFingers = fingers.count(1)
        cx, cy = hand['center']

        
        if totalFingers == 1:
            pyautogui.press('up')

        
        elif totalFingers == 2:
            pyautogui.press('down')

        
        elif totalFingers == 3:
            pyautogui.press('right')
        

        elif totalFingers == 4:
            pyautogui.press('left')

        cv2.putText(img, f'Fingers: {totalFingers}', (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Subway Surfers Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
