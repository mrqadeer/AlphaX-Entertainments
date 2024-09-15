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
DEFAULT_IMAGE = pathlib.Path(IMAGE_SAVE_FOLDER, 'default.png')

# Function to ensure directories exist
def ensure_directories():
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
    """
    pathlib.Path(IMAGE_SAVE_FOLDER).mkdir(parents=True, exist_ok=True)
    pathlib.Path(VIDEO_SAVE_FOLDER).mkdir(parents=True, exist_ok=True)

# Function to save an uploaded image
def save_image(uploaded_image):
    """
    Save an uploaded image to the server.

    Parameters
    ----------
    uploaded_image : UploadedFile
        The image to be saved.

    Returns
    -------
    str
        The path to the saved image.
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

    Parameters
    ----------
    uploaded_file : UploadedFile
        The video to be saved.

    Returns
    -------
    str
        The path to the saved video.
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

# Function to download an image from a URL
def download_image(url):
    """
    Download an image from a URL and save it to the server.

    Parameters
    ----------
    url : str
        The URL of the image to download.

    Returns
    -------
    str
        The path to the saved image.
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
    Get the image URL from an IMDb page.

    Parameters
    ----------
    imdb_url : str
        The URL of the IMDb page to retrieve the image from.

    Returns
    -------
    str
        The URL of the image or the default image path if the request fails.
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
    Read an image and encode it in base64.

    Parameters
    ----------
    image_path : str
        The path to the image file.

    Returns
    -------
    str
        The base64 encoded image data.

    Raises
    ------
    FileNotFoundError
        If the image file does not exist.
    Exception
        If there is an error reading the file.
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
def validate_audio_file(uploaded_file):
    """
    Validate the size of an uploaded audio file.

    Parameters
    ----------
    uploaded_file : st.uploaded_file_manager.UploadedFile
        The uploaded audio file.

    Returns
    -------
    bool
        True if the file size is less than or equal to 4 MB, False otherwise.

    Raises
    ------
    ValueError
        If the uploaded file is not an audio file.
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
