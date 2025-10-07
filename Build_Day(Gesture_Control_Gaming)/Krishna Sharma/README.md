# Blink Control System

This Python script enables hands-free control of simple games and applications by detecting eye blinks. It uses a camera and the **cvzone** library to track facial landmarks, specifically focusing on the distance between the eyelids. This allows you to control actions like jumping in a game or pressing the spacebar with a simple blink.

The system is particularly well-suited for games that use a single, repetitive action, such as "jump" in the Google Chrome Dino game or "flap" in Flappy Bird.

## How It Works

The script uses a **Face Mesh Detector** to identify over 400 points on the face in real-time. To determine if a blink has occurred, it measures the vertical distance between key points on the upper and lower eyelids.

A key feature of this script is its ability to adapt to the user's distance from the camera. It calculates the height of the face in the camera frame and uses this to adjust the blink detection threshold. This means the system will work reliably whether you are close to the screen or sitting further away.

When a blink is detected, the script uses the **pynput** library to simulate a keyboard press (the spacebar by default), providing a seamless control experience.

## Prerequisites

Python version: 3.10 (update the .python-version file if necessary)

Before running the script, you need to install the following libraries:

* **cvzone**: A computer vision library built on top of OpenCV.

* **opencv-python**: The core OpenCV library.

* **mediapipe**: Used by cvzone for face mesh detection.

* **pynput**: For sending keystrokes.

You can install all of them using uv

```
uv sync
```

Alternatively, you can use pip:

```
pip install cvzone opencv-python mediapipe pynput
```
 
## Usage

1. Make sure you have a webcam connected and working.

2. Run the script from your terminal:

```
uv run main.py
```

OR

```
python main.py
```

4. Once the script is running, open a simple game like the Chrome Dino game. The script will automatically start detecting your blinks and controlling the game.

5. To stop the script, press **`Ctrl + C`** in the terminal or simply press **`q`** if the Livefeed display is enabled.

## Customization

The script can be easily customized to suit your needs:

* **Change the control key:** Modify the `_key` variable to use a different keyboard key. For example, to use the 'up' arrow key, change the line to `_key = Key.up`.

* **Adjust blink sensitivity:** The `_threshold` parameter controls the blink sensitivity. You can experiment with different values if the detection is too sensitive or not sensitive enough.

* **Display the live camera feed:** The line `cv2.imshow("Livefeed", frame)` is commented out. If you want to see what the camera is detecting, you can uncomment this line.

## Contributing

Feel free to open issues or submit pull requests if you have suggestions or improvements for this project.