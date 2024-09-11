import requests
import os
import pathlib
import streamlit as st

# Function to download and save the image


def download_image(image_url):
    # Ensure the folder exists
    save_folder = 'data/images'
    pathlib.Path(save_folder).mkdir(parents=True, exist_ok=True)

    # Get the image content
    try:
        response = requests.get(image_url, stream=True)
    except (requests.ConnectionError,requests.Timeout,requests.HTTPError):
        return None

    # Check if the request was successful
    if response.status_code == 200:
        # Set the full path to save the image
        image_path = os.path.join(save_folder, 'downloaded.png')

        # Open the image file and write the content
        with open(image_path, 'wb') as file:
            file.write(response.content)

        st.info(f"Image downloaded and saved.")
    else:
        st.error(f"Failed to download image. Status code: {response.status_code}")


