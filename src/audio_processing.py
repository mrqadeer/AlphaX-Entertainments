import pathlib
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from typing import Optional
from helpers.utils import validate_audio_file

def audio_processing(uploaded_file) -> Optional[str]:
    """
    Process an uploaded audio file and return its path in WAV format.

    Args:
        uploaded_file (st.uploaded_file_manager.UploadedFile): The uploaded audio file.

    Returns:
        Optional[str]: Path to the processed WAV file or None if an error occurs.
    """
    try:
        # Validate the audio file size
        if not validate_audio_file(uploaded_file):
            st.error("File size is too large. Please upload a smaller file.")
            st.stop()

        # Read audio bytes and create the directory for saving the file
        audio_bytes: bytes = uploaded_file.read()
        path: str = 'data/audio'
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        
        # Set up the file name and extension
        file_name: str = uploaded_file.name
        audio_file_path: pathlib.Path = pathlib.Path(path, file_name)
        get_extension: str = audio_file_path.suffix
        
        # Save the uploaded file
        try:
            with open(audio_file_path, 'wb') as f:
                f.write(audio_bytes)
        except OSError as e:
            st.error(f"File writing error: {e}")
            return None
        
        # Convert MP3 to WAV if necessary
        try:
            if get_extension == '.mp3':
                wav_path: Optional[str] = convert_mp3_to_wav(str(audio_file_path))
            else:
                wav_path = str(audio_file_path)
            return wav_path
        except Exception as e:
            st.error(f"Error converting audio file: {e}")
            return None

    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None


def transcribe_audio_to_text(audio_path: str) -> str:
    """
    Transcribe a WAV audio file to text using Google's Web Speech API.

    Args:
        audio_path (str): Path to the WAV audio file.

    Returns:
        str: Transcribed text or error message if transcription fails.
    """
    recognizer: sr.Recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        # Attempt to transcribe using Google Web Speech API
        try:
            text: str = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Audio could not be transcribed."
        except sr.RequestError as e:
            return f"API request error: {e}"

    except FileNotFoundError:
        return "Audio file not found."
    except OSError as e:
        return f"Error accessing audio file: {e}"
    except Exception as e:
        return f"Unexpected error during transcription: {e}"


def convert_mp3_to_wav(mp3_path: str) -> Optional[str]:
    """
    Convert an MP3 file to WAV format.

    Args:
        mp3_path (str): Path to the MP3 file.

    Returns:
        Optional[str]: Path to the converted WAV file or an error message.
    """
    try:
        # Convert MP3 to WAV
        audio = AudioSegment.from_mp3(mp3_path)
        wav_path: str = mp3_path.replace(".mp3", ".wav")
        audio.export(wav_path, format="wav")
        return wav_path

    except FileNotFoundError:
        st.error("MP3 file not found.")
        return None
    except OSError as e:
        st.error(f"File conversion error: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error during MP3 to WAV conversion: {e}")
        return None
