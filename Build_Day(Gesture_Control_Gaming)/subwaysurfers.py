#subwaysurfer
import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
detector=HandDetector(detectionCon=0.5,maxHands=2)
last_action_time = time.time()
cooldown = 1
while True:
    success, frame =cap.read()
    img=cv2.flip(frame,1)

    hand,img=detector.findHands(img)
    if time.time() - last_action_time > cooldown:
        if hand and hand[0]['type']=="Right":
            fingers=detector.fingersUp(hand[0])
            totalFingers=fingers.count(1)
            cv2.putText(img,f'Fingers:{totalFingers}',(50,50),cv2.FONT_HERSHEY_PLAIN,2, (0,255,0),2)
            if totalFingers>=4 :
                pyautogui.press('right')
                last_action_time = time.time()
            if totalFingers<=1:
                pyautogui.press('left')
                last_action_time = time.time()

        if hand and hand[0]['type']=="Left":
            fingers=detector.fingersUp(hand[0])
            totalFingers=fingers.count(1)
            cv2.putText(img,f'Fingers:{totalFingers}',(50,50),cv2.FONT_HERSHEY_PLAIN,2, (0,255,0),2)
            if totalFingers>=4 :
                pyautogui.press('up')
                last_action_time = time.time()
            if totalFingers<=1:
                pyautogui.press('down')
                last_action_time = time.time()


    cv2.imshow('Livefeed',img)
    cv2.waitKey(1)