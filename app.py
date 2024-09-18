import requests
import ast
import streamlit as st
from PIL import Image
from io import BytesIO
from streamlit_option_menu import option_menu
from components.input_components import (get_credentials,
                                         get_choice)

from components.display_components import display_home_content
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
    """Load a CSS file and inject it into the Streamlit app.

    Parameters
    ----------
    file_name : str
        The path to the CSS file to load.

    Returns
    -------
    None
    """
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("static/style.css")
# Main function


def main():

    """
    Main function of the streamlit app. This function renders the main interface of the app.

    The interface has a sidebar with two options: "Home" and "Try Now AlphaX". If the user selects "Home", a form is displayed to enter credentials. If the user selects "Try Now AlphaX", the app displays a subheader with the username and a menu with four options: Text, Image, Audio and Video. Depending on the user's choice, a different handler function is called to process the user's input.

    Args:
        None

    Returns:
        None
    """
    st.title("AlphaX Entertainments")

    with st.sidebar:
        selected = option_menu(
            menu_title='Menu',
            options=["Home","Credentials", "Try Now AlphaX"],
            icons=["house","key", "book"],
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
        display_home_content()
    elif selected == "Credentials":
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
