import re
import os
from difflib import get_close_matches
from automation.system_control import SystemControl
from automation.file_access import FileAccess
from automation.browser_control import BrowserControl
from gpt_module import GPTTaskBreakdown
from action_executor import ActionExecutor

class CommandHandler:
    """
    Handles the processing and execution of user commands.
    """
    
    def __init__(self, speaker, openai_integration=None):
        """
        Initialize the command handler with necessary components.
        
        Args:
            speaker: Speaker object for voice responses
        """
        self.speaker = speaker
        self.system_control = SystemControl()
        self.file_access = FileAccess()
        self.browser_control = BrowserControl()
        self.openai_integration = openai_integration
        self.gpt_breakdown = GPTTaskBreakdown()
        self.action_executor = ActionExecutor(speaker)
        
        # App name mappings for fuzzy matching
        self.app_mappings = {
            'notepad': 'notepad',
            'notpad': 'notepad',
            'notepadd': 'notepad',
            'calculator': 'calc',
            'calc': 'calc',
            'claculator': 'calc',
            'calclator': 'calc',
            'paint': 'mspaint',
            'mspaint': 'mspaint',
            'chrome': 'chrome',
            'google chrome': 'chrome',
            'browser': 'chrome',
            'cmd': 'cmd',
            'command prompt': 'cmd',
            'terminal': 'cmd',
            'explorer': 'explorer',
            'file explorer': 'explorer',
            'files': 'explorer',
            'task manager': 'taskmgr',
            'taskmgr': 'taskmgr'
        }
        
        # Command patterns and their corresponding functions
        self.command_patterns = [
            # System commands - flexible patterns
            (r"(hey|yo|bro|please|can you|could you)?\s*(open|launch|start|run)\s+(.*?)\s*(now|please)?", self._handle_open_app_flexible),
            (r"open control panel", self._handle_control_panel),
            (r"uninstall (.*)", self._handle_uninstall),
            (r"(what('s| is) the time|tell me the (current )?time|current time|what time is it)", self._handle_time),
            (r"battery (percentage|level|status)", self._handle_battery),
            
            # File system commands
            (r"open (the |my |)(last|latest|recent) (file|document) (I |)(downloaded|download)", self._handle_last_download),
            (r"(show|tell|list) (me |)(the |my |)(last|latest|recent) (\d+) (files|documents)", self._handle_recent_files),
            
            # Browser commands
            (r"open (.*\.(com|org|net|io|gov))", self._handle_open_website),
            (r"search (for |)(.*) on google", self._handle_google_search),
            (r"search (for |)(.*) on youtube", self._handle_youtube_search),
            (r"open youtube and search (for |)(.*)", self._handle_youtube_search),
            
            # News commands
            (r"(latest |recent |)(news|updates) (in |from |about |)(.*)", self._handle_news_search),
            (r"tell me (the |)(latest |recent |)(news|updates) (in |from |about |)(.*)", self._handle_news_search),
        ]
    
    def process_command(self, command):
        """
        Process the user command and execute the appropriate action.
        
        Args:
            command (str): The user's command
            
        Returns:
            str: Response to the user's command
        """
        command = command.lower().strip()
        
        # Check for greetings
        if any(greeting in command for greeting in ["hello", "hi", "hey", "greetings"]):
            return "Hello! How can I assist you today?"
        
        # Check for help command
        if "help" in command or "what can you do" in command:
            return self._get_help_message()
        
        # First, try to match simple command patterns
        for pattern, handler in self.command_patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                return handler(*match.groups())
        
        # If no simple pattern matches, try GPT task breakdown for complex commands
        if self.gpt_breakdown.openai.api_key:
            return self._handle_complex_command(command)
        
        # Fallback to basic OpenAI conversation
        if self.openai_integration and self.openai_integration.api_key:
            system_message = "You are JARVIS, a helpful AI assistant. Keep responses brief and concise."
            return self.openai_integration.get_response(command, system_message)
        
        return "I'm not sure how to process that command. Try saying 'help' for a list of commands."
    
    def _handle_complex_command(self, command):
        """
        Handle complex multi-step commands using GPT task breakdown.
        
        Args:
            command (str): Complex natural language command
            
        Returns:
            str: Response message
        """
        # Check if this looks like a complex command
        complexity_indicators = ['and then', 'and', 'after that', 'also', 'then']
        action_words = ['open', 'search', 'type', 'tell', 'find', 'save', 'close']
        
        has_complexity = any(indicator in command.lower() for indicator in complexity_indicators)
        has_multiple_actions = sum(1 for word in action_words if word in command.lower()) > 1
        
        if has_complexity or has_multiple_actions:
            tasks = self.gpt_breakdown.parse_command(command)
            
            if tasks:
                self.speaker.speak("I understand. Let me break that down and execute it step by step.")
                self.action_executor.execute_tasks(tasks)
                return "Task completed successfully."
            else:
                return "I couldn't break down that complex command. Please try rephrasing it."
        
        # If not complex, fall back to simple OpenAI response
        if self.openai_integration and self.openai_integration.api_key:
            system_message = "You are JARVIS, a helpful AI assistant. Keep responses brief and concise."
            return self.openai_integration.get_response(command, system_message)
        
        return "I'm not sure how to process that command."
    
    def _get_help_message(self):
        """Return a help message with available commands."""
        return ("I can help you with the following:\n"
                "Simple Commands:\n"
                "- Open applications: 'open notepad'\n"
                "- System controls: 'open control panel', 'uninstall program'\n"
                "- File operations: 'open the last file I downloaded', 'show me the last 5 documents'\n"
                "- Web browsing: 'open youtube.com', 'search for cats on google'\n"
                "- System info: 'what's the time', 'battery percentage'\n\n"
                "Complex Commands (with OpenAI):\n"
                "- 'Search for Python tutorials and open Notepad to take notes'\n"
                "- 'Tell me the weather in Delhi and type it in a new document'\n"
                "- 'Find the distance between Mumbai and Pune, then save it to a file'")
    
    # System command handlers
    def _handle_open_app_flexible(self, greeting, action, app_name, politeness):
        """Handle flexible app opening commands."""
        return self._execute_app_command(app_name.strip() if app_name else "")
    
    def _execute_app_command(self, app_name):
        """Execute app opening with fuzzy matching."""
        if not app_name:
            return "Please specify which application to open."
            
        # Clean the app name
        app_name = app_name.lower().strip()
        
        # Direct mapping check
        if app_name in self.app_mappings:
            actual_app = self.app_mappings[app_name]
            return self._launch_app(actual_app, app_name)
        
        # Fuzzy matching
        close_matches = get_close_matches(app_name, self.app_mappings.keys(), n=1, cutoff=0.6)
        if close_matches:
            matched_app = close_matches[0]
            actual_app = self.app_mappings[matched_app]
            return self._launch_app(actual_app, app_name)
        
        # Try direct launch if no match found
        return self._launch_app(app_name, app_name)
    
    def _launch_app(self, command, original_name):
        """Actually launch the application."""
        try:
            if command == 'notepad':
                os.system('notepad')
                return "Opening Notepad now."
            elif command == 'calc':
                os.system('calc')
                return "Got it, launching Calculator."
            elif command == 'mspaint':
                os.system('mspaint')
                return "Opening Paint for you."
            elif command == 'chrome':
                os.system('start chrome')
                return "Starting Chrome browser."
            elif command == 'cmd':
                os.system('start cmd')
                return "Opening Command Prompt."
            elif command == 'explorer':
                os.system('explorer')
                return "Opening File Explorer."
            elif command == 'taskmgr':
                os.system('taskmgr')
                return "Opening Task Manager."
            else:
                # Try generic launch
                os.system(f'start {command}')
                return f"Attempting to open {original_name}."
        except Exception as e:
            return f"Sorry, I couldn't open {original_name}."
    
    def _handle_control_panel(self):
        return self.system_control.open_control_panel()
    
    def _handle_uninstall(self, app_name):
        return self.system_control.uninstall_app(app_name)
    
    def _handle_time(self, *args):
        return self.system_control.get_time()
    
    def _handle_battery(self):
        return self.system_control.get_battery_status()
    
    # File system command handlers
    def _handle_last_download(self):
        return self.file_access.open_last_download()
    
    def _handle_recent_files(self, _, __, ___, ____, count, file_type):
        try:
            count = int(count)
            return self.file_access.list_recent_files(count, file_type)
        except ValueError:
            return f"Sorry, I couldn't understand the number of files to show."
    
    # Browser command handlers
    def _handle_open_website(self, website):
        return self.browser_control.open_website(website)
    
    def _handle_google_search(self, _, query):
        return self.browser_control.search_google(query)
    
    def _handle_youtube_search(self, _, query):
        return self.browser_control.search_youtube(query)
    
    def _handle_news_search(self, *args):
        # Extract location from the arguments
        location = args[-1] if args and args[-1] else "local"
        query = f"{location} news latest"
        return self.browser_control.search_google(query)