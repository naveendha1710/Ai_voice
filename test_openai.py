"""
Test OpenAI API connectivity
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_openai_connection():
    """Test OpenAI API connection and verify it's working."""
    
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("[ERROR] No OpenAI API key found in .env file")
        print("Please add your API key to the .env file:")
        print("OPENAI_API_KEY=your_key_here")
        return False
    
    print(f"[SUCCESS] API key found: {api_key[:5]}...{api_key[-4:]}")
    
    try:
        print("[INFO] Testing API connection...")
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=10
        )
        
        # Print response details
        print("\n[SUCCESS] API connection successful!")
        print(f"Model: {response.model}")
        print(f"Response: {response.choices[0].message.content}")
        print(f"Tokens used: {response.usage.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] API connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("OpenAI API Connection Test")
    print("=" * 40)
    
    if test_openai_connection():
        print("\n[SUCCESS] Your OpenAI integration is working correctly!")
    else:
        print("\n[ERROR] OpenAI integration has issues. Please check your API key and internet connection.")