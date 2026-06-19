import re
import os
import platform

def clean_text(text):
    """
    Cleans and normalizes text input.
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Cleaned text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_system_info():
    """
    Gets basic system information.
    
    Returns:
        dict: System information
    """
    info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version()
    }
    
    return info

def is_valid_path(path):
    """
    Checks if a file path is valid.
    
    Args:
        path (str): Path to check
        
    Returns:
        bool: True if path is valid, False otherwise
    """
    return os.path.exists(path)