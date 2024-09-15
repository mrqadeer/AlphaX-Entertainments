# components\input_components.py

import streamlit as st
from streamlit_mic_recorder import speech_to_text
import time


if 'username' not in st.session_state:
    st.session_state['username'] = 'Qadeer'
def get_credentials():
    st.subheader("Enter your credentials")
    cols = st.columns(4)
    with cols[0]: 
        
        username = st.text_input("Username")
    with cols[1]:
        
        google_api_key = st.text_input("GOOGLE_API_KEY", type="password")
    with cols[2]:
        openai_api_key = st.text_input("OPENAI_API_KEY", type="password")
    with cols[3]:
        assymbly_api_key = st.text_input("Assymbly API Key", type="password")
    submit = st.button("Submit")
    if username and google_api_key and openai_api_key and assymbly_api_key and submit:
        # write to .env file
        st.session_state['username'] = username
        with open(".env", "w") as f:
            
            f.write(f"GOOGLE_API_KEY='{google_api_key}'\n")
            f.write(f"OPENAI_API_KEY='{openai_api_key}'\n")
            f.write(f"ASSYMBLY_API_KEY='{assymbly_api_key}'\n")
            st.success("Credentials saved successfully!")
        return True
    else:
        st.error("Please enter all credentials.")
        return False

def get_choice():
    st.markdown("<div class='choice'>Choose an option to get started</div>", unsafe_allow_html=True)
    cols=st.columns([3,6,2.5])
    with cols[1]:
        choice=st.selectbox("Select an option", ("Text", "Image", "Audio", "Video"))
    st.markdown("<div class='rainbow-divider'></div>", unsafe_allow_html=True)
    return choice

def get_text_prompt():
    with st.expander("Dialogue:",expanded=True):
        st.subheader("Enter Dialogue")
        text = st.text_area("Text")
        # submit = st.button("Submit")
        if text:
            
            return text
        else:
            return ''
        
    
def get_image_prompt():
    with st.expander("Image:", expanded=True):
        st.subheader("Enter image URL or Upload an image")
        
        # Rainbow divider (assuming the CSS is defined somewhere)
        st.markdown("<div class='rainbow-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='choice'>Choose an option to get started</div>", unsafe_allow_html=True)
        cols=st.columns([3,6,2.5])
        with cols[1]:
            choice=st.selectbox("Select an option", ("URL", "Upload"),)
        if choice=="URL":
            image_url = st.text_input("Image URL")
            if image_url:
                return image_url, 'url'
            else:
                return '','error'
        else:
            uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
            if uploaded_image:
                return uploaded_image, 'upload'
            else:
                return '','error'
  
def get_audio_prompt():
    with st.expander("Audio:", expanded=True):
        st.subheader("Record an audio or Upload an audio")
        
        st.markdown("<div class='rainbow-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='choice'>Choose an option to get started</div>", unsafe_allow_html=True)
        cols=st.columns([3,6,2.5])
        with cols[1]:
            choice=st.selectbox("Select an option", ("Upload","Record"),)
        if choice=="Record":
            with cols[1]:
                with st.progress(0, text="Recording..."):
                    recorded_text = speech_to_text(
                        language='en',
                        start_prompt="🎙️ Start Recording",
                        stop_prompt="🛑 Stop Recording",
                        just_once=False,
                        use_container_width=False,
                        callback=None,
                        args=(),
                        kwargs={},
                        key=None
                    )
                   
            if recorded_text:
                progress_text = "Getting your dialogue. Please wait."
                my_bar = st.progress(0, text=progress_text)
               
                # Simulate the progress of fetching the dialogue
                for percent_complete in range(1, 101):
                    time.sleep(0.03)  # Simulate processing time
                    my_bar.progress(percent_complete, text=progress_text)
                with st.empty():
                    my_bar.progress(100, text="Successfully fetched your dialogue.")
                st.text_area("Recorded Text", recorded_text)
                return recorded_text, 'recording'
            else:
                return '','error'
        else:
            uploaded_audio = st.file_uploader("Upload an audio", type=["mp3", "wav"])
            if uploaded_audio:
                return uploaded_audio, 'upload'
            else:
                return '','error'
