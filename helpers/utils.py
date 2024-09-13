import requests
import os
import base64
import pathlib
import streamlit as st
from bs4 import BeautifulSoup
from PIL import Image

# Function to download and save the image
def save_image(uploaded_image):
    # Ensure the folder exists
    save_folder = 'data/images'
    pathlib.Path(save_folder).mkdir(parents=True, exist_ok=True)
    image_path = os.path.join(save_folder, uploaded_image.name)
    image=Image.open(uploaded_image)
    image.save(image_path)
    return str(pathlib.Path(image_path))
    
def download_image(image_url):
    # Ensure the folder exists
    save_folder = 'data/images'
    pathlib.Path(save_folder).mkdir(parents=True, exist_ok=True)

    # Get the image content
    try:
        response = requests.get(image_url, stream=True)
    except (requests.ConnectionError,requests.Timeout,requests.HTTPError):
        raise e
    except requests.exceptions.MissingSchema:
        # st.error(f"Invalid image URL: {image_url}")
        st.stop()
        raise e
    except Exception as e:
        st.error(f"An error occurred: {e}")
        raise e

    # Check if the request was successful
    if response.status_code == 200:
        # Set the full path to save the image
        image_path = os.path.join(save_folder, 'downloaded.png')

        # Open the image file and write the content
        with open(image_path, 'wb') as file:
            file.write(response.content)

        # st.info(f"Image downloaded and saved.")
    else:
        st.error(f"Failed to download image. Status code: {response.status_code}")
        return None


    return str(pathlib.Path(image_path))

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

def download_image(url):
    # Ensure the folder exists
    save_folder = 'data/images'
    pathlib.Path(save_folder).mkdir(parents=True, exist_ok=True)
    image_path=os.path.join(save_folder, 'downloaded.png')
    try:
        response = requests.get(url, headers=HEADERS, stream=True)
        response.raise_for_status()  # Raises an error on a bad status
        with open(image_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        st.success(f"Image downloaded successfully")
        return str(pathlib.Path(image_path))
    except requests.RequestException as e:
        st.error(f"Failed to download {url}: {e}")
        raise e
    except Exception as e:
        st.error(f"An error occurred: {e}")
        raise e




def get_image_url(imdb_url):

    default_img = pathlib.Path('data/images/default.png')  
    try:
        response = requests.get(imdb_url, headers=HEADERS, timeout=10)  # Added timeout
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Use CSS selector for more reliable and faster searching
        div = soup.select_one('div.ipc-media.ipc-media--poster-27x40.ipc-image-media-ratio--poster-27x40')

        if div:
            # Check for img tag
            img_tag = div.find('img')

            # Handle lazy-loading by checking data attributes
            if img_tag:
                img_url = img_tag.get('src') or img_tag.get('data-src') or img_tag.get('data-lazy')
                if img_url:
                    return img_url
                
        # If no image found, return default image
        return default_img

    except (requests.ConnectionError, requests.HTTPError, requests.Timeout) as e:
        return default_img





def read_image(image_path):
    # Check if file exists first
    # st.write(image_path)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The file at {image_path} does not exist.")

    try:
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
            return image_data
    except Exception as e:
        raise e  # Let the exception propagate for debugging


if __name__ == "__main__":
    path='data/images/downloaded.png'
    print(read_image(path))