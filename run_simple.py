"""
Simple script to run JARVIS with minimal dependencies
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import pyttsx3

# Load environment variables
load_dotenv()

def main():
    print("🤖 Simple JARVIS - Minimal Version")
    print("=" * 40)
    
    # Initialize text-to-speech
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        
        def speak(text):
            print(f"JARVIS: {text}")
            engine.say(text)
            engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")
        def speak(text):
            print(f"JARVIS: {text}")
    
    # Initialize OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        speak("OpenAI API key not found. Please set it in the .env file.")
        return
    
    client = OpenAI(api_key=api_key)
    
    # Test API connection
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print(f"✅ OpenAI API connected: {response.choices[0].message.content}")
    except Exception as e:
        speak(f"Error connecting to OpenAI API: {e}")
        return
    
    speak("JARVIS is ready. How can I help you?")
    
    # Main loop
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
            speak("Goodbye!")
            break
        
        # Simple command handling
        if "open" in user_input.lower() and any(app in user_input.lower() for app in ["notepad", "calculator", "chrome", "browser"]):
            app = ""
            if "notepad" in user_input.lower():
                app = "notepad"
                os.system("notepad")
            elif "calculator" in user_input.lower() or "calc" in user_input.lower():
                app = "calculator"
                os.system("calc")
            elif "chrome" in user_input.lower() or "browser" in user_input.lower():
                app = "browser"
                os.system("start chrome")
                
            speak(f"Opening {app}")
            continue
        
        # Use OpenAI for everything else
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are JARVIS, a helpful AI assistant. Keep responses brief and informative."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=150
            )
            
            reply = response.choices[0].message.content
            speak(reply)
            
        except Exception as e:
            speak(f"I encountered an error: {str(e)}")

if __name__ == "__main__":
    main()