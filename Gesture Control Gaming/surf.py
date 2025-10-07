import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector

# Initialize the hand detector
detector = HandDetector(detectionCon=0.5, maxHands=1)

# Initialize the webcam
cam = cv2.VideoCapture(0)
cam.set(3, 480)  
cam.set(4, 480)  

while True:
    success, frame = cam.read()
    img = cv2.flip(frame, 1)  # Mirror effect
    hands, img = detector.findHands(img)

    if hands:
        fingers = detector.fingersUp(hands[0])
        totalFingers = fingers.count(1)

        # Show finger count on screen
        cv2.putText(img, f'Fingers: {totalFingers}', (50, 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)

        # Subway Surfers Controls
        
        
        # elif totalFingers == 3:
        #     pyautogui.press('right')
        if totalFingers == 5:
            pyautogui.keyUp('space')
        if totalFingers == 0:
            pyautogui.keyDown('space')

    cv2.imshow("Livefeed", img)
    cv2.waitKey(1)
