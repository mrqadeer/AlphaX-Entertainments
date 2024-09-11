import streamlit as st
if 'username' not in st.session_state:
    st.session_state['username'] = 'Qadeer'
def get_credentials():
    st.subheader("Enter your credentials")
    cols = st.columns(4)
    with cols[0]: 
        
        username = st.text_input("Username")
    with cols[1]:
        
        google_api_key = st.text_input("GOOGLE_API_KEY", type="password")
    with cols[2]:
        openai_api_key = st.text_input("OPENAI_API_KEY", type="password")
    with cols[3]:
        assymbly_api_key = st.text_input("Assymbly API Key", type="password")
    submit = st.button("Submit")
    if username and google_api_key and openai_api_key and assymbly_api_key and submit:
        # write to .env file
        st.session_state['username'] = username
        with open(".env", "w") as f:
            
            f.write(f"GOOGLE_API_KEY='{google_api_key}'\n")
            f.write(f"OPENAI_API_KEY='{openai_api_key}'\n")
            f.write(f"ASSYMBLY_API_KEY='{assymbly_api_key}'\n")
            st.success("Credentials saved successfully!")
        return True
    else:
        st.error("Please enter all credentials.")
        return False

def get_choice():
    st.markdown("<div class='choice'>Choose an option to get started</div>", unsafe_allow_html=True)
    cols=st.columns([3,6,2.5])
    with cols[1]:
        choice=st.radio("Select an option", ("Text", "Image", "Audio", "Video", "Recording"), horizontal=True)
    st.markdown("<div class='rainbow-divider'></div>", unsafe_allow_html=True)
    return choice

def get_text_prompt():
    with st.expander("Dialogue:",expanded=True):
        st.subheader("Enter Dialogue")
        text = st.text_area("Text")
        # submit = st.button("Submit")
        if text:
            
            return text
        else:
            return ''
        
    
def get_image_prompt():
    with st.expander("Image:", expanded=True):
        st.subheader("Enter image URL or Upload an image")
        # Rainbow divider (assuming the CSS is defined somewhere)
        st.markdown("<div class='rainbow-divider'></div>", unsafe_allow_html=True)
        
        cols = st.columns(2)
        with cols[0]:
            image_url = st.text_input("Image URL",)
        with cols[1]:
            uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        submit = st.button("Submit")
        if submit:
            # Restrict the user from entering both a URL and uploading an image
            if image_url and uploaded_image:
                st.warning("Please either enter an image URL or upload an image, not both.")
                st.stop()
                return 'error','error'
            
            # Check if the user provided an image URL or uploaded an image
            if len(image_url)>1 and (image_url.endswith(".jpg") or image_url.endswith(".png") or image_url.endswith(".jpeg")):
                return image_url,'url'
            else:
                st.info("Please enter a valid image URL or upload an image.")
            
            if uploaded_image:
                # Process the uploaded image
                return uploaded_image,'upload'
            else:
                return 'error','error'
        else:
            return 'error','error'