"""
Simple JARVIS starter without Unicode issues
"""

import time
import os
from dotenv import load_dotenv
from listener import Listener
from speaker import Speaker
from commands import CommandHandler
from openai_integration import OpenAIIntegration

# Load environment variables
load_dotenv()

def main():
    print("Starting JARVIS Assistant...")
    listener = Listener()
    speaker = Speaker()
    
    # Initialize OpenAI integration
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("ERROR: OpenAI API key not configured!")
        speaker.speak("OpenAI API key is missing. Please configure it.")
        return
    
    # Test OpenAI connection
    openai_integration = OpenAIIntegration(api_key)
    test_response = openai_integration.get_response("test")
    
    if "Error communicating with OpenAI: 401" in test_response:
        print("ERROR: OpenAI API key is invalid!")
        speaker.speak("OpenAI API key is invalid. Please update it.")
        return
    elif "Error communicating with OpenAI: 429" in test_response:
        print("WARNING: OpenAI rate limit exceeded. Will retry automatically.")
        speaker.speak("OpenAI rate limit reached. I will retry requests automatically.")
    
    print("OpenAI integration connected!")
    command_handler = CommandHandler(speaker, openai_integration)
    speaker.speak("JARVIS is now online with AI capabilities. How can I help you?")
    
    while True:
        print("\nWaiting for your command...")
        user_input = listener.listen()
        
        if user_input.lower() in ["exit", "quit", "goodbye", "bye", "shutdown"]:
            speaker.speak("Shutting down JARVIS. Goodbye!")
            break
            
        try:
            response = command_handler.process_command(user_input)
            if response:
                speaker.speak(response)
        except Exception as e:
            error_msg = f"I encountered an error: {str(e)}"
            print(f"Error: {e}")
            speaker.speak(error_msg)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nJARVIS shutdown by user.")
    except Exception as e:
        print(f"\nJARVIS encountered a critical error: {e}")