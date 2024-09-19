import os
import ast

import streamlit as st
from typing import Optional, Union, Tuple, List
from langchain_openai.chat_models import ChatOpenAI

from langchain_core.messages import HumanMessage
from prompts.system_prompts import (RECOMMENDATIONS_PROMPT, RECOGNITION_PROMPT)

from openai import (InternalServerError,APIError,ConflictError,
                    RateLimitError,APITimeoutError,BadRequestError,
                    APIConnectionError,AuthenticationError,InternalServerError,PermissionDeniedError,
                    LengthFinishReasonError,UnprocessableEntityError,
                    APIResponseValidationError,ContentFilterFinishReasonError)

# Constants
class LLMHandler:
    def __init__(self, model: str, temperature: float = 0.7, max_tokens: int = 2000, 
                 max_retries: int = 3, timeout: int = 60):
        """
        Initialize an LLMHandler instance with the given model, temperature, max_tokens, max_retries, timeout, and api_key.
        
        Args:
            model (str): The name of the model to use.
            temperature (float): The temperature to use when generating text. Defaults to 0.7.
            max_tokens (int): The maximum number of tokens to generate. Defaults to 2000.
            max_retries (int): The maximum number of retries to make if the API call fails. Defaults to 3.
            timeout (int): The timeout in seconds for the API call. Defaults to 60.
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.timeout = timeout
        self.api_key = st.session_state.get("openai_api_key")
        self.llm_instance = self.get_llm_instance()
        
    def get_llm_instance(self) -> Optional[ChatOpenAI]:
        """
        Create an instance of the Langchain OpenAI chat model with the provided parameters, or return None if an error occurs.
        
        Args:
            None
        
        Returns:
            Optional[ChatOpenAI]: The created LLM instance, or None if an error occurs.
        """
        if not self.api_key:
            raise ValueError("API key is missing or not set in the environment.")
        try:
            return ChatOpenAI(
                model_name=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                max_retries=self.max_retries,
                timeout=self.timeout,
                api_key=self.api_key
            )
        except Exception as e:
            st.error(f"Error creating LLM instance: {e}")
            return None
    
    def handle_response(self, messages: List[Tuple[str, str]]) -> str:
        """
        Handle the response from the LLM instance, including any errors that may occur.

        Args:
            messages (List[Tuple[str, str]]): The messages to send to the LLM instance.

        Returns:
            str: The response from the LLM instance, or an error message if an error occurs.

        Raises:
            ValueError: If the LLM instance is not created.
            Exception: If any other error occurs.
        """
        if not self.llm_instance:
            raise ValueError("LLM instance is not created.")
        try:
            response = self.llm_instance.invoke(messages)
            return response.content.strip().replace("json", "").replace("```", "").replace('\n', '')
        except (AuthenticationError, InternalServerError, RateLimitError, APIConnectionError, APIError) as e:
            self.handle_openai_error(e)
        except Exception as e:
            st.error(f"Error handling response: {e}")
            raise e

    def handle_openai_error(self, error: Exception):
        """
        Handle errors from OpenAI.

        This method handles errors that occur when invoking the LLM instance.
        It displays an error message to the user based on the type of error that occurred.

        Args:
            error (Exception): The error that occurred.

        Raises:
            ValueError: If the LLM instance is not created.
        """
        if isinstance(error, AuthenticationError):
            st.error("Authentication Error: Invalid API Key or authentication issue.")
        elif isinstance(error, BadRequestError):
            st.error("Bad Request Error: Your request is invalid.")
        elif isinstance(error, APIConnectionError):
            st.error("API Connection Error: Failed to connect to the API.")
        elif isinstance(error, RateLimitError):
            st.error("Rate Limit Error: You have exceeded your rate limit.")
        elif isinstance(error, APITimeoutError):
            st.error("API Timeout Error: The request timed out.")
        elif isinstance(error, InternalServerError):
            st.error("Internal Server Error: Something went wrong on OpenAI's side.")
        elif isinstance(error, ConflictError):
            st.error("Conflict Error: The request conflicts with the current state.")

        elif isinstance(error, PermissionDeniedError):
            st.error("Permission Denied Error: You do not have permission to perform this action.")
        elif isinstance(error, LengthFinishReasonError):
            st.error("Length Finish Reason Error: The completion length exceeded the limit.")
        elif isinstance(error, UnprocessableEntityError):
            st.error("Unprocessable Entity Error: The request is well-formed but unable to be processed.")
        elif isinstance(error, APIResponseValidationError):
            st.error("API Response Validation Error: The response from the API did not match the expected format.")
        elif isinstance(error, ContentFilterFinishReasonError):
            st.error("Content Filter Finish Reason Error: The content was filtered out by the API.")
        else:
            st.error(f"Unhandled OpenAI error: {error}")
class RecognitionHandler(LLMHandler):
    def __init__(self, model: str = "gpt-4o", **kwargs):
        """
        Initialize the RecognitionHandler.

        Args:
            model (str, optional): The model to use. Defaults to "gpt-4o".
            **kwargs: Additional keyword arguments to pass to the parent class.
        """
        super().__init__(model=model, **kwargs)
    
    def get_dialogue_response(self, dialogue: str) -> str:
        """
        Get the response from the LLM given a dialogue.

        Args:
            dialogue (str): The dialogue to get the response for.

        Returns:
            str: The response from the LLM.
        """
        messages = [("system", RECOGNITION_PROMPT), ("human", dialogue)]
        return self.handle_response(messages)
    
    def get_image_response(self, image_data: str) -> str:
        message = HumanMessage(
            content=[
                {"type": "text", "text": RECOGNITION_PROMPT},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]
        )
        return self.handle_response([message])

class RecommendationHandler(LLMHandler):
    def __init__(self, model: str = "gpt-4o", **kwargs):
        """
        Initialize a RecommendationHandler instance.

        Args:
            model (str, optional): The name of the LLM model to use. Defaults to "gpt-4o".
            **kwargs: Additional keyword arguments to pass to the LLMHandler constructor.
        """

        super().__init__(model=model, **kwargs)
    
    def get_recommendation_response(self, input_data: str) -> dict:
        """
        Get a recommendation response for a given input.

        Args:
            input_data (str): The input data to generate recommendations for.

        Returns:
            dict: The recommendation response in JSON format.

        Raises:
            Exception: If there is an error parsing the recommendations response.
        """
        
        messages = [("system", RECOMMENDATIONS_PROMPT), ("human", input_data)]
        response_str = self.handle_response(messages)
        try:
            return ast.literal_eval(response_str)
        except Exception as e:
            st.error(f"Error parsing recommendations response: {e}")
            raise e

# Usage examples
def get_recognition_response(input_data: str, input_type: str = "dialogue") -> Optional[str]:
    """
    Get a recognition response for a given input.

    Args:
        input_data (str): The input data to generate recognition for.
        input_type (str, optional): The type of input data. Defaults to "dialogue".

    Returns:
        Optional[str]: The recognition response in JSON format, or None if there is an error.

    Raises:
        Exception: If there is an error generating recognition response.
    """
    try:
        handler = RecognitionHandler()
        if input_type == "dialogue":
            return handler.get_dialogue_response(input_data)
        elif input_type == "image":
            return handler.get_image_response(input_data)
        else:
            st.error("Invalid input type provided.")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def get_recommendation_response(input_data: str) -> Optional[dict]:
    """
    Get a recommendation response for a given input.

    Args:
        input_data (str): The input data to generate recommendations for.

    Returns:
        Optional[dict]: The recommendation response in JSON format, or None if there is an error.

    Raises:
        Exception: If there is an error generating recommendations response.
    """
    try:
        handler = RecommendationHandler()
        return handler.get_recommendation_response(input_data)
    except Exception as e:
        st.error(f"Error: {e}")
        return None
