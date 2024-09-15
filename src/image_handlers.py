import ast 
import streamlit as st
from src.api_handlers import get_recommendation_response,get_recognition_response
from components.display_components import display_recongnition_result, display_recommendation_result
from components.input_components import get_image_prompt
from helpers.utils import read_image, download_image, save_image
def image_handler():
    # Get the image prompt (either URL or uploaded file)
    prompt_image, tag = get_image_prompt()

    # Always render the submit button
    submit = st.button("Submit", key="image")

    # Show the image preview based on the input type (URL or upload)
    if tag == 'url':

        image_path = download_image(prompt_image)

    elif tag == 'upload':
        image_path = save_image(prompt_image)

    # Only proceed when submit is clicked and there's a valid image
    if submit:

        with st.expander("Preview"):
            st.image(image_path, use_column_width=True)
        # st.info("TEst")
        try:
            with st.spinner("In progress..."):
                image = read_image(image_path=image_path)
                data = get_recognition_response(
                    input_data=image, input_type="image")
                data = ast.literal_eval(data)
                # st.json(data)
                if 'error' not in data:

                    display_recongnition_result(data)
                    data=get_recommendation_response(str(data))
                    # st.json(data)
                    display_recommendation_result(data)
                    
                else:
                    st.error(
                        "Couldn't process your request. Please try again later.")
        except Exception as e:
            st.error(f"An error occurred: {e}")