import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector
import time

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(detectionCon=0.75, maxHands=2)

print("🦖 Dino Game Gesture Controller")
print("  Left hand index finger up = Jump")
print("  Right hand index finger up = Duck")
print("⚠️ Click on the Dino game to focus!")

prev_jump = False
prev_duck = False
cooldown = 0.3
last_action_time = 0

while True:
    ret, img = cap.read()
    if not ret:
        print("⚠️ Camera not detected.")
        break

    img = cv2.flip(img, 1)  # Mirror image for natural movement
    hands, img = detector.findHands(img)  # Returns list of hands

    jump_detected = False
    duck_detected = False
    action = "RUNNING"
    current_time = time.time()

    # Process hands
    if hands:
        for hand in hands:
            fingers = detector.fingersUp(hand)
            hand_type = hand["type"]  # 'Left' or 'Right'

            if hand_type == "Left" and fingers[1] == 1:
                jump_detected = True
            if hand_type == "Right" and fingers[1] == 1:
                duck_detected = True

    # Trigger jump
    if jump_detected and not prev_jump and current_time - last_action_time > cooldown:
        pyautogui.keyDown("space")
        pyautogui.keyUp("space")
        action = "JUMP"
        last_action_time = current_time

    # Trigger duck
    elif duck_detected and not prev_duck and current_time - last_action_time > cooldown:
        pyautogui.keyDown("down")
        pyautogui.keyUp("down")
        action = "DUCK"
        last_action_time = current_time

    prev_jump = jump_detected
    prev_duck = duck_detected

    # Display current action
    cv2.putText(img, f"Action: {action}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Dino Controller - Left Jump / Right Duck", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
