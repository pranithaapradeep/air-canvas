import cv2
import numpy as np
from hand_tracker import HandTracker
from gesture_utils import GestureRecognizer

class AirCanvas:
    def __init__(self):
        self.hand_tracker = HandTracker()
        self.gesture_recognizer = GestureRecognizer()
        
        # Drawing variables
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Blue, Green, Red
        self.color_names = ["Blue", "Green", "Red"]
        self.color_index = 0
        self.draw_color = self.colors[self.color_index]
        self.brush_thickness = 8
        
        # Canvas and drawing state
        self.img_canvas = None
        self.xp, self.yp = 0, 0
        self.drawing_mode = False
        
        # Gesture state tracking
        self.prev_gesture = "none"
        self.gesture_counter = 0
        self.gesture_threshold = 3  # Frames to confirm gesture
    
    def setup_canvas(self, width, height):
        """Initialize the drawing canvas"""
        self.img_canvas = np.zeros((height, width, 3), np.uint8)
    
    def change_color(self):
        """Cycle through available colors"""
        self.color_index = (self.color_index + 1) % len(self.colors)
        self.draw_color = self.colors[self.color_index]
    
    def clear_canvas(self):
        """Clear the drawing canvas"""
        if self.img_canvas is not None:
            self.img_canvas[:] = 0
    
    def draw_ui(self, img):
        """Draw UI elements on the image"""
        h, w = img.shape[:2]
        
        # Color selection bar at top
        bar_height = 80
        cv2.rectangle(img, (0, 0), (w, bar_height), (50, 50, 50), cv2.FILLED)
        
        # Draw color options
        color_width = w // len(self.colors)
        for i, (color, name) in enumerate(zip(self.colors, self.color_names)):
            x1 = i * color_width
            x2 = (i + 1) * color_width
            
            # Highlight selected color
            if i == self.color_index:
                cv2.rectangle(img, (x1, 10), (x2, bar_height - 10), color, cv2.FILLED)
                cv2.rectangle(img, (x1, 10), (x2, bar_height - 10), (255, 255, 255), 3)
            else:
                cv2.rectangle(img, (x1 + 10, 20), (x2 - 10, bar_height - 20), color, cv2.FILLED)
            
            # Color name
            text_x = x1 + (color_width - len(name) * 10) // 2
            cv2.putText(img, name, (text_x, bar_height - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Instructions
        instructions = [
            "1 finger: Draw | 2 fingers: Pause | 4+ fingers: Clear | Click colors above"
        ]
        
        cv2.putText(img, instructions[0], (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def handle_color_selection(self, x, y, img_width):
        """Handle color selection from top bar"""
        if y < 80:  # Click in color bar area
            color_width = img_width // len(self.colors)
            selected_color = x // color_width
            if 0 <= selected_color < len(self.colors):
                self.color_index = selected_color
                self.draw_color = self.colors[self.color_index]
    
    def process_gesture(self, gesture, x, y, img_width):
        """Process recognized gesture and update drawing state"""
        if gesture == self.prev_gesture:
            self.gesture_counter += 1
        else:
            self.gesture_counter = 0
            self.prev_gesture = gesture
        
        # Handle color selection
        self.handle_color_selection(x, y, img_width)
        
        # Only act on gesture if it's been consistent for threshold frames
        if self.gesture_counter >= self.gesture_threshold:
            if gesture == "draw" and y > 80:  # Don't draw in color selection area
                self.drawing_mode = True
                if self.xp == 0 and self.yp == 0:
                    self.xp, self.yp = x, y
                
                # Draw line on canvas
                cv2.line(self.img_canvas, (self.xp, self.yp), (x, y), self.draw_color, self.brush_thickness)
                cv2.circle(self.img_canvas, (x, y), self.brush_thickness//2, self.draw_color, cv2.FILLED)
                self.xp, self.yp = x, y
            
            elif gesture == "pause":
                self.drawing_mode = False
                self.xp, self.yp = 0, 0
            
            elif gesture == "clear":
                self.clear_canvas()
                self.drawing_mode = False
                self.xp, self.yp = 0, 0
            
            else:
                self.drawing_mode = False
                self.xp, self.yp = 0, 0
        
        # Reset drawing position if not in drawing mode
        if not self.drawing_mode:
            self.xp, self.yp = 0, 0
    
    def run(self):
        """Main application loop"""
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)  # Width
        cap.set(4, 720)   # Height
        
        print("Air Canvas Started!")
        print("Gestures:")
        print("- 1 finger up: Draw")
        print("- 2 fingers up: Pause")
        print("- 4+ fingers up: Clear canvas")
        print("- Click on colors at the top to change color")
        print("Press 'q' to quit")
        
        while True:
            success, img = cap.read()
            if not success:
                break
            
            img = cv2.flip(img, 1)  # Mirror the image
            
            # Initialize canvas if not done
            if self.img_canvas is None:
                self.setup_canvas(img.shape[1], img.shape[0])
            
            # Find hands
            img = self.hand_tracker.find_hands(img)
            landmark_list = self.hand_tracker.find_position(img)
            
            if len(landmark_list) != 0:
                # Get drawing point (index finger tip)
                x, y = self.gesture_recognizer.get_drawing_point(landmark_list)
                
                if x is not None and y is not None:
                    # Recognize gesture
                    gesture = self.gesture_recognizer.recognize_gesture(landmark_list)
                    
                    # Process the gesture
                    self.process_gesture(gesture, x, y, img.shape[1])
                    
                    # Draw current finger position
                    cv2.circle(img, (x, y), 10, self.draw_color, cv2.FILLED)
            
            # Combine canvas with camera feed
            img_gray = cv2.cvtColor(self.img_canvas, cv2.COLOR_BGR2GRAY)
            _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
            img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
            img = cv2.bitwise_and(img, img_inv)
            img = cv2.bitwise_or(img, self.img_canvas)
            
            # Draw UI
            self.draw_ui(img)
            
            # Display
            cv2.imshow("Air Canvas", img)
            
            # Exit condition
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = AirCanvas()
    app.run()