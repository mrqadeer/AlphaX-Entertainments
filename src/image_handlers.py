import ast
import streamlit as st
from typing import Optional, Tuple
from src.api_handlers import get_recommendation_response, get_recognition_response
from components.display_components import display_recognition_result, display_recommendation_result
from components.input_components import get_image_prompt
from helpers.utils import read_image, download_image, save_image


def image_handler() -> None:
    """
    Handle image input, process it for recognition and recommendation, and display the results.

    This function gets an image prompt from the user (either via URL or upload), processes the image, 
    and sends it to the recognition and recommendation APIs to retrieve and display results.

    It displays a preview of the image and handles any errors during the recognition and recommendation processes.
    """
    # Get the image prompt (either URL or uploaded file)
    prompt_image, tag = get_image_prompt()
    cols=st.columns([5, 6, 2.5], gap="medium")
    with cols[1]:
        # Always render the submit button
        submit: bool = st.button("Submit", key="image")

    # Show the image preview based on the input type (URL or upload)
    image_path: Optional[str] = None
    if tag == 'url':
        image_path = download_image(prompt_image)
    elif tag == 'upload':
        image_path = save_image(prompt_image)

    # Only proceed when submit is clicked and there's a valid image
    if submit and image_path:
        try:
            with st.expander("Preview"):
                st.image(image_path, use_column_width=True)
        except Exception as e:
            st.error(f"Please review your URL if it's valid and try again")
            st.stop()

        try:
            with st.spinner("In progress..."):
                # Read and process the image
                image = read_image(image_path=image_path)
                
                # Get recognition response
                recognition_data = get_recognition_response(input_data=image, input_type="image")
                recognition_data = ast.literal_eval(recognition_data)

                # Check for errors in recognition response
                if 'error' not in recognition_data:
                    display_recognition_result(recognition_data)
                    
                    # Get recommendation response and display it
                    recommendation_data = get_recommendation_response(str(recognition_data))
                    display_recommendation_result(recommendation_data)
                else:
                    st.error("Couldn't process your request. Please try again later.")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
