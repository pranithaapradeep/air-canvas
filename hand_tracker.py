import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
    
    def find_hands(self, img, draw=True):
        """Detect hands in the image and return processed image with landmarks"""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        
        return img
    
    def find_position(self, img, hand_no=0):
        """Get landmark positions for the specified hand"""
        landmark_list = []
        
        if self.results.multi_hand_landmarks:
            if len(self.results.multi_hand_landmarks) > hand_no:
                hand = self.results.multi_hand_landmarks[hand_no]
                
                for id, landmark in enumerate(hand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    landmark_list.append([id, cx, cy])
        
        return landmark_list