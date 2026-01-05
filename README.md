# Air Canvas - AI-Powered Touch-Free Drawing

Air Canvas is an innovative computer vision application that enables touch-free drawing using hand gestures. Using your webcam and AI-powered hand tracking, you can draw in the air, change colors, and control the canvas without any physical contact.

## Features

- **Touch-free Drawing**: Draw in the air using your index finger
- **Gesture Controls**: Control the application using simple hand gestures
- **Multiple Colors**: Switch between Blue, Green, and Red colors
- **Real-time Performance**: Low-latency hand tracking and drawing
- **Clean Interface**: Intuitive visual feedback and instructions

## Tech Stack

- **Python**: Core programming language
- **OpenCV**: Computer vision and video processing
- **MediaPipe**: AI-powered hand tracking
- **NumPy**: Mathematical operations and array handling

## Installation

1. **Clone or download the project**:
   ```bash
   cd air_canvas
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## How to Use

### Gestures

The application recognizes the following hand gestures:

| Gesture | Action | Description |
|---------|--------|-------------|
| ![Index finger up](https://img.shields.io/badge/1%20finger-Draw-blue) | **Draw Mode** | Raise only your index finger to draw lines |
| ![Two fingers up](https://img.shields.io/badge/2%20fingers-Pause-yellow) | **Pause Drawing** | Raise index and middle fingers to stop drawing |
| ![Three fingers up](https://img.shields.io/badge/3%20fingers-Change%20Color-green) | **Change Color** | Raise any three fingers to cycle through colors |
| ![All fingers up](https://img.shields.io/badge/5%20fingers-Clear%20Canvas-red) | **Clear Canvas** | Raise all five fingers to clear the drawing |

### Getting Started

1. **Position yourself**: Sit about 2-3 feet from your webcam
2. **Ensure good lighting**: Make sure your hand is well-lit
3. **Start drawing**: Raise your index finger and move it to draw
4. **Change colors**: Use the three-finger gesture to cycle through Blue → Green → Red
5. **Clear canvas**: Raise all fingers to start fresh

### Tips for Best Performance

- Keep your hand within the camera frame
- Use deliberate, clear gestures
- Maintain consistent lighting
- Keep background simple for better hand detection
- Hold gestures for a moment to ensure recognition

## Project Structure

```
air_canvas/
├── main.py              # Main application entry point
├── hand_tracker.py      # MediaPipe hand tracking implementation
├── gesture_utils.py     # Gesture recognition logic
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Code Architecture

### HandTracker Class (`hand_tracker.py`)
- Initializes MediaPipe hand tracking model
- Detects and tracks hand landmarks in real-time
- Provides landmark position data

### GestureRecognizer Class (`gesture_utils.py`)
- Analyzes finger positions from landmarks
- Recognizes specific gestures based on finger states
- Returns drawing coordinates

### AirCanvas Class (`main.py`)
- Main application controller
- Manages drawing state and canvas
- Handles gesture processing and UI rendering
- Integrates all components

## System Requirements

- **Python**: 3.7 or higher
- **Webcam**: Any standard USB or built-in camera
- **RAM**: 4GB minimum (8GB recommended)
- **CPU**: Modern multi-core processor
- **OS**: Windows, macOS, or Linux

## Troubleshooting

### Common Issues

**Camera not detected**:
- Ensure your webcam is connected and not used by other applications
- Try changing the camera index in `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`

**Poor hand detection**:
- Improve lighting conditions
- Ensure your hand contrasts well with the background
- Keep your hand within the camera frame

**Laggy performance**:
- Close other applications using the camera
- Reduce video resolution in the code if needed
- Ensure your system meets the minimum requirements

**Gestures not recognized**:
- Hold gestures clearly for 2-3 seconds
- Ensure fingers are fully extended or closed
- Check that your hand is the only hand in frame

## Controls

- **'q' key**: Quit the application
- **Gestures**: All interactions are gesture-based (no keyboard/mouse needed during drawing)

## Future Enhancements

- Support for multiple hands
- More drawing tools (shapes, brushes)
- Save/load drawings
- Customizable colors
- Voice commands integration

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

**Enjoy drawing in the air! 🎨✋**