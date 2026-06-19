import os
import subprocess
import datetime
import psutil

class SystemControl:
    """
    Handles system-related operations like opening applications,
    control panel, and retrieving system information.
    """
    
    def open_application(self, app_name):
        """
        Opens the specified application.
        
        Args:
            app_name (str): Name of the application to open
            
        Returns:
            str: Response message
        """
        app_name = app_name.lower()
        
        # Common applications and their commands
        app_commands = {
            "notepad": "notepad",
            "calculator": "calc",
            "paint": "mspaint",
            "file explorer": "explorer",
            "command prompt": "cmd",
            "task manager": "taskmgr",
            "chrome": "start chrome",
            "edge": "start msedge",
            "firefox": "start firefox",
            "word": "start winword",
            "excel": "start excel",
            "powerpoint": "start powerpnt",
        }
        
        # Check if the app is in our known list
        if app_name in app_commands:
            try:
                os.system(app_commands[app_name])
                return f"Opening {app_name}."
            except Exception as e:
                return f"Failed to open {app_name}. Error: {str(e)}"
        
        # Try to open the app directly if not in our list
        try:
            os.system(f"start {app_name}")
            return f"Attempting to open {app_name}."
        except Exception as e:
            return f"Failed to open {app_name}. Error: {str(e)}"
    
    def open_control_panel(self):
        """
        Opens the Windows Control Panel.
        
        Returns:
            str: Response message
        """
        try:
            os.system("control")
            return "Opening Control Panel."
        except Exception as e:
            return f"Failed to open Control Panel. Error: {str(e)}"
    
    def uninstall_app(self, app_name):
        """
        Opens the Programs and Features window to uninstall an application.
        
        Args:
            app_name (str): Name of the application to uninstall
            
        Returns:
            str: Response message
        """
        try:
            # Open Programs and Features
            os.system("appwiz.cpl")
            return f"Opening Programs and Features. Please locate {app_name} to uninstall."
        except Exception as e:
            return f"Failed to open uninstall window. Error: {str(e)}"
    
    def get_time(self):
        """
        Gets the current time.
        
        Returns:
            str: Current time as a string
        """
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."
    
    def get_battery_status(self):
        """
        Gets the current battery percentage.
        
        Returns:
            str: Battery status as a string
        """
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                power_plugged = battery.power_plugged
                status = "plugged in" if power_plugged else "not plugged in"
                return f"Battery is at {percent}% and is {status}."
            else:
                return "Battery information is not available. You might be on a desktop computer."
        except Exception as e:
            return f"Failed to get battery status. Error: {str(e)}"