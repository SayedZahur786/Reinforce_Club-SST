#How to play:
#1. Right hand controls changing lanes 
#2. Left hand controls jumping and rolling
#3. You cant use your fancy boards or headstarts yet.
#
#Right hand Controls:
#a. Open hand means changing to right and closed means changing to left.
#b. If you changed to lane once and wish to move in that direction again, just close and open your thumb once again.

#Left hand Controls:
#a. Open hand means jump and closed hand means roll.
#b. If you jump once or roll once and want same action again, just hide and show your thumb again.

#Some Tips
#a. Basic control of the game was Open hand and close hand and thumb is a action repeater.
#b. Always show your thumb as it keeps your controls in a neutral position.
#c. At starting Show both hand open in a upfront position(Thumbs towards middle).

#Notes
#1. If you want some changes for control mapping like Right hand controls changing lane to right ad jump and Left hand controlling
#   changing to left and rolling, suggest it to me please.


import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.5,maxHands=2)

cam = cv2.VideoCapture(0)

cam.set(3, 640)
cam.set(4, 480)
last_change = "none"
last_vertical = "none"
while True:
    success, frame = cam.read()
    img = cv2.flip(frame,1)


    hand, img = detector.findHands(img)
    if hand:
        for h in hand:
            if h['type'] == 'Right':
                fingers = detector.fingersUp(h)
                totalFingers = fingers.count(1)
                cv2.putText(img, f'Fingers: {totalFingers}', (50,50), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255))
                if totalFingers >= 4 and last_change !="right":
                    pyautogui.keyDown('right')
                    pyautogui.keyUp('right')
                    print("right once")
                    last_change = "right"
                elif totalFingers >=1 and totalFingers <= 4:
                    last_change = "none"
                elif totalFingers <=1  and last_change !="left":
                    pyautogui.keyDown('left')
                    pyautogui.keyUp('left')
                    print("left once")
                    last_change = "left"
            if h['type'] == 'Left':
                fingers = detector.fingersUp(h)
                totalFingers = fingers.count(1)
                cv2.putText(img, f'Fingers: {totalFingers}', (400,50), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255))
                if totalFingers >= 4  and last_vertical !="space":
                    pyautogui.keyDown('space')
                    pyautogui.keyUp('space')
                    print("jump once")
                    last_vertical = "space"
                elif totalFingers >=1 and totalFingers <= 4:
                    last_vertical = "none"
                elif totalFingers <=1  and last_vertical !="down":
                    pyautogui.keyDown('down')
                    pyautogui.keyUp('down')
                    print("down once")
                    last_vertical = "down"  
    cv2.imshow('Livefeed',img)
    cv2.waitKey(10)