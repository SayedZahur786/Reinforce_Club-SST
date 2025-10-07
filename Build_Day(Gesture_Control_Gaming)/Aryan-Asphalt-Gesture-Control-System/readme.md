# Asphalt 9: Gesture Control System

Drive like never before! This project uses your webcam to translate hand gestures into in-game commands for Asphalt 9: Legends, allowing you to steer, accelerate, brake, and use nitro with simple hand movements.



## 🚀 Features

* **Gesture-Based Driving**: Control your car's core functions without a keyboard.
* **Two-Handed Control**: Uses a two-handed system for intuitive steering and actions.
* **Real-Time Response**: Leverages OpenCV and MediaPipe for fast hand tracking and gesture recognition.
* **Simple Setup**: Requires only a webcam and a few common Python libraries.

---

## How It Works

The script captures video from your webcam and uses the `cvzone` library to detect and track your hands. Based on the fingers you raise on each hand, it simulates key presses using `pynput` to control the game.

### Control Mapping 🎮

| Action          | Hand           | Gesture                         | Keyboard Key     |
| :-------------- | :------------- | :------------------------------ | :--------------- |
| **Accelerate** | Both           | Any hand is visible             | `W` (held down)  |
| **Brake / Drift** | Either         | Open Palm (Four fingers up)     | `S` (held down)  |
| **Steer Left** | **Right** Hand | Index Finger Up                 | `A` (held down)  |
| **Steer Right** | **Left** Hand  | Index Finger Up                 | `D` (held down)  |
| **Nitro** | **Right** Hand | "Spider-Man" (Index & Pinky up) | `Space` (tapped) |

**Note on Steering:** The steering is intentionally inverted for a more natural feel. To steer your car left, you point with your right hand, and to steer right, you point with your left hand, similar to turning a steering wheel.

---

## Prerequisites

Before you begin, make sure you have Python installed on your system. You will also need the following libraries:

* **OpenCV**: For video capture and image processing.
* **cvzone**: A convenient wrapper for computer vision tasks, including hand tracking.
* **pynput**: To control the keyboard and simulate key presses.
* **MediaPipe**: The underlying engine used by `cvzone` for machine learning models.

You can install all the required libraries with a single command:

```bash
pip install -r requirements.txt
```

## How to Use

1.  **Start the Game**: Launch Asphalt 9: Legends and have it ready in the background. Ensure the game is using W (Accelerate), S (Brake), A (Steer Left), D (Steer Right), and Space (Nitro) for controls.
2.  **Run the Script**: Execute the Python script from your terminal:
    ```bash
    python your_script_name.py
    ```
3.  **Focus the Game Window**: A new window titled "Vid Capture" will appear, showing your webcam feed. **Immediately click on the Asphalt 9 game window** to make it the active application. This ensures that the key presses sent by the script are received by the game.
4.  **Start Driving**: Position yourself so the webcam can clearly see both of your hands. Use the gestures listed above to control your car.
5.  **Exit**: To stop the program, make the "Vid Capture" window active and press the **'x'** key.