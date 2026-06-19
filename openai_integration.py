import os
import time
from openai import OpenAI

class OpenAIIntegration:
    """
    Handles integration with OpenAI API for more intelligent responses.
    """
    
    def __init__(self, api_key=None):
        """
        Initialize with API key.
        
        Args:
            api_key (str, optional): OpenAI API key. If None, will try to get from environment.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")  # Get model from env or use default
        
        if not self.api_key:
            print("Warning: OpenAI API key not found. Set it using the OPENAI_API_KEY environment variable.")
            self.client = None
        else:
            # Initialize the OpenAI client
            self.client = OpenAI(api_key=self.api_key)
            
        print(f"Using OpenAI model: {self.model}")
        
        # Test API connection
        if self.api_key:
            self._test_api_connection()
    
    def _test_api_connection(self):
        """Test the OpenAI API connection."""
        if not self.client:
            return
            
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            print(f"✅ OpenAI API test successful: {response.usage.total_tokens} tokens used")
        except Exception as e:
            print(f"❌ OpenAI API test failed: {str(e)}")
    
    def get_response(self, prompt, system_message=None):
        """
        Get a response from OpenAI API.
        
        Args:
            prompt (str): User prompt
            system_message (str, optional): System message to guide the AI
            
        Returns:
            str: AI response or error message
        """
        if not self.client:
            return "OpenAI integration is not configured. Please set your API key."
        
        # Default system message if none provided
        if system_message is None:
            system_message = (
                "You are JARVIS, an AI assistant. When users ask for news, current events, or real-time information, "
                "suggest they use web search commands like 'search for Coimbatore news on Google' or offer to open news websites. "
                "Be helpful and suggest actionable solutions. Keep responses brief and informative."
            )
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        max_retries = 3
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                # Direct API call using the OpenAI client
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=150,
                    temperature=0.7
                )
                
                # Log token usage
                print(f"📊 OpenAI API call: {response.usage.total_tokens} tokens used")
                
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"Rate limit hit. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    continue
                return f"OpenAI API error: {str(e)}"
                
            except Exception as e:
                return f"Unexpected error: {str(e)}"
        
        return "Failed after multiple retries. Please try again later."