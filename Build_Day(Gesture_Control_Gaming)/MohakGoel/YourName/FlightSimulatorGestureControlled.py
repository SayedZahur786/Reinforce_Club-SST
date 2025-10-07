import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui

detector = HandDetector(detectionCon=0.8, maxHands=2)
cam = cv2.VideoCapture(0)
cam.set(3, 1280)
cam.set(4, 720)

def press_only(keys_to_press):
    all_keys = ['w', 's', 'a', 'd', 'up', 'down']
    for k in all_keys:
        if k in keys_to_press:
            pyautogui.keyDown(k)
        else:
            pyautogui.keyUp(k)

while True:
    success, frame = cam.read()

    img = cv2.flip(frame, 1)
    hands, img = detector.findHands(img)

    active_keys = []

    if hands:
        for hand in hands:
            handType = hand['type']
            fingers = detector.fingersUp(hand)
            fingerCount = fingers.count(1)

            if handType == 'Left':
                if fingerCount == 5:
                    active_keys = ['w']
                elif fingerCount == 0:
                    active_keys = ['s']
                elif fingerCount == 1:
                    active_keys = ['up']
                elif fingerCount == 2:
                    active_keys = ['down']

            if handType == 'Right':
                if fingerCount == 5:
                    active_keys = ['a']
                elif fingerCount == 1:
                    active_keys = ['w', 'd']
                elif fingerCount == 2:
                    active_keys = ['s', 'd']
                elif fingerCount == 3:
                    active_keys = ['s', 'a']
                elif fingerCount == 4:
                    active_keys = ['w', 'a']
                elif fingerCount == 0:
                    active_keys = ['d']
    press_only(active_keys)

    cv2.imshow("Webcam", img)
    cv2.waitKey(1)
