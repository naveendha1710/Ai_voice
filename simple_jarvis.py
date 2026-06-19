"""
Simple JARVIS starter with modern OpenAI API and no Unicode
"""

import os
import time
from dotenv import load_dotenv
from openai import OpenAI
import speech_recognition as sr
import pyttsx3

# Load environment variables
load_dotenv()

class SimpleJarvis:
    def __init__(self):
        # Initialize speech components
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)
        
        # Initialize OpenAI
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
    
    def speak(self, text):
        """Convert text to speech."""
        print(f"JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen for user input."""
        with sr.Microphone() as source:
            print("\nListening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            
        try:
            user_input = self.recognizer.recognize_google(audio)
            print(f"You: {user_input}")
            return user_input
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            self.speak("Sorry, my speech service is down.")
            return ""
    
    def get_ai_response(self, prompt):
        """Get response from OpenAI."""
        if not self.client:
            return "OpenAI is not configured. Please set your API key."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are JARVIS, an AI assistant. Keep responses helpful and concise."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def process_command(self, command):
        """Process user command."""
        command = command.lower()
        
        # Basic commands
        if "hello" in command or "hi jarvis" in command:
            return "Hello! How can I help you today?"
        
        elif "time" in command:
            current_time = time.strftime("%I:%M %p")
            return f"The current time is {current_time}."
        
        elif "date" in command:
            current_date = time.strftime("%A, %B %d, %Y")
            return f"Today is {current_date}."
        
        # For other commands, use AI
        else:
            return self.get_ai_response(command)
    
    def run(self):
        """Run the assistant."""
        print("Starting Simple JARVIS...")
        
        if not self.api_key:
            print("WARNING: OpenAI API key not found.")
            self.speak("OpenAI API key is missing. Some features will be limited.")
        else:
            self.speak("JARVIS is online and ready to assist.")
        
        while True:
            user_input = self.listen()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit", "goodbye", "bye", "shutdown"]:
                self.speak("Shutting down. Goodbye!")
                break
            
            response = self.process_command(user_input)
            self.speak(response)

if __name__ == "__main__":
    jarvis = SimpleJarvis()
    jarvis.run()