class Listener:
    """
    Simulates voice recognition by taking text input from the user.
    Can be extended later to use actual speech recognition.
    """
    
    def listen(self):
        """
        Simulates listening to user's voice command by taking text input.
        
        Returns:
            str: The user's command as text
        """
        try:
            user_input = input("🎤 You: ").strip()
            if user_input:
                print(f"📝 Received: {user_input}")
            return user_input
        except (EOFError, KeyboardInterrupt):
            return "exit"