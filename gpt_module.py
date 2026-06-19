import json
import re
from openai_integration import OpenAIIntegration

class GPTTaskBreakdown:
    """
    Uses OpenAI GPT to break down complex natural language commands into actionable tasks.
    """
    
    def __init__(self, api_key=None):
        self.openai = OpenAIIntegration(api_key)
        
    def parse_command(self, user_input):
        """
        Parse complex user command into actionable tasks.
        
        Args:
            user_input (str): Natural language command from user
            
        Returns:
            list: List of actionable tasks or None if parsing fails
        """
        if not self.openai.api_key:
            return None
            
        system_prompt = """You are JARVIS, an AI assistant that breaks down user commands into actionable tasks.

Convert the user's natural language command into a JSON list of simple tasks. Use only these action types:
- "say: [text]" - speak text aloud
- "search: [query]" - search the internet
- "open: [app_name]" - open application (notepad, calculator, chrome, etc.)
- "type: [text]" - type text into active application
- "save_file: [filename]" - save current file
- "close: [app_name]" - close application

Example:
User: "Tell me the distance from Delhi to Mumbai and type it in Notepad"
Response: ["search: distance from Delhi to Mumbai", "say: The distance is approximately 1400km", "open: notepad", "type: Distance from Delhi to Mumbai: 1400km"]

Only return the JSON array, nothing else."""

        try:
            response = self.openai.get_response(user_input, system_prompt)
            
            # Extract JSON from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                tasks_json = json_match.group()
                tasks = json.loads(tasks_json)
                return [task.strip() for task in tasks if isinstance(task, str)]
            
            return None
        except Exception as e:
            print(f"Error parsing command: {e}")
            return None