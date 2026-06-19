import re
import json
from datetime import datetime
from commands import CommandHandler
from gpt_module import GPTTaskBreakdown
from action_executor import ActionExecutor

class EnhancedCommandHandler(CommandHandler):
    """Enhanced command handler with context awareness and advanced AI integration."""
    
    def __init__(self, voice_engine, openai_integration, context_manager, system_controller, task_manager):
        # Initialize parent class properly
        super().__init__(voice_engine, openai_integration)
        
        # Enhanced components
        self.context_manager = context_manager
        self.system_controller = system_controller
        self.task_manager = task_manager
        self.voice_engine = voice_engine
        
        # Initialize existing automation modules
        from automation.system_control import SystemControl
        from automation.file_access import FileAccess
        from automation.browser_control import BrowserControl
        
        self.system_control = SystemControl()
        self.file_access = FileAccess()
        self.browser_control = BrowserControl()
        
        # GPT and action executor
        self.gpt_breakdown = GPTTaskBreakdown()
        self.action_executor = ActionExecutor(voice_engine)
        
        # Enhanced command patterns
        self.enhanced_patterns = [
            # Context-aware commands
            (r"what was i (doing|working on) (before|earlier|last)", self._handle_context_recall),
            (r"continue (with |from |)(that|previous|last) (task|work|conversation)", self._handle_continue_task),
            (r"remind me (in |after |)(\d+) (minutes?|hours?) (to |about |)(.*)", self._handle_reminder),
            
            # System control commands
            (r"set volume to (\d+)", self._handle_set_volume),
            (r"set brightness to (\d+)", self._handle_set_brightness),
            (r"(turn on|turn off|toggle) (wifi|wi-fi)", self._handle_wifi_control),
            (r"clean (temp|temporary) files", self._handle_clean_temp),
            (r"take (a |)screenshot", self._handle_screenshot),
            (r"system (status|info|information)", self._handle_system_info),
            
            # Task management
            (r"(show|list|what are) (my |)(active |current |)(tasks|jobs)", self._handle_task_status),
            (r"cancel task (\w+)", self._handle_cancel_task),
            (r"task status", self._handle_task_status),
            
            # Multi-tasking commands
            (r"(.*) and (also |)(.*)", self._handle_parallel_commands),
            
            # Voice control
            (r"speak (slower|faster|louder|quieter)", self._handle_voice_control),
            (r"change voice to (\w+)", self._handle_voice_change),
            (r"stop (talking|speaking)", self._handle_stop_speech),
        ]
    
    def process_enhanced_command(self, command: str, context_summary: str = "") -> str:
        """Process command with enhanced AI and context awareness."""
        command = command.lower().strip()
        
        # Check enhanced patterns first
        for pattern, handler in self.enhanced_patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                return handler(*match.groups())
        
        # Check if it's a complex multi-step command
        if self._is_complex_command(command):
            return self._handle_complex_ai_command(command, context_summary)
        
        # Fall back to original command processing
        return self.process_command(command)
    
    def _is_complex_command(self, command: str) -> bool:
        """Determine if command requires AI breakdown."""
        complexity_indicators = ['and then', 'and also', 'after that', 'then', 'also']
        action_words = ['open', 'search', 'type', 'tell', 'find', 'save', 'close', 'play', 'start']
        
        has_complexity = any(indicator in command for indicator in complexity_indicators)
        has_multiple_actions = sum(1 for word in action_words if word in command) > 1
        
        return has_complexity or has_multiple_actions or len(command.split()) > 8
    
    def _handle_complex_ai_command(self, command: str, context: str) -> str:
        """Handle complex commands using AI breakdown."""
        if not self.openai_integration:
            return "Complex commands require OpenAI integration. Please configure your API key."
        
        # Enhanced prompt with context
        enhanced_prompt = f"""
        Context: {context}
        User Command: {command}
        
        Break this down into actionable tasks. Consider the context and user's current situation.
        """
        
        tasks = self.gpt_breakdown.parse_command(enhanced_prompt)
        
        if tasks:
            # Add to task manager for tracking
            task_id = self.task_manager.add_task(
                f"Complex command: {command[:50]}...",
                self.action_executor.execute_tasks,
                tasks
            )
            
            return f"I understand. Breaking down your request into {len(tasks)} tasks and executing them."
        else:
            # Fallback to direct AI response
            return self.openai_integration.get_response(command, f"Context: {context}")
    
    # Enhanced command handlers
    def _handle_context_recall(self, action, timeframe):
        """Recall previous context or tasks."""
        recent_context = self.context_manager.get_recent_context(60)  # Last hour
        
        if recent_context:
            last_topics = [ctx.get('context', {}).get('topic', 'general') for ctx in recent_context[-3:]]
            active_tasks = self.context_manager.get_active_tasks()
            
            response = f"Earlier you were working on: {', '.join(set(last_topics))}. "
            if active_tasks:
                response += f"You have active tasks: {', '.join([t['description'] for t in active_tasks.values()])}."
            
            return response
        else:
            return "I don't have any recent context to recall."
    
    def _handle_continue_task(self, *args):
        """Continue with previous task or conversation."""
        active_tasks = self.context_manager.get_active_tasks()
        
        if active_tasks:
            task_desc = list(active_tasks.values())[0]['description']
            return f"Continuing with: {task_desc}. What would you like me to do next?"
        else:
            recent_context = self.context_manager.get_recent_context(30)
            if recent_context:
                last_topic = recent_context[-1].get('context', {}).get('topic', 'our conversation')
                return f"Let's continue with {last_topic}. What's your next question?"
            else:
                return "I don't have a previous task to continue. What would you like me to help with?"
    
    def _handle_reminder(self, prefix, delay, unit, about_prefix, message):
        """Set a reminder."""
        try:
            delay_num = int(delay)
            if unit.startswith('hour'):
                delay_minutes = delay_num * 60
            else:
                delay_minutes = delay_num
            
            self.context_manager.proactive_agent.add_reminder(message, delay_minutes)
            return f"I'll remind you about '{message}' in {delay} {unit}."
        except ValueError:
            return "I couldn't understand the time format. Please specify like '5 minutes' or '2 hours'."
    
    def _handle_set_volume(self, level):
        """Set system volume."""
        try:
            volume_level = int(level)
            return self.system_controller.set_volume(volume_level)
        except ValueError:
            return "Please specify a volume level between 0 and 100."
    
    def _handle_set_brightness(self, level):
        """Set screen brightness."""
        try:
            brightness_level = int(level)
            return self.system_controller.set_brightness(brightness_level)
        except ValueError:
            return "Please specify a brightness level between 0 and 100."
    
    def _handle_wifi_control(self, action, interface):
        """Control WiFi."""
        enable = action.lower() in ['turn on', 'enable']
        return self.system_controller.toggle_wifi(enable)
    
    def _handle_clean_temp(self):
        """Clean temporary files."""
        return self.system_controller.clean_temp_files()
    
    def _handle_screenshot(self, article=None):
        """Take a screenshot."""
        return self.system_controller.take_screenshot()
    
    def _handle_system_info(self):
        """Get system information."""
        return self.system_controller.get_system_info()
    
    def _handle_task_status(self, *args):
        """Get task status."""
        return self.task_manager.get_task_status()
    
    def _handle_cancel_task(self, task_id):
        """Cancel a specific task."""
        return self.task_manager.cancel_task(task_id)
    
    def _handle_parallel_commands(self, command1, also, command2):
        """Handle parallel commands."""
        # Process both commands in parallel
        task_id1 = self.task_manager.add_task(
            f"Command: {command1}",
            self._execute_single_command,
            command1
        )
        
        task_id2 = self.task_manager.add_task(
            f"Command: {command2}",
            self._execute_single_command,
            command2
        )
        
        return f"Executing both commands in parallel: '{command1}' and '{command2}'"
    
    def _execute_single_command(self, command):
        """Execute a single command (for parallel processing)."""
        return self.process_command(command)
    
    def _handle_voice_control(self, control):
        """Control voice settings."""
        if control == "slower":
            self.voice_engine.set_voice_speed(120)
            return "Speaking slower now."
        elif control == "faster":
            self.voice_engine.set_voice_speed(200)
            return "Speaking faster now."
        elif control == "louder":
            self.voice_engine.set_voice_volume(1.0)
            return "Speaking louder now."
        elif control == "quieter":
            self.voice_engine.set_voice_volume(0.6)
            return "Speaking quieter now."
    
    def _handle_voice_change(self, voice_name):
        """Change voice."""
        if self.voice_engine.set_voice_by_name(voice_name):
            return f"Voice changed to {voice_name}."
        else:
            available = [name for _, name in self.voice_engine.get_available_voices()]
            return f"Voice '{voice_name}' not found. Available voices: {', '.join(available[:3])}..."
    
    def _handle_stop_speech(self):
        """Stop current speech."""
        self.voice_engine.interrupt_current_speech()
        return ""  # Don't speak a response