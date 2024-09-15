import pathlib
import cv2
import streamlit as st
from PIL import Image
from typing import List, Optional


def extract_frames(video_path: str, interval: int = 1) -> List[Image.Image]:
    """
    Extract frames from a video file at specified intervals.

    Args:
        video_path (str): Path to the video file.
        interval (int): Interval (in seconds) at which frames are extracted.

    Returns:
        List[Image.Image]: List of frames extracted from the video as PIL Images.
    """
    frames: List[Image.Image] = []

    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Error: Unable to open video file: {video_path}")

        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
        if frame_rate == 0:
            raise ValueError(f"Error: Unable to retrieve frame rate from video: {video_path}")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames == 0:
            raise ValueError(f"Error: Unable to retrieve total frame count from video: {video_path}")

        for i in range(0, total_frames, frame_rate * interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                st.warning(f"Warning: Failed to read frame {i}. Skipping to next frame.")

    except cv2.error as e:
        st.error(f"OpenCV Error: {e}")
    except ValueError as ve:
        st.error(f"Value Error: {ve}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    finally:
        if 'cap' in locals():
            cap.release()

    return frames


def combine_frames_in_grid(frames: List[Image.Image], output_path: str, rows: int = 5, cols: int = 5) -> Optional[str]:
    """
    Combine frames into a grid and save the combined image.

    Args:
        frames (List[Image.Image]): List of frames to combine.
        output_path (str): Path where the combined image will be saved.
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.

    Returns:
        Optional[str]: Path to the saved combined image, or None if an error occurred.
    """
    try:
        if len(frames) == 0:
            raise ValueError("No frames provided to combine.")

        if len(frames) < rows * cols:
            raise ValueError(f"Not enough frames to create a grid. Need {rows * cols}, but got {len(frames)}.")

        frames = frames[:rows * cols]

        frame_height, frame_width, _ = frames[0].shape

        for frame in frames:
            if frame.shape != (frame_height, frame_width, 3):
                raise ValueError("All frames must have the same size and 3 channels (RGB).")

        combined_width = frame_width * cols
        combined_height = frame_height * rows
        combined_image = Image.new('RGB', (combined_width, combined_height))

        for i, frame in enumerate(frames):
            try:
                frame_image = Image.fromarray(frame)
                row = i // cols
                col = i % cols
                combined_image.paste(frame_image, (col * frame_width, row * frame_height))
            except Exception as e:
                st.error(f"Error pasting frame {i} into the grid: {str(e)}")
                return None

        combined_image.save(output_path)
        return str(output_path)

    except ValueError as ve:
        st.error(f"Value Error: {ve}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None
