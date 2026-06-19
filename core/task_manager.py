import threading
import time
import uuid
from datetime import datetime
from typing import Dict, List, Callable

class TaskManager:
    """Manages multiple concurrent tasks and provides status updates."""
    
    def __init__(self, speaker):
        self.speaker = speaker
        self.active_tasks = {}
        self.completed_tasks = {}
        self.task_queue = []
        self.max_concurrent = 3
        
    def add_task(self, description: str, task_func: Callable, *args, **kwargs) -> str:
        """Add a new task to be executed."""
        task_id = str(uuid.uuid4())[:8]
        task = {
            'id': task_id,
            'description': description,
            'function': task_func,
            'args': args,
            'kwargs': kwargs,
            'status': 'queued',
            'created': datetime.now(),
            'started': None,
            'completed': None,
            'result': None,
            'error': None
        }
        
        self.task_queue.append(task)
        self._process_queue()
        return task_id
    
    def _process_queue(self):
        """Process queued tasks if slots available."""
        while len(self.active_tasks) < self.max_concurrent and self.task_queue:
            task = self.task_queue.pop(0)
            self._start_task(task)
    
    def _start_task(self, task: Dict):
        """Start executing a task in a separate thread."""
        task['status'] = 'running'
        task['started'] = datetime.now()
        self.active_tasks[task['id']] = task
        
        def task_wrapper():
            try:
                result = task['function'](*task['args'], **task['kwargs'])
                task['result'] = result
                task['status'] = 'completed'
                task['completed'] = datetime.now()
                
                # Move to completed tasks
                self.completed_tasks[task['id']] = task
                del self.active_tasks[task['id']]
                
                # Notify completion
                self.speaker.speak(f"Task completed: {task['description']}")
                
                # Process next queued task
                self._process_queue()
                
            except Exception as e:
                task['error'] = str(e)
                task['status'] = 'failed'
                task['completed'] = datetime.now()
                
                # Move to completed tasks
                self.completed_tasks[task['id']] = task
                del self.active_tasks[task['id']]
                
                # Notify failure
                self.speaker.speak(f"Task failed: {task['description']} - {str(e)}")
                
                # Process next queued task
                self._process_queue()
        
        thread = threading.Thread(target=task_wrapper, daemon=True)
        thread.start()
    
    def get_task_status(self, task_id: str = None) -> str:
        """Get status of specific task or all tasks."""
        if task_id:
            # Check active tasks
            if task_id in self.active_tasks:
                task = self.active_tasks[task_id]
                return f"Task {task_id}: {task['description']} - Status: {task['status']}"
            
            # Check completed tasks
            if task_id in self.completed_tasks:
                task = self.completed_tasks[task_id]
                return f"Task {task_id}: {task['description']} - Status: {task['status']}"
            
            return f"Task {task_id} not found"
        
        else:
            # Return status of all tasks
            status_report = []
            
            if self.active_tasks:
                status_report.append(f"Active tasks ({len(self.active_tasks)}):")
                for task in self.active_tasks.values():
                    status_report.append(f"  - {task['description']} ({task['status']})")
            
            if self.task_queue:
                status_report.append(f"Queued tasks ({len(self.task_queue)}):")
                for task in self.task_queue[:3]:  # Show first 3
                    status_report.append(f"  - {task['description']}")
            
            if not self.active_tasks and not self.task_queue:
                status_report.append("No active or queued tasks")
            
            return "\n".join(status_report)
    
    def cancel_task(self, task_id: str) -> str:
        """Cancel a queued or running task."""
        # Check queued tasks
        for i, task in enumerate(self.task_queue):
            if task['id'] == task_id:
                self.task_queue.pop(i)
                return f"Cancelled queued task: {task['description']}"
        
        # Check active tasks (can't really cancel running threads safely)
        if task_id in self.active_tasks:
            return f"Cannot cancel running task: {self.active_tasks[task_id]['description']}"
        
        return f"Task {task_id} not found or already completed"
    
    def clear_completed(self):
        """Clear completed task history."""
        count = len(self.completed_tasks)
        self.completed_tasks.clear()
        return f"Cleared {count} completed tasks from history"
    
    def execute_parallel_tasks(self, task_descriptions: List[str], task_functions: List[Callable]):
        """Execute multiple tasks in parallel."""
        task_ids = []
        for desc, func in zip(task_descriptions, task_functions):
            task_id = self.add_task(desc, func)
            task_ids.append(task_id)
        
        self.speaker.speak(f"Started {len(task_ids)} tasks in parallel")
        return task_ids