# src/text_handlers.py
import ast
import streamlit as st
from typing import Optional

from src.api_handlers import get_recognition_response, get_recommendation_response
from components.display_components import display_recognition_result, display_recommendation_result
from components.input_components import get_text_prompt


def text_handler() -> Optional[None]:
    """
    Handles text input for dialogue recognition and recommendation.

    It processes the dialogue entered by the user, sends it to recognition and recommendation 
    APIs, and displays the results in a grid format.
    """
    dialogue: str = get_text_prompt()

    submit: bool = st.button("Submit")

    if len(dialogue) > 0 and submit:
        try:
            # Display a spinner while the request is processed
            with st.spinner("In progress..."):
                # Fetch recognition response
                data = get_recognition_response(input_data=dialogue, input_type="dialogue")

                try:
                    # Attempt to parse the recognition response into a Python dict
                    data = ast.literal_eval(data)

                    if 'error' not in data:
                        # Display recognition result
                        display_recognition_result(data)

                        # Fetch and display recommendation response based on the recognized data
                        recommendation_data = get_recommendation_response(str(data))
                        display_recommendation_result(recommendation_data)
                    else:
                        st.error(data.get('error', 'Please try again with a different dialogue.'))

                except (ValueError, SyntaxError) as parse_error:
                    st.error(f"Error parsing response data: {parse_error}")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")

        except Exception as e:
            st.error(f"An error occurred while processing the text: {e}")
