import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui

detector = HandDetector(detectionCon=0.5, maxHands=2) #maxHands-> Maximum number of Hands $ detectionCon-> Detection Confidence means the amount of sureity for detecting a hand

cam = cv2.VideoCapture(0) # 0 is the index for the in-built camera

cam.set(3, 800) #Configure the width
cam.set(4, 600) #Configure the height

while True:
    success, frame = cam.read() #cam.read() tries to capture a frame from the camera or video. 
                                #success will be True if the frame is captured successfully, otherwise False.
                                #frame will contain the image data of the captured frame, if successful.


    img = cv2.flip(frame,1) #0-> x-axis and 1-> y-axis and -1-> both axis

    hand, img = detector.findHands(img)

    if hand and hand[0]['type'] == "Right": #Check if the hand is right

        fingers = detector.fingersUp(hand[0]) #Checks if the fingers of the right hand is up or not
        totalFingers = fingers.count(1) #1-> open palm and 0-> closed palm

        cv2.putText(img, f'Fingers: {totalFingers}', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        if totalFingers==1:
            pyautogui.keyDown('right')
            pyautogui.keyUp('left')
            pyautogui.keyUp('down')
            pyautogui.keyUp('up')
        if totalFingers==2:
            pyautogui.keyDown('left')
            pyautogui.keyUp('right')
            pyautogui.keyUp('down')
            pyautogui.keyUp('up')
        if totalFingers == 5:
            pyautogui.keyDown('up')
            pyautogui.keyUp('left')
            pyautogui.keyUp('down')
            pyautogui.keyUp('right')

        if totalFingers == 0:
            pyautogui.keyDown('down')
            pyautogui.keyUp('up')
            pyautogui.keyUp('left')
            pyautogui.keyUp('right')

    cv2.imshow('Livefeed', img)
    cv2.waitKey(1) #wait for 1sec and then send frames
