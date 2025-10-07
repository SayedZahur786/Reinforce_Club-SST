import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time

# Configuration constants
DETECTION_CONFIDENCE = 0.8
MAX_HANDS = 1
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
HOOK_KEY = 'space'

# Initialize hand detector with improved settings
detector = HandDetector(detectionCon=DETECTION_CONFIDENCE, maxHands=MAX_HANDS)

# Initialize video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Cannot access camera")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
cap.set(cv2.CAP_PROP_FPS, 30)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01

print("🎮 Stickman Hook Gesture Controller Starting...")
print("📋 Instructions:")
print("   • Show 2+ fingers to HOOK/SWING")
print("   • Show 1 finger or fist to RELEASE")
print("   • Move mouse to the top-left corner to trigger fail-safe")
print("   • Press 'q' to quit")
print("\n⏳ Initializing camera...")
time.sleep(2)  # Allow camera to initialize

# Game state tracking
is_hooking = False

try:
    while True:
        success, img = cap.read()

        if not success:
            print("⚠️ Failed to read from camera")
            continue

        # Flip horizontally
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, draw=True)

        # Status overlay
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (CAMERA_WIDTH, 100), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)

        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            totalFingers = fingers.count(1)

            lmList = hand["lmList"]
            center_x, center_y = hand["center"]

            # Display finger count and hand position
            cv2.putText(img, f'Fingers: {totalFingers}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(img, f'Hand Center: ({center_x}, {center_y})', (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            should_hook = totalFingers > 1

            if should_hook and not is_hooking:
                pyautogui.keyDown(HOOK_KEY)  # Start hooking
                is_hooking = True
                cv2.putText(img, "🪝 HOOKING!", (200, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif not should_hook and is_hooking:
                pyautogui.keyUp(HOOK_KEY)    # Release hook
                is_hooking = False
                cv2.putText(img, "✋ RELEASED!", (200, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            elif is_hooking:
                cv2.putText(img, "🪝 HOOKING!", (200, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(img, "👊 READY", (200, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            cv2.circle(img, (center_x, center_y), 10, (255, 0, 255), -1)

        else:
            # No hands detected
            if is_hooking:
                pyautogui.keyUp(HOOK_KEY)
                is_hooking = False
            cv2.putText(img, 'No hands detected', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.putText(img, "📋 Show hand to control", (200, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        # Add instructions overlay
        cv2.putText(img, "Press 'q' to quit | 'r' to reset", (10, CAMERA_HEIGHT - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Show the image
        cv2.imshow("🎮 Stickman Hook Gesture Controller", img)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\n👋 Quitting...")
            break
        elif key == ord('r'):
            print("🔄 Resetting controller...")
            if is_hooking:
                pyautogui.keyUp(HOOK_KEY)
                is_hooking = False

except KeyboardInterrupt:
    print("\n⛔ Interrupted by user")
except Exception as e:
    print(f"\n❌ An error occurred: {e}")
finally:

    # Cleanup resources
    print("🧹 Cleaning up...")
    if is_hooking:
        pyautogui.keyUp(HOOK_KEY)
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Cleanup complete!")
