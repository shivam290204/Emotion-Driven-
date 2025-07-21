# story_generator.py
# This module selects a story and handles text-to-speech narration.

import random
import pyttsx3
from story_data import STORY_TEMPLATES

class StoryGenerator:
    """
    A class to generate and narrate stories based on emotion.
    """
    def __init__(self):
        """
        Initializes the StoryGenerator and the text-to-speech engine.
        """
        self.story_templates = STORY_TEMPLATES
        try:
            self.tts_engine = pyttsx3.init()
        except Exception as e:
            print(f"Error initializing text-to-speech engine: {e}")
            self.tts_engine = None

    def select_story(self, emotion):
        """
        Selects a random story template based on the detected emotion.

        Args:
            emotion (str): The detected emotion (e.g., 'happy', 'sad').

        Returns:
            str: A story string, or a default message if the emotion is not found.
        """
        # Fallback to neutral if the emotion is not in our templates
        if emotion not in self.story_templates:
            emotion = "neutral"
            
        stories = self.story_templates.get(emotion, ["No story found for this mood."])
        return random.choice(stories)

    def narrate_story(self, text):
        """
        Narrates the given text using the text-to-speech engine.

        Args:
            text (str): The text to be spoken.
        """
        if self.tts_engine:
            try:
                # Set properties before speaking
                self.tts_engine.setProperty('rate', 150)  # Speed of speech
                self.tts_engine.setProperty('volume', 0.9) # Volume (0.0 to 1.0)
                
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"Error during narration: {e}")
        else:
            print("Text-to-speech engine not available.")

