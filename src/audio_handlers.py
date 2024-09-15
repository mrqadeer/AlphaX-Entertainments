import ast
import streamlit as st
from components.input_components import get_audio_prompt
from src.audio_processing import audio_processing, transcribe_audio_to_text
from src.api_handlers import get_recommendation_response,get_recognition_response
from components.display_components import display_recongnition_result, display_recommendation_result
def audio_handler():
    """
    Handle audio input, either via URL or upload.
    Displays a preview after the user submits the form.
    """
    
    # Get the audio prompt (either URL or uploaded file)
    prompt_audio, tag = get_audio_prompt()

    # Render the submit button
    submit = st.button("Submit", key="audio")

    # Only proceed if submit button is clicked and there's valid audio input
    if submit:
        # Show the audio preview based on the input type (URL or upload)
        if tag == 'recording':
            audio_text = prompt_audio
        
        elif tag == 'upload':
            with st.expander("Preview Audio"):
                st.audio(prompt_audio, format="audio/wav", start_time=0)

            # Optionally process the audio file
            with st.spinner("Processing audio..."):
                try:
                    audio_path = audio_processing(prompt_audio)
                    audio_text = transcribe_audio_to_text(audio_path)
                    st.text_area("Transcribed Text", audio_text,disabled=True)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    raise e
            
           
            
        # Proceed with any further audio processing
        try:
            with st.spinner("In progress..."):
                data = get_recognition_response(
                    input_data=audio_text, input_type="dialogue")
                data = ast.literal_eval(data)
                if 'error' not in data:

                    display_recongnition_result(data)
                    data=get_recommendation_response(str(data))
                    display_recommendation_result(data)
                else:
                    st.error(data.get('error','Please try again with a different dialogue.'))
            # Add your logic for recognition and recommendation here
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

