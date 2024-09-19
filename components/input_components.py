import streamlit as st
import time
from streamlit_mic_recorder import speech_to_text
from typing import Tuple, Union, Optional
from helpers.save_credentials import save_credentials

# Initialize session state if not already set
if 'username' not in st.session_state:
    st.session_state['username'] = 'Qadeer'
if 'openai_api_key' not in st.session_state:
    st.session_state['openai_api_key'] = None
if 'signed_in' not in st.session_state:
    st.session_state['signed_in'] = False
@st.dialog("Sign In to get touch in AlphaX Entertainments")
def get_credentials() -> bool:
    """
    Get API credentials from the user and save them to a .env file.

    Returns:
        bool: True if credentials were successfully saved, False otherwise.
    """
    
    
    st.session_state['username'] = st.text_input("Username")
    st.session_state['openai_api_key'] = st.text_input("OPENAI_API_KEY", type="password")
    
    
    
    if st.session_state['username'] and st.session_state['openai_api_key'] :
        st.session_state['signed_in'] = True
    else:
        st.session_state['signed_in'] = False
    cols=st.columns([5, 4.5, 3])
    with cols[1]:
        submit = st.button("Submit", disabled=not st.session_state['signed_in'], key="sign_in")
    if submit:
        if save_credentials(st.session_state['openai_api_key']):
            st.success(f"Nice to have you {st.session_state['username'].title()}!")
        else:
            st.error("Error saving credentials.")

    return st.session_state['signed_in']

def get_choice() -> str:
    """
    Display options for the user to choose from and return the selected option.

    Returns:
        str: The selected option.
    """
    st.markdown("<div class='choice'>Choose an option to get started</div>", unsafe_allow_html=True)
    cols = st.columns([3, 6, 2.5])
    
    with cols[1]:
        choice = st.selectbox("Select an option", ("Text", "Image", "Audio", "Video"))
    
    st.markdown("<div class='rainbow-divider'></div>", unsafe_allow_html=True)
    return choice


def get_text_prompt() -> str:
    """
    Get text input from the user.

    Returns:
        str: The entered text.
    """
    with st.expander("Dialogue:", expanded=True):
        st.subheader("Enter Dialogue")
        text = st.text_area("Text")
        return text if text else ''


def get_image_prompt() -> Tuple[Union[str, None], str]:
    """
    Get image URL or uploaded image from the user.

    Returns:
        Tuple[Union[str, None], str]: The image URL or uploaded image file and the input type.
    """
    with st.expander("Image:", expanded=True):
        st.subheader("Enter image URL or Upload an image")
        st.markdown("<div class='rainbow-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='choice'>Choose an option to get started</div>", unsafe_allow_html=True)
        
        cols = st.columns([3, 6, 2.5])
        with cols[1]:
            choice = st.selectbox("Select an option", ("URL", "Upload"))
        
        if choice == "URL":
            image_url = st.text_input("Image URL")
            return (image_url, 'url') if image_url else ('', 'error')
        else:
            uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
            return (uploaded_image, 'upload') if uploaded_image else ('', 'error')


def get_audio_prompt() -> Tuple[Union[str, None], str]:
    """
    Get audio input from the user either by recording or uploading.

    Returns:
        Tuple[Union[str, None], str]: The recorded or uploaded audio and the input type.
    """
    with st.expander("Audio:", expanded=True):
        st.subheader("Record an audio or Upload an audio")
        st.markdown("<div class='rainbow-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='choice'>Choose an option to get started</div>", unsafe_allow_html=True)
        
        cols = st.columns([3, 6, 2.5])
        with cols[1]:
            choice = st.selectbox("Select an option", ("Upload", "Record"))
        
        if choice == "Record":
            with st.progress(0, text="Recording..."):
                recorded_text = speech_to_text(
                    language='en',
                    start_prompt="🎙️ Start Recording",
                    stop_prompt="🛑 Stop Recording",
                    just_once=False,
                    use_container_width=False
                )
            
            if recorded_text:
                progress_text = "Getting your dialogue. Please wait."
                my_bar = st.progress(0, text=progress_text)
                
                for percent_complete in range(1, 101):
                    time.sleep(0.03)  # Simulate processing time
                    my_bar.progress(percent_complete, text=progress_text)
                
                st.text_area("Recorded Text", recorded_text)
                return recorded_text, 'recording'
            else:
                return '', 'error'
        else:
            uploaded_audio = st.file_uploader("Upload an audio", type=["mp3", "wav"])
            return (uploaded_audio, 'upload') if uploaded_audio else ('', 'error')


def get_video_prompt() -> Optional[bytes]:
    """
    Get a video file uploaded by the user.

    Returns:
        Optional[bytes]: The uploaded video file or None if no file was uploaded.
    """
    with st.expander("Video:", expanded=True):
        st.subheader("Upload Video")
        st.markdown("<div class='rainbow-divider'></div>", unsafe_allow_html=True)
        
        cols = st.columns([3, 6, 2.5])
        with cols[1]:
            uploaded_video = st.file_uploader("Upload a video", type=["mp4", "mkv"])
        
        return uploaded_video
