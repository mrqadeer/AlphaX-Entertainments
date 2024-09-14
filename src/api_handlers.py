

import os
import ast
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai.chat_models import ChatOpenAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from langchain_core.messages import HumanMessage
from google.generativeai.types.safety_types import HarmBlockThreshold, HarmCategory

from prompts.system_prompts import RECOMMENDATIONS_PROMPT,RECOGNITION_PROMPT
# Function to get the specific LLM model
from dotenv import load_dotenv
load_dotenv()
def get_llm_instance(model="gemini-1.5-pro", max_tokens=4000):
    try:
        safety_settings = {
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            }
        # Get the API key directly from the environment variable
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            raise ValueError("API key is missing or not set in the environment.")
        
        # Pass the API key directly to the ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(model=model, max_tokens=max_tokens, api_key=api_key, safety_settings=safety_settings,
                                     temperature=0.7)
        return llm
    except ChatGoogleGenerativeAIError as e:
        st.error(f"Error: {e}")
        raise e
    except Exception as e:
        st.error(f"Error: {e}")
        raise e
# def get_llm_instance(model="gpt-4o", max_tokens=4000):
#     try:
#         safety_settings = {
#                 HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
#                 HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
#                 HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
#                 HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
#             }
#         # Get the API key directly from the environment variable
        
#         # Pass the API key directly to the ChatGoogleGenerativeAI
#         llm = ChatOpenAI(temperature=0.5, model_name="gpt-4o", max_tokens=4000,api_key=os.environ["OPENAI_API_KEY"])
#         return llm
#     # except ChatGoogleGenerativeAIError as e:
#     #     st.error(f"Error: {e}")
#     #     raise e
#     except Exception as e:
#         st.error(f"Error: {e}")
#         raise e

# # Function to handle dialogue LLM responses
def get_dialogue_llm_response(llm, dialogue:str):
    try:
        messages = [("system", RECOGNITION_PROMPT), ("human", dialogue)]
        response = llm.invoke(messages)
        
        # Parse and clean up the response
        response = response.content.strip().replace("json", "").replace("```", "").replace('\n', '')
        # Optionally parse as JSON if needed
        # response = ast.literal_eval(response)
        
        return response
    except ChatGoogleGenerativeAIError as e:
        # st.error("You are running out of credits. Check you qouta")
        st.error(f"Error: {e}")
        
        raise e
        
    except Exception as e:
        st.error(f"Error: {e}")
        raise e

# Function to handle image-based LLM responses
def get_image_llm_response(llm, image_data:str):
    
    try:
        message = HumanMessage(
        content=[
            {"type": "text", "text": RECOGNITION_PROMPT},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ],
    )
        response = llm.invoke([message])
        
        # Parse and clean up the response
        response = response.content.strip().replace("json", "").replace("```", "").replace('\n', '')
        # Optionally parse as JSON if needed
        # response = ast.literal_eval(response)
        
        return response
    except ChatGoogleGenerativeAIError as e:
        # st.error("You are running out of credits. Check you qouta")
        st.error(f"Error: {e}")
        
        raise e
        
    except Exception as e:
        st.error(f"Error: {e}")
        raise e

# Main function to handle LLM response based on input type
def get_recognition_response(input_data, input_type="dialogue"):
    # Get the LLM instance (can be expanded to dynamically choose models if needed)
    llm = get_llm_instance()
    
    # Handle response based on the input type
    if input_type == "dialogue":
        return get_dialogue_llm_response(llm, input_data)
    elif input_type == "image":
        return get_image_llm_response(llm, input_data)
    else:
        st.error("Invalid input type provided.")
        return None
def get_recommendation_llm_instance(model="gpt-3.5-turbo", max_tokens=2000):
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("API key is missing or not set in the environment.")
        # Pass the API key directly to the ChatGoogleGenerativeAI
        llm = ChatOpenAI(model_name=model, 
                         max_tokens=max_tokens,
                         temperature=0.5, 
                         api_key=api_key)
        return llm
    
    except Exception as e:
        st.error(f"Error: {e}")
        raise e
    

def get_recommendation_response(input_data:str):
    # st.info("In progress...Recommendations will be displayed here")
    try:
        llm=get_recommendation_llm_instance()
        messages = [("system", RECOMMENDATIONS_PROMPT), ("human", input_data)]
        response=llm.invoke(messages)
        response = ast.literal_eval(response.content.strip())
        return response
    except Exception as e:
        st.error(f"Error: {e}")
        raise e
    