import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui

cam = cv2.VideoCapture(0)
cam.set(3,600)

detector = HandDetector(detectionCon=0.5,maxHands=1)

while True:

    status, LiveFeed = cam.read()

    hands, LiveFeed = detector.findHands(LiveFeed)

    if hands:

        fingers = detector.fingersUp(hands[0])

        if fingers[2]==1 and fingers[1]==1:    #up
            pyautogui.keyDown('up')
            pyautogui.keyUp('down')
            pyautogui.keyUp('left')
            pyautogui.keyUp('right')
        elif fingers[3]==1 and fingers[4]==1:   #down
            pyautogui.keyDown('down')
            pyautogui.keyUp('up')
            pyautogui.keyUp('left')
            pyautogui.keyUp('right')
        elif fingers[4]==1:             #right
            pyautogui.keyDown('right')
            pyautogui.keyUp('down')
            pyautogui.keyUp('left')
            pyautogui.keyUp('up')
        elif fingers[1]==1:             #left
            pyautogui.keyDown('left')
            pyautogui.keyUp('down')
            pyautogui.keyUp('up')
            pyautogui.keyUp('right')
        else:
            pyautogui.keyUp('up')
            pyautogui.keyUp('left')
            pyautogui.keyUp('right')
            pyautogui.keyUp('down')
    

    cv2.imshow("LiveFeed",LiveFeed)

    if cv2.waitKey(1) & 0xFF == 27:     # 27 for esc
        break
