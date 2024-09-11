import requests
import ast
import streamlit as st
from PIL import Image
from io import BytesIO
from streamlit_option_menu import option_menu

from components.input_components import (get_credentials,
                                         get_choice,
                                         get_text_prompt,
                                         get_image_prompt
                                         )
from src.api_handlers import get_llm_response

from components.display_components import display_recongnition_result,display_recommendation_result
if 'credential_flag' not in st.session_state:
    st.session_state['credential_flag'] = False

# Set the wide layout
st.set_page_config(layout="wide", page_title="AlphaX Entertainments", page_icon=":cinema:")

# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css("static/style.css")
# Main function
def main():
    # load_css("static/style.css")  # Path to your CSS file

    st.title("AlphaX Entertainments")

    with st.sidebar:
        selected = option_menu(
            menu_title='Menu',
            options=["Home", "About"],
            icons=["house", "book"],
            menu_icon="cast",
            default_index=0,
                styles={
                    "menu-title":{"color":'green',"font-size": "26px"},
                    "container": {"padding": "15!important", "background-color": 'black'},
                    "icon": {"color": "white ", "font-size": "20px"},
                    "nav-link": {"color": "white", "font-size": "20px",'font-weight':'bold', 
                                 "text-align": "left", "margin": "0px",
                                 "--hover-color": "magenta"},
                    "nav-link-selected": {"background-color": "#02ab21"}
                }
        )
        
    if selected == "Home":
        if get_credentials():
            st.session_state['credential_flag'] = True
            
    elif selected == "About":
        if not st.session_state['credential_flag']:
            st.subheader("Please enter your credentials to access AlphaX Entertainments")
            st.stop()
        
        st.subheader(f"{st.session_state['username'].title()} Welcome to AlphaX Entertainments")
        st.markdown("<div class='rainbow-divider'></div>", unsafe_allow_html=True)
        choice=get_choice()
        
        # st.markdown("<div class='rainbow-divider'></div>", unsafe_allow_html=True)
        if choice=="Text":
            dialogue=get_text_prompt()
            submit=st.button("Submit")
            if len(dialogue)>0 and submit:
               
                with st.spinner("In progress..."):
                    data=get_llm_response(dialogue)
                    data=ast.literal_eval(data)

                    display_recongnition_result(data)
                    display_recommendation_result(data)
                    # Display recommendations in a 2x5 grid
        elif choice=="Image":
            # st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
            prompt_image,tag=get_image_prompt()
            
            if tag=='url':
                
        elif choice=="Audio":
            st.file_uploader("Upload an audio", type=["mp3", "wav"])
            ...
        elif choice=="Video":
            st.file_uploader("Upload a video", type=["mp4", "mov"])
            ...
        elif choice=="Recording":
            st.file_uploader("Upload a recording", type=["mp3", "wav", "mp4", "mov"])
            ...
        else:
            st.write("Please select a valid option")


if __name__ == "__main__":
    main()