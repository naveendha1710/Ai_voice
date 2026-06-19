import os
import time
import threading
from dotenv import load_dotenv
from datetime import datetime


# Core JARVIS modules
from core.context_manager import ContextManager
from core.proactive_agent import ProactiveAgent
from core.system_controller import AdvancedSystemController
from core.task_manager import TaskManager
from core.voice_engine import AdvancedVoiceEngine

# Existing modules
from listener import Listener
from openai_integration import OpenAIIntegration
from enhanced_commands import EnhancedCommandHandler

load_dotenv()

class AdvancedJARVIS:
    """Advanced JARVIS AI Assistant with context awareness and proactive behavior."""
    
    def __init__(self):
        print("🤖 Initializing Advanced JARVIS...")
        
        # Core components
        self.voice_engine = AdvancedVoiceEngine()
        self.listener = Listener()
        self.context_manager = ContextManager()
        self.system_controller = AdvancedSystemController()
        self.task_manager = TaskManager(self.voice_engine)
        
        # Initialize OpenAI
        self.openai_integration = self._initialize_openai()
        
        # Enhanced command handler
        self.command_handler = EnhancedCommandHandler(
            self.voice_engine, 
            self.openai_integration,
            self.context_manager,
            self.system_controller,
            self.task_manager
        )
        
        # Proactive agent
        self.proactive_agent = ProactiveAgent(self.voice_engine, self.context_manager)
        
        # System state
        self.running = False
        self.session_start = datetime.now()
        
    def _initialize_openai(self):
        """Initialize OpenAI with proper error handling."""
        api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key or api_key == "your_openai_api_key_here":
            self.voice_engine.speak("OpenAI API key not configured. Please set it up for full capabilities.", priority='urgent')
            return None
        
        openai_integration = OpenAIIntegration(api_key)
        
        # Test connection
        test_response = openai_integration.get_response("test connection")
        if "Error" in test_response:
            self.voice_engine.speak(f"OpenAI connection issue: {test_response}", priority='urgent')
            return None
        
        print("✅ OpenAI integration successful")
        return openai_integration
    
    def start(self):
        """Start the advanced JARVIS system."""
        self.running = True
        
        # Start proactive monitoring
        self.proactive_agent.start_monitoring()
        
        # Welcome message with context
        welcome_msg = self._generate_welcome_message()
        self.voice_engine.speak(welcome_msg, priority='urgent')
        
        # Main interaction loop
        self._main_loop()
    
    def _generate_welcome_message(self):
        """Generate contextual welcome message without system status."""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            greeting = "Good morning"
        elif 12 <= current_hour < 17:
            greeting = "Good afternoon"
        elif 17 <= current_hour < 21:
            greeting = "Good evening"
        else:
            greeting = "Good night"
        
        return f"{greeting}! Advanced JARVIS is now online with full AI capabilities. How can I assist you today?"
    
    def _main_loop(self):
        """Main interaction loop with enhanced error handling."""
        while self.running:
            try:
                print(f"\n🎤 Waiting for your command... (Session: {self._get_session_duration()})")
                print("💡 Try: 'hello', 'what time is it', 'help', or any question")
                
                user_input = self.listener.listen()
                
                if not user_input or not user_input.strip():
                    print("⚠️ No input received, please try again...")
                    continue
                
                print(f"📝 You said: {user_input}")
                
                # Check for shutdown commands
                if user_input.lower() in ["exit", "quit", "goodbye", "bye", "shutdown", "stop jarvis"]:
                    self._shutdown()
                    break
                
                # Process command with context
                self._process_command_with_context(user_input)
                
            except KeyboardInterrupt:
                print("\n⚠️ Keyboard interrupt detected")
                self._shutdown()
                break
            except Exception as e:
                error_msg = f"I encountered an error: {str(e)}"
                print(f"❌ Error: {e}")
                self.voice_engine.speak(error_msg, priority='urgent')
                time.sleep(1)
    
    def _process_command_with_context(self, user_input: str):
        """Process command with full context awareness."""
        try:
            # Add context to the command processing
            context_summary = self.context_manager.get_context_summary()
            
            # Enhanced command processing
            response = self.command_handler.process_enhanced_command(user_input, context_summary)
            
            # Record interaction
            self.context_manager.add_interaction(
                user_input, 
                response, 
                {'timestamp': datetime.now().isoformat()}
            )
            
            # Speak response if provided
            if response:
                self.voice_engine.speak(response)
                
        except Exception as e:
            error_msg = f"Command processing failed: {str(e)}"
            print(f"❌ {error_msg}")
            self.voice_engine.speak("I had trouble processing that command. Please try again.", priority='urgent')
    
    def _get_session_duration(self):
        """Get current session duration."""
        duration = datetime.now() - self.session_start
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def _shutdown(self):
        """Graceful shutdown of JARVIS."""
        self.running = False
        
        # Stop proactive monitoring
        self.proactive_agent.stop_monitoring()
        
        # Save context and preferences
        self.context_manager.save_preferences()
        
        # Final message
        session_duration = self._get_session_duration()
        shutdown_msg = f"JARVIS shutting down after {session_duration} session. Goodbye!"
        
        self.voice_engine.speak(shutdown_msg, priority='urgent')
        self.voice_engine.wait_until_done(timeout=5)
        
        print("🤖 Advanced JARVIS shutdown complete")

def main():
    """Main entry point for Advanced JARVIS."""
    try:
        jarvis = AdvancedJARVIS()
        jarvis.start()
    except Exception as e:
        print(f"❌ Critical error starting JARVIS: {e}")

if __name__ == "__main__":
    main()