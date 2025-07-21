# emotion_detector.py
# This module handles real-time facial emotion detection using the webcam with DeepFace.

import cv2
from deepface import DeepFace
import numpy as np

class EmotionDetector:
    """
    A class to detect emotions from a live webcam feed using DeepFace.
    """
    def __init__(self):
        """
        Initializes the emotion detector.
        The DeepFace model will be built automatically on the first analysis.
        """
        print("EmotionDetector initialized. Model will be loaded on first scan.")
        pass

    def detect_emotion(self, frame):
        """
        Detects the dominant emotion from a single frame.

        Args:
            frame (numpy.ndarray): The image frame captured from the webcam.

        Returns:
            tuple: A tuple containing the dominant emotion (str) and the frame with
                   emotion text and bounding box drawn on it. Returns (None, frame)
                   if no face is detected.
        """
        try:
            # DeepFace.analyze will build the model on the first run.
            # We set enforce_detection to False to avoid crashing if no face is found.
            analysis = DeepFace.analyze(
                img_path=frame,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend='opencv' # Using opencv backend is often faster
            )

            # analysis can be a list of dicts. We'll take the first one.
            if isinstance(analysis, list) and len(analysis) > 0:
                analysis = analysis[0]

            # Check if a face was detected and emotion analysis was successful
            if 'dominant_emotion' in analysis:
                dominant_emotion = analysis['dominant_emotion']
                face_region = analysis['region']

                # Draw bounding box and text on the frame
                x, y, w, h = face_region['x'], face_region['y'], face_region['w'], face_region['h']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Put the emotion text above the rectangle
                cv2.putText(
                    frame,
                    dominant_emotion,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2,
                )
                return dominant_emotion, frame

        except Exception as e:
            # DeepFace can sometimes raise exceptions if the face is not clear
            # We can print this for debugging, but will otherwise ignore it.
            # print(f"Could not process frame with DeepFace: {e}")
            pass 

        return None, frame

    def start_webcam_scan(self):
        """
        Opens the webcam and scans for emotion until one is confidently detected.

        Returns:
            str: The detected dominant emotion, or None if the scan is cancelled.
        """
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return None

        detected_emotion = None
        
        print("Starting webcam scan... Look at the camera. Press 'q' to quit.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Can't receive frame. Exiting ...")
                break

            frame = cv2.flip(frame, 1)

            emotion, annotated_frame = self.detect_emotion(frame)

            if emotion:
                detected_emotion = emotion
                cv2.imshow('Emotion Scan', annotated_frame)
                cv2.waitKey(1000) # Display for 1 second
                break

            cv2.imshow('Emotion Scan - Press "q" to quit', annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return detected_emotion
