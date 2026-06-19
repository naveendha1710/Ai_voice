import pyttsx3
import threading
import queue
import time
from typing import Optional

# Fix COM interface issues
try:
    import comtypes
    import comtypes.client
except ImportError:
    comtypes = None

try:
    # Try to import _compointer_base safely
    from comtypes import _compointer_base
except (ImportError, AttributeError, NameError):
    # Create a dummy _compointer_base if it doesn't exist
    class _compointer_base:
        pass
    if 'comtypes' in globals() and comtypes:
        comtypes._compointer_base = _compointer_base

class AdvancedVoiceEngine:
    """Advanced voice engine with natural speech, interruption handling, and voice queuing."""
    
    def __init__(self):
        self.engine = None
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.current_speech = None
        self.interrupt_flag = threading.Event()
        
        # Initialize engine with fallback drivers
        self._initialize_engine()
        
        if self.engine:
            self._setup_voice()
            # Start speech processing thread
            self.speech_thread = threading.Thread(target=self._process_speech_queue, daemon=True)
            self.speech_thread.start()
    
    def _initialize_engine(self):
        """Initialize TTS engine with multiple driver fallbacks."""
        drivers = ['sapi5', None, 'nsss', 'espeak']
        
        for driver in drivers:
            try:
                if driver:
                    self.engine = pyttsx3.init(driverName=driver)
                else:
                    self.engine = pyttsx3.init()
                print(f"✅ Voice engine initialized with driver: {driver or 'default'}")
                return
            except Exception as e:
                print(f"❌ Failed to initialize with driver {driver}: {e}")
                continue
        
        print("⚠️ All voice drivers failed, using fallback mode")
        self.engine = None
    
    def _setup_voice(self):
        """Configure voice properties safely."""
        if not self.engine:
            return
            
        try:
            # Set basic properties
            self.engine.setProperty('rate', 160)
            self.engine.setProperty('volume', 0.9)
            
            # Try to set preferred voice
            voices = self.engine.getProperty('voices')
            if voices:
                preferred_voices = ['david', 'mark', 'zira', 'hazel']
                for voice in voices:
                    if any(pref in voice.name.lower() for pref in preferred_voices):
                        self.engine.setProperty('voice', voice.id)
                        break
        except Exception as e:
            print(f"Voice setup warning: {e}")
    
    def speak(self, text: str, priority: str = 'normal', interruptible: bool = True):
        """Add text to speech queue with priority."""
        speech_item = {
            'text': text,
            'priority': priority,
            'interruptible': interruptible,
            'timestamp': time.time()
        }
        
        if priority == 'urgent':
            # Clear queue for urgent messages
            self._clear_queue()
            self.interrupt_current_speech()
        
        self.speech_queue.put(speech_item)
    
    def _process_speech_queue(self):
        """Process speech queue in background thread."""
        while True:
            try:
                speech_item = self.speech_queue.get(timeout=1)
                self._speak_text(speech_item)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Speech processing error: {e}")
    
    def _speak_text(self, speech_item: dict):
        """Actually speak the text with error handling."""
        text = speech_item['text']
        print(f"JARVIS: {text}")
        
        if not self.engine:
            return
            
        try:
            self.is_speaking = True
            self.current_speech = speech_item
            self.interrupt_flag.clear()
            
            self.engine.say(text)
            self.engine.runAndWait()
            
        except Exception as e:
            print(f"Speech error: {e}")
        finally:
            self.is_speaking = False
            self.current_speech = None
    
    def _enhance_speech(self, text: str) -> str:
        """Enhance text for more natural speech."""
        # Add pauses for better flow
        text = text.replace('. ', '... ')
        text = text.replace(', ', ', ')
        
        # Emphasize important words
        emphasis_words = ['important', 'urgent', 'warning', 'error', 'completed', 'failed']
        for word in emphasis_words:
            text = text.replace(word, f'<emphasis level="strong">{word}</emphasis>')
        
        return text
    
    def interrupt_current_speech(self):
        """Interrupt current speech safely."""
        if self.is_speaking and self.engine:
            try:
                self.interrupt_flag.set()
                self.engine.stop()
            except Exception:
                pass
    
    def _clear_queue(self):
        """Clear the speech queue."""
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
            except queue.Empty:
                break
    
    def is_busy(self) -> bool:
        """Check if voice engine is currently speaking."""
        return self.is_speaking
    
    def wait_until_done(self, timeout: Optional[float] = None):
        """Wait until current speech is finished."""
        start_time = time.time()
        while self.is_speaking:
            if timeout and (time.time() - start_time) > timeout:
                break
            time.sleep(0.1)
    
    def set_voice_speed(self, speed: int):
        """Set voice speed safely."""
        if self.engine:
            try:
                self.engine.setProperty('rate', max(50, min(300, speed)))
            except Exception as e:
                print(f"Voice speed error: {e}")
    
    def set_voice_volume(self, volume: float):
        """Set voice volume safely."""
        if self.engine:
            try:
                self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
            except Exception as e:
                print(f"Voice volume error: {e}")
    
    def get_available_voices(self) -> list:
        """Get list of available voices safely."""
        if not self.engine:
            return []
        try:
            voices = self.engine.getProperty('voices')
            return [(voice.id, voice.name) for voice in voices] if voices else []
        except Exception as e:
            print(f"Voice list error: {e}")
            return []
    
    def set_voice_by_name(self, voice_name: str) -> bool:
        """Set voice by name safely."""
        if not self.engine:
            return False
        try:
            voices = self.engine.getProperty('voices')
            if voices:
                for voice in voices:
                    if voice_name.lower() in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        return True
        except Exception as e:
            print(f"Voice change error: {e}")
        return False