# 🎮 Stickman Hook Gesture Controller

A real-time hand gesture controller for the popular **Stickman Hook** game using computer vision and hand tracking technology.

## 🎯 Overview

This project implements a gesture-based control system that allows you to play Stickman Hook using hand gestures instead of keyboard inputs. The system uses your webcam to detect hand positions and translates finger movements into game controls.

## 🎮 How It Works

### Game Mechanics

- **Hook/Swing**: Show two or more fingers to make the stickman hook onto objects and swing
- **Release**: Show one finger or make a fist to release the hook and let the stickman fly
- **Timing**: The key to success is timing your hooks and releases to maintain momentum

### Gesture Controls

| Gesture                   | Action           | Game Effect  |
| ------------------------- | ---------------- | ------------ |
| ✌️ Two or more fingers up | Hold spacebar    | Hook/Swing   |
| ☝️ One finger or fist     | Release spacebar | Release hook |

## 🛠️ Technical Implementation

### Technologies Used

- **OpenCV (cv2)**: Computer vision library for camera input and image processing
- **CVZone HandTrackingModule**: Hand detection and finger tracking
- **PyAutoGUI**: Automated keyboard input simulation
- **Python**: Core programming language

### Key Features

1. **Real-time Hand Detection**: Uses MediaPipe-based hand tracking for accurate finger detection
2. **Mirror Mode**: Camera feed is flipped horizontally for intuitive control
3. **State Tracking**: Prevents key spamming by tracking hook state
4. **Visual Feedback**: On-screen indicators show current gesture and game state
5. **Error Handling**: Robust error handling for camera issues and interruptions

### Code Structure

```python
# Configuration Constants
DETECTION_CONFIDENCE = 0.8  # Hand detection accuracy
MAX_HANDS = 1              # Single hand tracking
CAMERA_WIDTH/HEIGHT = 640/480  # Video resolution
HOOK_KEY = 'space'         # Game control key

# Main Components
1. Camera initialization and setup
2. Hand detection loop
3. Gesture recognition logic
4. Game control mapping
5. Visual feedback system
6. Cleanup and error handling
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.7 or higher
- Webcam (built-in or external)
- Stickman Hook game (browser or standalone)

### Required Libraries

Install the following Python packages:

```bash
pip install opencv-python
pip install cvzone
pip install pyautogui
pip install mediapipe
```

### Quick Start

1. **Clone/Download** this repository
2. **Install dependencies** using the command above
3. **Open Stickman Hook** in your browser or launch the game
4. **Run the controller**:
   ```bash
   python stickmanHook.py
   ```
5. **Position your hand** in front of the camera
6. **Start playing** with gestures!

## 🎮 Usage Instructions

### Setup

1. Ensure good lighting for optimal hand detection
2. Position camera at comfortable distance (arm's length)
3. Keep background relatively clear
4. Launch Stickman Hook game first
5. Run the gesture controller script

### Playing

1. **Starting**: Show two or more fingers to begin hooking
2. **Swinging**: Keep two+ fingers visible to maintain hook
3. **Releasing**: Show one finger or make a fist to release and fly
4. **Timing**: Practice timing for smooth gameplay

### Controls

- **'q'**: Quit the application
- **'r'**: Reset controller state
- **Mouse to top-left**: Emergency stop (PyAutoGUI failsafe)

## 🔧 Customization Options

### Sensitivity Adjustment

```python
DETECTION_CONFIDENCE = 0.8  # Higher = more strict detection
```

### Control Mapping

```python
HOOK_KEY = 'space'  # Change to any key for different games
```

### Camera Settings

```python
CAMERA_WIDTH = 640   # Adjust resolution
CAMERA_HEIGHT = 480  # for performance/quality balance
```

## 🎯 Performance Tips

1. **Lighting**: Ensure good, even lighting on your hands
2. **Background**: Use a contrasting background for better detection
3. **Distance**: Maintain consistent distance from camera
4. **Stability**: Keep hand movements smooth and deliberate
5. **Calibration**: Restart if detection becomes inaccurate

## 🐛 Troubleshooting

### Common Issues

**Camera not detected:**

- Check camera permissions
- Ensure no other applications are using the camera
- Try different camera indices (0, 1, 2...)

**Poor hand detection:**

- Improve lighting conditions
- Clean camera lens
- Adjust `DETECTION_CONFIDENCE` value
- Ensure hands are visible and unobstructed

**Game not responding:**

- Ensure Stickman Hook game window is active
- Check if spacebar is the correct control key
- Disable other input software that might interfere

**High CPU usage:**

- Reduce camera resolution
- Lower frame rate
- Close unnecessary applications

## 🤝 Contributing

Feel free to contribute improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🙏 Acknowledgments

- **CVZone**: For the excellent hand tracking module
- **MediaPipe**: For robust hand detection algorithms
- **OpenCV**: For computer vision capabilities
- **Stickman Hook**: For the entertaining game that inspired this project
- **Claude Sonnet**: For writing this README

---

**Created by**: Muneer Alam
**Project**: AIML Club Assignment - Build Day (Gesture Control Gaming)  
**Date**: September 2025

_Have fun playing Stickman Hook with gestures! 🎮✋_
