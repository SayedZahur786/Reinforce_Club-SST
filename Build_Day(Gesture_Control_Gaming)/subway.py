import cv2 
from cvzone.HandTrackingModule import HandDetector 
import pyautogui
import time

detector = HandDetector(detectionCon=0.5, maxHands=1)

cam = cv2.VideoCapture(0)

# cam.set(3,320)
# cam.set(4,240)
cam.set(3, 640)
cam.set(4, 480)

last_action_time = 0
cooldown = 1  # seconds between actions (prevents spamming)

while True:
    success, frame = cam.read()
    img = frame   # no flip


    hand,img= detector.findHands(img)
    
    # Check cooldown before triggering action
    if time.time() - last_action_time > cooldown:
        if hand and hand[0]['type'] == "Right":
            fingers=detector.fingersUp(hand[0])
            totalFingers = fingers.count(1)
            cv2.putText(img, f'Fingers: {totalFingers}', (50,50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            

            if totalFingers == 2:#go right
                
                pyautogui.press('right')
                last_action_time = time.time()
            elif totalFingers == 5:#go up
                
                pyautogui.press('up')
                last_action_time = time.time()
                
            
    if hand and hand[0]['type'] == "Left":
        fingers=detector.fingersUp(hand[0])
        totalFingers = fingers.count(1)
        cv2.putText(img, f'Fingers: {totalFingers}', (50,50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        

        if totalFingers == 2:#go left
                
            pyautogui.press('left')
            last_action_time = time.time()
        elif totalFingers == 5:#go down
                
            pyautogui.press('down')
            last_action_time = time.time()
        
    cv2.imshow('Livefeed', img)
    cv2.waitKey(1)