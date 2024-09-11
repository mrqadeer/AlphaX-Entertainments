import os
import ast
import streamlit as st
from prompts.system_prompts import TEXT_DIALOGUE_PROMPT
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai.chat_models import ChatOpenAI
# Initialize the language model
from dotenv import load_dotenv
load_dotenv()
def get_llm_response(dialogue):
    try:
        os.environ["GOOGLE_API_KEY"] =os.getenv("GOOGLE_API_KEY")
    
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-pro",max_tokens=4000)
        
        messages = [("system", TEXT_DIALOGUE_PROMPT), ("human", dialogue)]
        response = llm.invoke(messages)
        # st.write(response)
        # Parse the JSON response from the model
        response = response.content.strip().replace("json", "").replace("```", "").replace('\n','')
        
        # response=ast.literal_eval(response)
        return response
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()