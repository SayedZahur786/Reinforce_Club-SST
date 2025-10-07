import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time

detector = HandDetector(detectionCon=0.65, maxHands=2)

cam = cv2.VideoCapture(0)
cam.set(3, 800)
cam.set(4, 600)

lstime = time.time()
shoot_delay = 0.1
mouseDown = False
frame_interval = 2
frame_count = 0

while True:
    success, img = cam.read()
    frame_count += 1
    hand, img = detector.findHands(img)

    if frame_count % frame_interval == 0:
        frame_count = 0

    if hand and hand[0]['type'] == "Right":
        fingers = detector.fingersUp(hand[0])  # finger = [thumb, index, middle, ring, pinky]
        lmList1 = hand[0]["lmList"]
        length = 0
        
        x1, y1 = lmList1[8][0:2]
        x2, y2 = lmList1[12][0:2]
        threshold = 16 #If the difference between y1 and y2 is less than the threshold, then we will consider the line horizontal
        if abs(y1-y2) < threshold:
            length, info, img = detector.findDistance((x1, y1), (x2, y2), img, color=(255, 0, 255), scale=10) #length is the distance in pixels and img is the visual dots and info gives the coordinates of the three points that are shown

        #Shooting
        if fingers[0] == 0:
            if not mouseDown:
                pyautogui.mouseDown()
                mouseDown = True
        else:
            if mouseDown:
                pyautogui.mouseUp()
                mouseDown = False

        if length <= 19:
            #Jump
            if fingers[2] == 1 and fingers[1] == 1:
                pyautogui.keyDown('space')
            elif fingers[2] == 0 and fingers[1] == 0:
                pyautogui.keyUp('space')
            else:
                #Forward
                if fingers[1] == 1:
                    pyautogui.keyDown('w')
                elif fingers[1] == 0:
                    pyautogui.keyUp('w')
                
                #Backward
                if fingers[2] == 1:
                    pyautogui.keyDown('s')
                elif fingers[2] == 0:
                    pyautogui.keyUp('s')   
        else:
            #Dash-forward
            if fingers[2] == 1 and fingers[1] == 1:
                pyautogui.keyDown('shift')
                pyautogui.keyDown('w')
            elif fingers[2] == 0 or fingers[1] == 0:
                pyautogui.keyUp('shift')
                pyautogui.keyUp('w')
            else:
                #Forward
                if fingers[1] == 1:
                    pyautogui.keyDown('w')
                elif fingers[1] == 0:
                    pyautogui.keyUp('w')
                
                #Backward
                if fingers[2] == 1:
                    pyautogui.keyDown('s')
                elif fingers[2] == 0:
                    pyautogui.keyUp('s')   


        #Reload
        if fingers[4] == 1:
            pyautogui.keyDown('r')
        elif fingers[4] == 0:
            pyautogui.keyUp('r')   

    if hand and hand[0]['type'] == "Left":
        fingers = detector.fingersUp(hand[0])  # finger = [thumb, index, middle, ring, pinky]
        
        #Crouch
        if fingers[0] == 1 and fingers[1] == 1:
            pyautogui.keyDown('c')
        elif fingers[0] == 0 and fingers[1] == 0:
            pyautogui.keyUp('c')
        else:
            #Right
            if fingers[0] == 1:
                pyautogui.keyDown('d')
            elif fingers[0] == 0:
                pyautogui.keyUp('d')

            #Left
            if fingers[1] == 1:
                pyautogui.keyDown('a')
            elif fingers[1] == 0:
                pyautogui.keyUp('a')
        
        #Cursor move down
        if fingers[2] == 1 and fingers[3] == 1:
            pyautogui.move(0, 50)
        elif fingers[2] == 0 and fingers[3] == 1:
            pyautogui.move(0, 0)
        else:
            #Cursor move up
            if fingers[2] == 1:
                pyautogui.move(0, -50)
            elif fingers[2] == 0:
                pyautogui.move(0, 0)

        #Cursor move left
        if fingers[4] == 1 and fingers[3] == 1:
            pyautogui.move(-50, 0)
        elif fingers[4] == 0 and fingers[3] == 1:
            pyautogui.move(0, 0)
        else:
            #Cursor move right
            if fingers[4] == 1:
                pyautogui.move(50, 0)
            elif fingers[4] == 0:
                pyautogui.move(0, 0)

    cv2.imshow("Livefeed", img)
    cv2.waitKey(1)


