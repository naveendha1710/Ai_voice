import os
import subprocess
import psutil
import winreg
from ctypes import windll

class AdvancedSystemController:
    """Advanced system control capabilities."""
    
    def __init__(self):
        self.running_processes = {}
    
    def set_volume(self, level: int):
        """Set system volume (0-100)."""
        try:
            # Use Windows API to set volume
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, None, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            volume.SetMasterScalarVolume(level / 100.0, None)
            return f"Volume set to {level}%"
        except ImportError:
            # Fallback using nircmd if available
            try:
                subprocess.run(['nircmd', 'setsysvolume', str(int(level * 655.35))], check=True)
                return f"Volume set to {level}%"
            except:
                return "Volume control not available. Install pycaw package for full functionality."
    
    def set_brightness(self, level: int):
        """Set screen brightness (0-100)."""
        try:
            # Use WMI to control brightness
            import wmi
            c = wmi.WMI(namespace='wmi')
            methods = c.WmiMonitorBrightnessMethods()[0]
            methods.WmiSetBrightness(level, 0)
            return f"Brightness set to {level}%"
        except ImportError:
            return "Brightness control requires WMI package. Install with: pip install WMI"
        except Exception as e:
            return f"Could not set brightness: {str(e)}"
    
    def toggle_wifi(self, enable: bool = None):
        """Toggle WiFi on/off."""
        try:
            if enable is None:
                # Toggle current state
                result = subprocess.run(['netsh', 'interface', 'show', 'interface'], 
                                      capture_output=True, text=True)
                wifi_enabled = 'Wi-Fi' in result.stdout and 'Connected' in result.stdout
                enable = not wifi_enabled
            
            action = 'enable' if enable else 'disable'
            subprocess.run(['netsh', 'interface', 'set', 'interface', 'Wi-Fi', action], check=True)
            status = "enabled" if enable else "disabled"
            return f"WiFi {status}"
        except Exception as e:
            return f"Could not toggle WiFi: {str(e)}"
    
    def get_system_info(self):
        """Get comprehensive system information."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('C:')
            battery = psutil.sensors_battery()
            
            info = f"CPU: {cpu_percent}%, RAM: {memory.percent}%, "
            info += f"Disk: {(disk.used/disk.total)*100:.1f}%"
            
            if battery:
                info += f", Battery: {battery.percent}%"
                if battery.power_plugged:
                    info += " (charging)"
            
            return info
        except Exception as e:
            return f"Could not get system info: {str(e)}"
    
    def clean_temp_files(self):
        """Clean temporary files."""
        try:
            temp_dirs = [
                os.environ.get('TEMP', ''),
                os.environ.get('TMP', ''),
                'C:\\Windows\\Temp'
            ]
            
            cleaned_count = 0
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            try:
                                os.remove(os.path.join(root, file))
                                cleaned_count += 1
                            except:
                                pass
            
            return f"Cleaned {cleaned_count} temporary files"
        except Exception as e:
            return f"Could not clean temp files: {str(e)}"
    
    def manage_startup_programs(self, action: str, program_name: str = None):
        """Manage startup programs."""
        try:
            startup_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            
            if action == "list":
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_key) as key:
                    programs = []
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            programs.append(name)
                            i += 1
                        except WindowsError:
                            break
                    return f"Startup programs: {', '.join(programs)}"
            
            elif action == "disable" and program_name:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_key, 0, winreg.KEY_SET_VALUE) as key:
                    try:
                        winreg.DeleteValue(key, program_name)
                        return f"Disabled {program_name} from startup"
                    except FileNotFoundError:
                        return f"Program {program_name} not found in startup"
            
        except Exception as e:
            return f"Could not manage startup programs: {str(e)}"
    
    def take_screenshot(self, filename: str = None):
        """Take a screenshot."""
        try:
            import pyautogui
            if not filename:
                from datetime import datetime
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            return f"Screenshot saved as {filename}"
        except ImportError:
            return "Screenshot requires pyautogui package"
        except Exception as e:
            return f"Could not take screenshot: {str(e)}"