# app.py
# The main Streamlit application for the Emotion-Driven Interactive Storyteller.

import streamlit as st
from emotion_detector import EmotionDetector
from story_generator import StoryGenerator
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Emotion-Driven Storyteller",
    page_icon="🎭",
    layout="centered",
)

# --- Initialize Session State ---
if 'story' not in st.session_state:
    st.session_state.story = ""
if 'emotion' not in st.session_state:
    st.session_state.emotion = ""
if 'scanning' not in st.session_state:
    st.session_state.scanning = False


# --- Main Application ---
def main():
    """
    The main function to run the Streamlit app.
    """
    st.title("🎭 Emotion-Driven Interactive Storyteller")
    st.markdown("---")
    st.write(
        "Welcome! This app uses your webcam to detect your emotion and "
        "generates a short story tailored to your mood. Click the button below to start!"
    )

    # --- Instantiate our main components ---
    emotion_detector = EmotionDetector()
    story_generator = StoryGenerator()

    # --- UI Elements ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start_button = st.button("🎬 Start Emotion Scan", use_container_width=True)

    if start_button:
        st.session_state.scanning = True
        st.session_state.story = ""
        st.session_state.emotion = ""

        with st.spinner("Accessing webcam... Please look at the camera. A new window will open."):
            # A brief pause to allow the user to read the message
            time.sleep(2)
            
            # The webcam scan runs in a separate window managed by OpenCV
            detected_emotion = emotion_detector.start_webcam_scan()

        if detected_emotion:
            st.session_state.emotion = detected_emotion.capitalize()
            st.success(f"Emotion Detected: **{st.session_state.emotion}**!")

            with st.spinner(f"Generating a {st.session_state.emotion.lower()} story for you..."):
                story = story_generator.select_story(detected_emotion)
                st.session_state.story = story
                
                # Narrate the story
                story_generator.narrate_story(story)
        else:
            st.warning("Emotion detection was cancelled or no face was found.")
        
        st.session_state.scanning = False


    # --- Display the generated story ---
    if st.session_state.story:
        st.markdown("---")
        st.subheader(f"A Story for When You're Feeling {st.session_state.emotion}")
        st.info(st.session_state.story)

        # Add a button to replay the audio
        if st.button("🔊 Replay Narration", use_container_width=True):
            with st.spinner("Narrating the story again..."):
                 story_generator.narrate_story(st.session_state.story)


# --- Run the App ---
if __name__ == "__main__":
    main()

