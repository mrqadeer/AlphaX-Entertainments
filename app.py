import requests
import ast
import streamlit as st
from PIL import Image
from io import BytesIO
from streamlit_option_menu import option_menu
from components.input_components import (get_credentials,
                                         get_choice)


from src.text_handlers import text_handler



from src.image_handlers import image_handler
from src.audio_handlers import audio_handler
from src.video_handlers import video_handler

if 'credential_flag' not in st.session_state:
    st.session_state['credential_flag'] = False

# Set the wide layout
st.set_page_config(
    layout="wide", page_title="AlphaX Entertainments", page_icon=":cinema:")

# Load custom CSS


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("static/style.css")
# Main function


def main():

    st.title("AlphaX Entertainments")

    with st.sidebar:
        selected = option_menu(
            menu_title='Menu',
            options=["Home", "Try Now AlphaX"],
            icons=["house", "book"],
            menu_icon="cast",
            default_index=0,
            styles={
                "menu-title": {"color": 'green', "font-size": "26px"},
                "container": {"padding": "15!important", "background-color": 'black'},
                "icon": {"color": "white ", "font-size": "20px"},
                "nav-link": {"color": "white", "font-size": "20px", 'font-weight': 'bold',
                             "text-align": "left", "margin": "0px",
                             "--hover-color": "magenta"},
                "nav-link-selected": {"background-color": "#02ab21"}
            }
        )

    if selected == "Home":
        if get_credentials():
            st.session_state['credential_flag'] = True

    elif selected == "Try Now AlphaX":
        if not st.session_state['credential_flag']:
            st.subheader(
                "Please enter your credentials to access AlphaX Entertainments")
            st.stop()

        st.subheader(
            f"{st.session_state['username'].title()} Welcome to AlphaX Entertainments")
        st.markdown("<div class='rainbow-divider'></div>",
                    unsafe_allow_html=True)
        choice = get_choice()

        # st.markdown("<div class='rainbow-divider'></div>", unsafe_allow_html=True)
        if choice == "Text":
            text_handler()
        elif choice == "Image":
            image_handler()

        elif choice == "Audio":
            audio_handler()
        elif choice == "Video":
            video_handler()
        else:
            st.write("Please select a valid option")


if __name__ == "__main__":
    main()
