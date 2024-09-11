import streamlit as st

from components.input_components import credentials
if 'credential_flag' not in st.session_state:
    st.session_state['credential_flag'] = False
import streamlit as st
from streamlit_option_menu import option_menu

# Set the wide layout
st.set_page_config(layout="wide")

# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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
        username, claude_api_key, groq_api_key, assymbly_api_key = credentials()
        if username and claude_api_key and groq_api_key and assymbly_api_key:
            st.session_state['credential_flag'] = True
            
    elif selected == "About":
        if st.session_state['credential_flag'] == True:
            st.subheader("About AlphaX Entertainments")
        else:
            st.subheader("Please enter your credentials to access AlphaX Entertainments")



if __name__ == "__main__":
    main()