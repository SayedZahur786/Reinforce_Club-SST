import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui

detector = HandDetector(detectionCon=0.5,maxHands=2)
cam = cv2.VideoCapture(0)

cam.set(3, 640)
cam.set(4, 480)
while True:
  success, frame = cam.read()

  hand, frame = detector.findHands(frame)

  if hand and hand[0]['type'] == "Right":
    fingers = detector.fingersUp(hand[0])
    totalFingers = fingers.count(1)
    cv2.putText(frame, f'Fingers: {totalFingers}', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    if totalFingers == 5:
      pyautogui.press('up')
    if totalFingers == 4:
      pyautogui.press('down')
    if totalFingers == 1:
      pyautogui.press('right')
    if totalFingers == 2:
      pyautogui.press('left')
  
  
  
  cv2.imshow("Livefeed", frame)
  cv2.waitKey(1)
