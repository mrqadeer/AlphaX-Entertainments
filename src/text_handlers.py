# src\text_handlers.py
import ast
import streamlit as st

from src.api_handlers import get_recognition_response,get_recommendation_response
from components.display_components import display_recongnition_result, display_recommendation_result
from components.input_components import get_text_prompt
def text_handler():
    dialogue = get_text_prompt()
    submit = st.button("Submit")
    if len(dialogue) > 0 and submit:
        # st.write(dialogue)
        try:

            with st.spinner("In progress..."):
                data = get_recognition_response(
                    input_data=dialogue, input_type="dialogue")
                data = ast.literal_eval(data)
                if 'error' not in data:
                    # st.info('In progress...')

                    display_recongnition_result(data)
                    
                    data=get_recommendation_response(str(data))
                    # st.json(data)
                    display_recommendation_result(data)
                else:
                    st.error(data.get('error','Please try again with a different dialogue.'))
                # Display recommendations in a 2x5 grid
        except Exception:
            pass