def save_credentials(api_key: str)->bool:
    """
    Save API credentials to a file.

    This function writes the provided API key to a `.env` file, setting the key
    for OpenAI API access.

    Args:
        api_key (str): The API key/token to save.

    Returns:
        bool: True if the credentials were saved successfully, False otherwise.

    Example:
        >>> save_credentials("your_api_key_here")
        True
    """
    try:
        with open('.env', 'w') as file:
            file.write(f"OPENAI_API_KEY='{api_key}'")
    except Exception as e:
        raise e
    return True