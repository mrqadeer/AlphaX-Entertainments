import pathlib
import ast
import streamlit as st
from typing import Optional
from components.input_components import get_video_prompt
from helpers.utils import save_video
from src.video_processing import extract_frames, combine_frames_in_grid
from helpers.utils import read_image
from components.display_components import display_recognition_result, display_recommendation_result
from src.api_handlers import get_recognition_response, get_recommendation_response
def video_handler() -> None:
    """
    Handle video input, extract frames, and combine them into a grid.
    
    This function gets a video file from the user, processes it to extract frames, 
    and combines those frames into a grid layout. The combined image is then saved to the specified path.
    """
    # Get the video prompt (either via URL or uploaded file)
    uploaded_file: Optional[st.uploaded_file_manager.UploadedFile] = get_video_prompt()
    
    if uploaded_file is None:
        st.warning("Please upload a video.")
        st.stop()

    # Preview the uploaded video
    with st.expander("Preview:"):
        st.video(uploaded_file)
    
    # Submit button to process the video
    submit: bool = st.button("Submit")
    
    if submit:
        try:
            with st.spinner("In progress..."):
                # Save the uploaded video to the file system
                video_path: str = save_video(uploaded_file)
                
                # Extract frames from the video
                frames = extract_frames(video_path)
                
                # Define the output directory for images
                output_path = pathlib.Path('data/images')
                output_path.mkdir(parents=True, exist_ok=True)
                
                # Define the combined image path
                combined_image_path = output_path / 'combined.png'
                
                # Combine the frames into a grid and save the result
                image_path=combine_frames_in_grid(frames, combined_image_path)
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
            st.error(f"An error occurred during video processing: {e}")
