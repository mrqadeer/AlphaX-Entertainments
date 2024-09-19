def save_credentials(api_key: str)->bool:
    """
    Save API credentials based on the selected LLM choice.

    Args:
        api_key (str): The API key/token to save.

    Returns:
        bool: True if the credentials were saved successfully.
    """
    try:
        with open('.env', 'w') as file:
            file.write(f"OPENAI_API_KEY='{api_key}'")
    except Exception as e:
        raise e
    return True