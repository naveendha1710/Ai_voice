import pyttsx3

class Speaker:
    """
    Handles text-to-speech functionality for JARVIS responses.
    """
    
    def __init__(self):
        """
        Initialize the text-to-speech engine.
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        
        # Get available voices and set a male voice if available
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "male" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
    
    def speak(self, text):
        """
        Convert text to speech.
        
        Args:
            text (str): The text to be spoken
        """
        print(f"JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()