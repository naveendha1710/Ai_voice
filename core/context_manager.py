import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any

class ContextManager:
    """Manages conversation context, memory, and user preferences."""
    
    def __init__(self):
        self.conversation_history = []
        self.current_tasks = {}
        self.user_preferences = {}
        self.session_data = {
            'start_time': datetime.now(),
            'last_activity': datetime.now(),
            'active_apps': [],
            'current_topic': None
        }
        self.load_preferences()
    
    def add_interaction(self, user_input: str, response: str, context: Dict = None):
        """Add interaction to conversation history."""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'response': response,
            'context': context or {}
        }
        self.conversation_history.append(interaction)
        self.session_data['last_activity'] = datetime.now()
        
        # Keep only last 50 interactions for memory efficiency
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
    
    def get_recent_context(self, minutes: int = 30) -> List[Dict]:
        """Get recent conversation context."""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        return [
            interaction for interaction in self.conversation_history
            if datetime.fromisoformat(interaction['timestamp']) > cutoff
        ]
    
    def add_task(self, task_id: str, description: str, status: str = "active"):
        """Add or update a task."""
        self.current_tasks[task_id] = {
            'description': description,
            'status': status,
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat()
        }
    
    def update_task_status(self, task_id: str, status: str):
        """Update task status."""
        if task_id in self.current_tasks:
            self.current_tasks[task_id]['status'] = status
            self.current_tasks[task_id]['updated'] = datetime.now().isoformat()
    
    def get_active_tasks(self) -> Dict:
        """Get all active tasks."""
        return {k: v for k, v in self.current_tasks.items() if v['status'] == 'active'}
    
    def set_preference(self, key: str, value: Any):
        """Set user preference."""
        self.user_preferences[key] = value
        self.save_preferences()
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference."""
        return self.user_preferences.get(key, default)
    
    def save_preferences(self):
        """Save preferences to file."""
        try:
            with open('user_preferences.json', 'w') as f:
                json.dump(self.user_preferences, f, indent=2)
        except Exception:
            pass
    
    def load_preferences(self):
        """Load preferences from file."""
        try:
            with open('user_preferences.json', 'r') as f:
                self.user_preferences = json.load(f)
        except FileNotFoundError:
            self.user_preferences = {
                'voice_speed': 150,
                'preferred_browser': 'chrome',
                'work_hours': {'start': '09:00', 'end': '17:00'},
                'reminder_frequency': 30
            }
    
    def get_context_summary(self) -> str:
        """Get a summary of current context for AI."""
        recent = self.get_recent_context(15)
        active_tasks = self.get_active_tasks()
        
        summary = f"Current session started at {self.session_data['start_time'].strftime('%H:%M')}. "
        
        if recent:
            summary += f"Recent conversation topics: {', '.join(set([r.get('context', {}).get('topic', 'general') for r in recent[-3:]]))}. "
        
        if active_tasks:
            summary += f"Active tasks: {', '.join([t['description'] for t in active_tasks.values()])}. "
        
        return summary