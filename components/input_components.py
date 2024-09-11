import streamlit as st

def credentials():
    st.subheader("Enter your credentials")
    cols = st.columns(4)
    with cols[0]: 
        
        username = st.text_input("Username")
    with cols[1]:
        
        claude_api_key = st.text_input("Password", type="password")
    with cols[2]:
        groq_api_key = st.text_input("Groq API Key", type="password")
    with cols[3]:
        assymbly_api_key = st.text_input("Assymbly API Key", type="password")
    submit = st.button("Submit")
    if username and claude_api_key and groq_api_key and assymbly_api_key:
        if submit:
            st.success("Credentials saved successfully!")
            return username, claude_api_key, groq_api_key, assymbly_api_key
    else:
        return "", "", "", ""
    
