
import pathlib
import streamlit as st
import streamlit as st
import speech_recognition as sr

from pydub import AudioSegment
from pydub import AudioSegment



from helpers.utils import validate_audio_file
def audio_processing(uploaded_file):
    # Read audio bytes
    if validate_audio_file(uploaded_file):
            
        audio_bytes = uploaded_file.read()
        path='data/audio'
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        # Set temp filename
        file_name = uploaded_file.name
        audio_file_path = pathlib.Path(path, file_name)
        get_extension = audio_file_path.suffix
        
        try:
            with open(audio_file_path, 'wb') as f:
                f.write(audio_bytes)
                
            
            if get_extension == '.mp3':
                wav_path = convert_mp3_to_wav(audio_file_path)
            else:
                wav_path = audio_file_path
            return str(wav_path)

        except Exception as e:
            st.error(f"Error processing audio: {str(e)}")
            return None

    else:
        st.error("File size is too large. Please upload a smaller file.")
        st.stop()

def transcribe_audio_to_text(audio_path):
    """Transcribe a WAV audio file to text."""
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            # Try to transcribe the audio using Google Web Speech API
            try:
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                st.stop()
                return "Audio could not be transcribed."
            except sr.RequestError:
                st.stop()
                return "API request failed."
    except FileNotFoundError:
        st.stop()
        return "Audio file not found."
    except Exception as e:
        st.stop()
        return f"Error: {e}"

def convert_mp3_to_wav(mp3_path):
    """Convert mp3 file to wav format."""
    # Ensure mp3_path is a string (if pathlib.Path object is passed, convert it to a string)
    if isinstance(mp3_path, pathlib.Path):
        mp3_path = str(mp3_path)

    try:
        audio = AudioSegment.from_mp3(mp3_path)
        wav_path = mp3_path.replace(".mp3", ".wav")
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception as e:
        return f"Error converting mp3 to wav: {e}"