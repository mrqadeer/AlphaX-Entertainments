import pathlib
import streamlit as st
from typing import Optional
from components.input_components import get_video_prompt
from helpers.utils import save_video
from src.video_processing import extract_frames, combine_frames_in_grid


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
                combine_frames_in_grid(frames, combined_image_path)
                
                # Optionally, display the combined image
                with st.expander("Combined Frames Preview:"):
                    st.image(combined_image_path, use_column_width=True)
        
        except Exception as e:
            st.error(f"An error occurred during video processing: {e}")
