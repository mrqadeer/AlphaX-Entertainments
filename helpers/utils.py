import requests
import os
import base64
import pathlib
import streamlit as st
from bs4 import BeautifulSoup
from PIL import Image

# Constants
IMAGE_SAVE_FOLDER = 'data/images'
VIDEO_SAVE_FOLDER = 'data/video'
AUDIO_SAVE_FOLDER = 'data/audio'
DEFAULT_IMAGE = pathlib.Path(IMAGE_SAVE_FOLDER, 'default.png')

# Function to ensure directories exist
def ensure_directories()->None:
    """
    Ensure that the directories for saving images and videos exist.

    This function makes sure that the directories specified in the
    constants IMAGE_SAVE_FOLDER and VIDEO_SAVE_FOLDER exist. If they do
    not exist, they are created.

    Parameters
    ----------
    None

    Returns
    -------
    None
    Example:
        >>> ensure_directories()
        # Directories are created if they don't exist
    """
    pathlib.Path(IMAGE_SAVE_FOLDER).mkdir(parents=True, exist_ok=True)
    pathlib.Path(VIDEO_SAVE_FOLDER).mkdir(parents=True, exist_ok=True)

# Function to save an uploaded image
def save_image(uploaded_image):
    """
    Save an uploaded image to the server.

    This function saves the provided image file to a predefined folder.

    Args:
        uploaded_image (UploadedFile): The image file to be saved.

    Returns:
        str: The path to the saved image.

    Example:
        >>> save_image(uploaded_image)
        'data/images/uploaded_image.png'
    """
    ensure_directories()
    image_path = os.path.join(IMAGE_SAVE_FOLDER, uploaded_image.name)
    image = Image.open(uploaded_image)
    image.save(image_path)
    return str(pathlib.Path(image_path))

# Function to save an uploaded video
def save_video(uploaded_file):
    """
    Save an uploaded video to the server.

    This function saves the provided video file to a predefined folder.

    Args:
        uploaded_file (UploadedFile): The video file to be saved.

    Returns:
        str: The path to the saved video, or None if an error occurred.

    Example:
        >>> save_video(uploaded_file)
        'data/video/uploaded_video.mp4'
    """
    ensure_directories()
    video_path = pathlib.Path(VIDEO_SAVE_FOLDER, uploaded_file.name)
    try:
        with open(video_path, 'wb') as f:
            f.write(uploaded_file.read())
        return str(video_path)
    except Exception as e:
        st.error(f"Error processing video: {str(e)}")
        return None
def save_audio(audio_bytes):
    """
    Save an uploaded audio file to the server.

    This function saves the provided audio file to a predefined folder.

    Args:
        audio_bytes (UploadedFile): The audio file to be saved.

    Returns:
        str: The path to the saved audio, or None if an error occurred.

    Example:
        >>> save_audio(audio_bytes)
        'data/audio/uploaded_audio.mp3'
    """
    ensure_directories()
    audio_path = pathlib.Path(AUDIO_SAVE_FOLDER, 'uploaded_audio.mp3')
    try:
        with open(audio_path, 'wb') as f:
            f.write(audio_bytes)
        return str(audio_path)
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        return None
# Function to download an image from a URL
def download_image(url):
    """
    Download an image from a URL and save it to the server.

    This function downloads an image from the specified URL and saves it to a
    predefined folder. If the download fails, a default image is used.

    Args:
        url (str): The URL of the image to download.

    Returns:
        str: The path to the saved image, or the path to the default image if an error occurred.

    Example:
        >>> download_image("https://example.com/image.png")
        'data/images/downloaded.png'
    """
    ensure_directories()
    image_path = os.path.join(IMAGE_SAVE_FOLDER, 'downloaded.png')
    try:
        response = requests.get(url, headers=HEADERS, stream=True)
        response.raise_for_status()  # Raises an error on a bad status
        with open(image_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return str(pathlib.Path(image_path))
    except requests.RequestException as e:
        st.error(f"Failed to download {url}: {e}")
        st.stop()
        return str(DEFAULT_IMAGE)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.stop()
        return str(DEFAULT_IMAGE)

# Function to get the image URL from IMDb
def get_image_url(imdb_url):
    """
    Retrieve the image URL from an IMDb page.

    This function extracts the URL of the image from the IMDb page specified by
    the provided URL. If the extraction fails, a default image path is returned.

    Args:
        imdb_url (str): The URL of the IMDb page to retrieve the image from.

    Returns:
        str: The URL of the image, or the path to the default image if an error occurred.

    Example:
        >>> get_image_url("https://www.imdb.com/title/tt1234567/")
        'https://example.com/image.png'
    """
    try:
        response = requests.get(imdb_url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        img_tag = soup.select_one('div.ipc-media.ipc-media--poster-27x40.ipc-image-media-ratio--poster-27x40 img')
        img_url = img_tag.get('src') or img_tag.get('data-src') or img_tag.get('data-lazy')
        return img_url if img_url else str(DEFAULT_IMAGE)
    except (requests.RequestException, AttributeError) as e:
        st.error(f"Failed to retrieve image from {imdb_url}: {e}")
        return str(DEFAULT_IMAGE)

# Function to read an image and encode it in base64
def read_image(image_path):
    """
    Read an image file and encode it in base64.

    This function reads an image file from the specified path and encodes it as
    a base64 string.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The base64 encoded image data.

    Raises:
        FileNotFoundError: If the image file does not exist.
        Exception: For other errors encountered while reading the file.

    Example:
        >>> read_image("data/images/sample.png")
        'iVBORw0KGgoAAAANSUhEUgAAAAUA...'
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The file at {image_path} does not exist.")
    try:
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
            return image_data
    except Exception as e:
        raise e  # Let the exception propagate for debugging

# Function to validate the size of an audio file
def validate_audio_file(uploaded_file)->bool:
    """
    Validate the size of an uploaded audio file.

    This function checks if the size of the uploaded audio file is within the
    allowed limit (4 MB).

    Args:
        uploaded_file (st.uploaded_file_manager.UploadedFile): The uploaded audio file.

    Returns:
        bool: True if the file size is less than or equal to 4 MB, False otherwise.

    Example:
        >>> validate_audio_file(uploaded_file)
        True
    """
    
    file_size_mb = uploaded_file.size / (1024 * 1024)  # Convert bytes to MB
    max_size_mb = 4  # Set maximum file size to 4 MB
    return file_size_mb <= max_size_mb

# Headers for web requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

if __name__ == "__main__":
    # Example usage
    path = 'data/images/downloaded.png'
    try:
        print(read_image(path))
    except Exception as e:
        print(f"Error: {e}")
