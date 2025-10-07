# Asphalt Gesture Control System Script with Python, OpenCV, cvzone, etc Libraries
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import mediapipe
from pynput.keyboard import Key, Controller
detector = HandDetector(detectionCon=0.9, maxHands=2)
keyboard = Controller()
# Accelerate Function
def accelarate():
    print("accelarate on")
    # keyboard.press("w")
    pass

#Brake Function
def brakes(brake_bool):
    if brake_bool:
        print("brake on")
        keyboard.release("w")
        keyboard.press("s")
    else:
        print("brake off")
        keyboard.press("w")
        keyboard.release("s")

#Left Steering 
def left_steer(left_bool):
    
    if left_bool:
        keyboard.press("a")
        print("Left on")
    else:
        keyboard.release("a")
        print("Left off")
    pass

#Right Steering
def right_steer(right_bool):
    
    if right_bool:
        keyboard.press("d")
        print("Right On")
    else:
        keyboard.release("d")
        print("Right off")
    pass

#Nitro Function
def nitro():
    keyboard.tap(Key.space)
    print("nitro")
    pass

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

counter = 0
while True:
    success, frame = cap.read()
    frame = cv2.flip(frame,1)
    hand, img = detector.findHands(frame,True, flipType=False)
    key = cv2.waitKey(1)

    #Dictionary to save Hand in Order
    hand_dict = {
        "Right":[],
        "Left":[]
    }
    for x in hand:
        if x["type"] == "Right":
            hand_dict["Right"] = x
        else:
            hand_dict["Left"] = x
    # print(hand_dict)

    if hand:
        if hand_dict["Left"]!=[] and hand_dict["Right"]!=[]:
            fingers_right = detector.fingersUp(hand_dict["Right"])
            fingers_left = detector.fingersUp(hand_dict["Left"])
            # Accelaration control - Just Both Hands in front of the Camera
            if hand_dict["Left"]!=[] or hand_dict["Right"]!=[]:
                accelarate()
            
            # right steering control - Uses Left Hand
            if fingers_left==[0,1,0,0,0]:
                right_steer(right_bool=True)
            else:
                right_steer(right_bool=False)

            # left steering control - Uses Right Hand
            if fingers_right==[0,1,0,0,0]:
                left_steer(left_bool=True)
            else:
                left_steer(left_bool=False)

            #brakes/ drift - Flat Palm Action
            if fingers_right==[0,1,1,1,1] or fingers_left==[0,1,1,1,1]:
                brakes(brake_bool=True)
            else:
                brakes(brake_bool=False)
            
            #Nitro Control - SpiderMan Action with Right Hand
            if fingers_right==[0,1,0,0,1]:
                if counter%10:
                    nitro()
                counter+=1
        cv2.imshow("Vid Capture", frame)
    
    # Press X on the Keyword to Exit the Program
    if key==ord("x"):
        break

