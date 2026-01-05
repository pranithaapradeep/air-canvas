import numpy as np

class GestureRecognizer:
    def __init__(self):
        # Finger tip and pip landmark IDs
        self.tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
        self.pip_ids = [3, 6, 10, 14, 18]  # Corresponding PIP joints
    
    def fingers_up(self, landmark_list):
        """Determine which fingers are up based on landmark positions"""
        if len(landmark_list) < 21:
            return []
        
        fingers = []
        
        # Thumb (check x coordinate relative to hand orientation)
        if landmark_list[self.tip_ids[0]][1] < landmark_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Other fingers (check y coordinate - tip above pip joint)
        for i in range(1, 5):
            if landmark_list[self.tip_ids[i]][2] < landmark_list[self.tip_ids[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers
    
    def recognize_gesture(self, landmark_list):
        """Recognize gesture based on finger positions"""
        fingers = self.fingers_up(landmark_list)
        
        if len(fingers) == 0:
            return "none"
        
        fingers_up_count = sum(fingers)
        
        # Index finger up only - Draw mode
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            return "draw"
        
        # Index and middle finger up - Pause mode
        elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            return "pause"
        
        # All fingers up - Clear canvas
        elif fingers_up_count >= 4:
            return "clear"
        
        else:
            return "none"
    
    def get_drawing_point(self, landmark_list):
        """Get the index finger tip position for drawing"""
        if len(landmark_list) > 8:
            return landmark_list[8][1], landmark_list[8][2]  # Index finger tip
        return None, None