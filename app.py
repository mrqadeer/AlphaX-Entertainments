import os
import pathlib
import streamlit as st

from components.input_components import (get_credentials,
                                         get_choice,
                                         get_page_choice)

from components.display_components import (display_home_content,
                                           display_html_content)
from src.text_handlers import text_handler



from src.image_handlers import image_handler
from src.audio_handlers import audio_handler
from src.video_handlers import video_handler


# Set the wide layout
st.set_page_config(
    layout="wide", page_title="AlphaX Entertainments", page_icon=":cinema:")

if 'signed_in' not in st.session_state:
    st.session_state['signed_in'] = False

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
    # Ensure it works no matter where it's called from
    file_path = os.path.join(os.path.dirname(__file__), 'static/css', file_name)
    file_path = pathlib.Path(file_path)
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")
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
    st.logo("static/assets/logo/alphax.png")
    st.title("AlphaX Entertainments")
    selected=get_page_choice()
    if selected == "Home":
    
        display_home_content()
        
    elif selected == "Credentials":
        display_html_content(tag='credentials')
        cols = st.columns([4, 3, 2.5])
        with cols[1]:
            submit = st.button("Submit",key="submit")
            if submit:
                if get_credentials():
                    st.session_state['signed_in'] = True

    elif selected == "Try AlphaX":
        if not st.session_state['signed_in']:
            display_html_content(tag='alert')    
            st.stop()
        display_html_content(tag='welcome')
        
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
    
 

    # Footer HTML and CSS
    display_html_content(tag='footer')
    # Hide mainmenu and footer of StreamlitCloud
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)
if __name__ == "__main__":
    main()
