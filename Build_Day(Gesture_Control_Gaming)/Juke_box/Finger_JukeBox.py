import cv2
from cvzone.HandTrackingModule import HandDetector
from pygame import mixer
import os

# ---------- Music Setup ----------
playlist = ["Song1.mp3", "Song2.mp3", "Song3.mp3", "Song4.mp3"]  
current_index = 0
mixer.init()
mixer.music.load(playlist[current_index])
mixer.music.play()

# ---------- Hand Detection Setup ----------
detector = HandDetector(detectionCon=0.5, maxHands=1)
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

volume = 0.5  # start at 50%
mixer.music.set_volume(volume)
paused = False

def next_track():
    global current_index
    current_index = (current_index + 1) % len(playlist)
    mixer.music.load(playlist[current_index])
    mixer.music.play()
    print(f"▶️ Next track: {playlist[current_index]}")

def prev_track():
    global current_index
    current_index = (current_index - 1) % len(playlist)
    mixer.music.load(playlist[current_index])
    mixer.music.play()
    print(f"◀️ Previous track: {playlist[current_index]}")

def toggle_play_pause():
    global paused
    if paused:
        mixer.music.unpause()
        print("▶️ Play")
    else:
        mixer.music.pause()
        print("⏸ Pause")
    paused = not paused

def stop_music():
    mixer.music.stop()
    print("⏹ Stop")

# ---------- Main Loop ----------
while True:
    success, frame = cam.read()
    if not success:
        break

    img = cv2.flip(frame, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        fingers = detector.fingersUp(hands[0])
        total = fingers.count(1)

        # Display finger count on screen
        cv2.putText(img, f'Fingers: {total}', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Gesture Controls
        if total == 0:
            toggle_play_pause()
        elif total == 1:
            volume = max(0.0, volume - 0.05)
            mixer.music.set_volume(volume)
            print(f"🔉 Volume down: {int(volume*100)}%")
        elif total == 2:
            volume = min(1.0, volume + 0.05)
            mixer.music.set_volume(volume)
            print(f"🔊 Volume up: {int(volume*100)}%")
        elif total == 3:
            next_track()
        elif total == 4:
            prev_track()
        elif total == 5:
            stop_music()

    cv2.imshow("Finger Jukebox", img)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
mixer.quit()
