# src/audio_handlers.py
import ast
import streamlit as st
from typing import Optional

from helpers.utils import save_audio
from components.input_components import get_audio_prompt
from components.display_components import display_recognition_result, display_recommendation_result
from src.api_handlers import get_recognition_response, get_recommendation_response,get_recognized_text

def audio_handler() -> Optional[None]:
    """
    Handles audio input (either via URL or uploaded file) for dialogue recognition and recommendation.
    
    Displays a preview of the audio file and performs transcription, recognition, and recommendation processing.
    """
    try:
        # Get the audio prompt (either URL or uploaded file)
        prompt_audio, tag = get_audio_prompt()

        if not prompt_audio:
            st.warning("No audio input provided.")
            st.stop()
        cols=st.columns([5, 6, 2.5], gap="medium")
        with cols[1]:
            # Render the submit button
            submit: bool = st.button("Submit", key="audio")

        # Only proceed if the submit button is clicked and valid audio input is available
        if submit:
            with st.expander("Preview Audio"):
                st.audio(prompt_audio, format="audio/wav", start_time=0)
            audio_text: str = ""

            try:
                # Handle audio based on input type (recording or upload)
                if tag == 'recording':
                    # If audio is from recording, assume it's already in text form
                    audio_path=save_audio(prompt_audio)
                    audio_text = prompt_audio

                elif tag == 'upload':
                    audio_bytes=prompt_audio.read()
                    audio_path=save_audio(audio_bytes)
                    
                    
                with st.spinner("Processing audio..."):
                    

                    # Transcribe audio to text
                    audio_text = get_recognized_text(audio_path)
                    if not audio_text:
                        raise ValueError("Transcription failed.")
                    
                    # Display transcribed text
                    st.text_area("Transcribed Text", audio_text, disabled=False)

            except ValueError as ve:
                st.error(f"Value Error: {ve}")
                return
            except Exception as e:
                st.error(f"An error occurred during audio processing: {e}")
                return

            # Proceed with recognition and recommendation
            try:
                with st.spinner("Recognition and recommendation in progress..."):
                    # Perform dialogue recognition
                    data: str = get_recognition_response(input_data=audio_text, input_type="dialogue")
                    data_dict: dict = ast.literal_eval(data)

                    if 'error' not in data_dict:
                        # Display recognition results
                        display_recognition_result(data_dict)

                        # Fetch and display recommendations
                        recommendation_data: str = get_recommendation_response(str(data_dict))
                        display_recommendation_result(recommendation_data)
                    else:
                        st.error(data_dict.get('error', 'Please try again with a different dialogue.'))

            except Exception as e:
                st.error(f"An error occurred during recognition or recommendation: {e}")
                return

    except ValueError as ve:
        st.error(f"{ve}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
