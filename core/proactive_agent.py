import threading
import time
import psutil
from datetime import datetime, timedelta
from typing import Callable

class ProactiveAgent:
    """Handles proactive behaviors like reminders, system monitoring, and suggestions."""
    
    def __init__(self, speaker, context_manager):
        self.speaker = speaker
        self.context_manager = context_manager
        self.monitoring = False
        self.reminders = []
        self.system_alerts = {
            'battery_low': False,
            'memory_high': False,
            'disk_low': False
        }
        
    def start_monitoring(self):
        """Start background monitoring."""
        if not self.monitoring:
            self.monitoring = True
            threading.Thread(target=self._monitor_loop, daemon=True).start()
    
    def stop_monitoring(self):
        """Stop background monitoring."""
        self.monitoring = False
    
    def add_reminder(self, message: str, delay_minutes: int):
        """Add a timed reminder."""
        reminder_time = datetime.now() + timedelta(minutes=delay_minutes)
        self.reminders.append({
            'message': message,
            'time': reminder_time,
            'active': True
        })
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                self._check_reminders()
                self._check_system_health()
                self._check_idle_time()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(60)
    
    def _check_reminders(self):
        """Check and trigger reminders."""
        current_time = datetime.now()
        for reminder in self.reminders:
            if reminder['active'] and current_time >= reminder['time']:
                self.speaker.speak(f"Reminder: {reminder['message']}")
                reminder['active'] = False
    
    def _check_system_health(self):
        """Monitor system health and alert if needed."""
        try:
            # Battery check
            battery = psutil.sensors_battery()
            if battery and battery.percent < 20 and not battery.power_plugged:
                if not self.system_alerts['battery_low']:
                    self.speaker.speak(f"Battery is low at {battery.percent}%. Consider plugging in your charger.")
                    self.system_alerts['battery_low'] = True
            elif battery and battery.percent > 30:
                self.system_alerts['battery_low'] = False
            
            # Memory check
            memory = psutil.virtual_memory()
            if memory.percent > 85:
                if not self.system_alerts['memory_high']:
                    self.speaker.speak(f"Memory usage is high at {memory.percent}%. Consider closing some applications.")
                    self.system_alerts['memory_high'] = True
            elif memory.percent < 70:
                self.system_alerts['memory_high'] = False
            
            # Disk space check
            disk = psutil.disk_usage('C:')
            disk_percent = (disk.used / disk.total) * 100
            if disk_percent > 90:
                if not self.system_alerts['disk_low']:
                    self.speaker.speak(f"Disk space is low at {disk_percent:.1f}%. Consider cleaning up files.")
                    self.system_alerts['disk_low'] = True
            elif disk_percent < 85:
                self.system_alerts['disk_low'] = False
                
        except Exception as e:
            print(f"System health check error: {e}")
    
    def _check_idle_time(self):
        """Check for idle time and offer suggestions."""
        last_activity = self.context_manager.session_data['last_activity']
        idle_time = datetime.now() - last_activity
        
        # If idle for more than 30 minutes, offer suggestions
        if idle_time > timedelta(minutes=30):
            current_hour = datetime.now().hour
            if 9 <= current_hour <= 17:  # Work hours
                suggestions = [
                    "Would you like me to check your calendar for upcoming meetings?",
                    "Should I help you organize your desktop or clean temporary files?",
                    "Would you like a productivity tip or a quick system status update?"
                ]
                # Only suggest once per idle period
                if not hasattr(self, '_last_suggestion_time') or \
                   datetime.now() - self._last_suggestion_time > timedelta(hours=1):
                    import random
                    suggestion = random.choice(suggestions)
                    self.speaker.speak(suggestion)
                    self._last_suggestion_time = datetime.now()
    
    def suggest_based_on_time(self):
        """Provide time-based suggestions."""
        current_hour = datetime.now().hour
        
        if current_hour == 9:
            return "Good morning! Ready to start your productive day?"
        elif current_hour == 12:
            return "It's lunch time. Don't forget to take a break!"
        elif current_hour == 17:
            return "End of work day. Would you like me to help wrap up any tasks?"
        elif current_hour >= 22:
            return "It's getting late. Consider winding down for better sleep."
        
        return None