import streamlit as st
if 'username' not in st.session_state:
    st.session_state['username'] = 'Qadeer'
def credentials():
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
    
def text_prompt():
    st.subheader("Enter text")
    text = st.text_area("Text")
    # submit = st.button("Submit")
    if text:
        
        return text
    else:
        return ''