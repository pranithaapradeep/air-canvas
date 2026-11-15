
import sys
import threading
from pathlib import Path

import av
import cv2
import streamlit as st
from streamlit_webrtc import (
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)

# Make the original project files importable
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from main import AirCanvas


st.set_page_config(
    page_title="Air Canvas",
    page_icon="🎨",
    layout="wide"
)

st.title("✋ Air Canvas")
st.write("Draw in the air using your hand gestures.")

st.markdown("""
**Controls**
- ☝️ Index finger: Draw
- ✌️ Index + middle fingers: Pause
- 🖐️ Four or more fingers: Clear canvas
- Select a colour using the dropdown below
""")

selected_color = st.selectbox(
    "Choose drawing colour",
    ["Blue", "Green", "Red"]
)


class AirCanvasProcessor(VideoProcessorBase):

    def __init__(self):
        self.canvas = AirCanvas()
        self.lock = threading.Lock()

    def set_color(self, color):
        with self.lock:
            index = self.canvas.color_names.index(color)
            self.canvas.color_index = index
            self.canvas.draw_color = self.canvas.colors[index]

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        # Mirror webcam image
        img = cv2.flip(img, 1)

        height, width = img.shape[:2]

        if self.canvas.img_canvas is None:
            self.canvas.setup_canvas(width, height)

        # Use original hand tracking logic
        img = self.canvas.hand_tracker.find_hands(img)
        landmarks = self.canvas.hand_tracker.find_position(img)

        if len(landmarks) != 0:

            x, y = self.canvas.gesture_recognizer.get_drawing_point(
                landmarks
            )

            if x is not None and y is not None:

                gesture = self.canvas.gesture_recognizer.recognize_gesture(
                    landmarks
                )

                self.canvas.process_gesture(
                    gesture, x, y, width
                )

                cv2.circle(
                    img,
                    (x, y),
                    10,
                    self.canvas.draw_color,
                    cv2.FILLED
                )

        # Combine camera feed with drawing canvas
        gray = cv2.cvtColor(
            self.canvas.img_canvas,
            cv2.COLOR_BGR2GRAY
        )

        _, inverse = cv2.threshold(
            gray, 50, 255, cv2.THRESH_BINARY_INV
        )

        inverse = cv2.cvtColor(
            inverse,
            cv2.COLOR_GRAY2BGR
        )

        img = cv2.bitwise_and(img, inverse)
        img = cv2.bitwise_or(img, self.canvas.img_canvas)

        # Reuse original interface rendering
        self.canvas.draw_ui(img)

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
        )


ctx = webrtc_streamer(
    key="air-canvas",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=AirCanvasProcessor,
    rtc_configuration={
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]}
        ]
    },
    media_stream_constraints={
        "video": True,
        "audio": False
    },
    async_processing=True
)

if ctx.video_processor:
    ctx.video_processor.set_color(selected_color)

st.caption(
    "Allow camera access when prompted. "
    "Use good lighting and keep your hand visible."
)
