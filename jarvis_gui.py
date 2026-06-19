import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue
from datetime import datetime
from advanced_jarvis import AdvancedJARVIS

class JARVISGui:
    """GUI interface for Advanced JARVIS with real-time logs and task panels."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced JARVIS - AI Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a1a')
        
        # Message queue for thread-safe GUI updates
        self.message_queue = queue.Queue()
        
        # JARVIS instance
        self.jarvis = None
        self.jarvis_thread = None
        
        self.setup_gui()
        self.start_message_processor()
        
    def setup_gui(self):
        """Setup the GUI layout."""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="🤖 Advanced JARVIS", 
                              font=('Arial', 20, 'bold'), 
                              fg='#00ff41', bg='#1a1a1a')
        title_label.pack(pady=(0, 10))
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg='#1a1a1a')
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = tk.Label(status_frame, text="Status: Offline", 
                                    font=('Arial', 12), 
                                    fg='#ff4444', bg='#1a1a1a')
        self.status_label.pack(side=tk.LEFT)
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg='#1a1a1a')
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = tk.Button(button_frame, text="Start JARVIS", 
                                     command=self.start_jarvis,
                                     bg='#00ff41', fg='black', 
                                     font=('Arial', 10, 'bold'))
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = tk.Button(button_frame, text="Stop JARVIS", 
                                    command=self.stop_jarvis,
                                    bg='#ff4444', fg='white', 
                                    font=('Arial', 10, 'bold'),
                                    state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Console tab
        console_frame = tk.Frame(notebook, bg='#1a1a1a')
        notebook.add(console_frame, text="Console")
        
        self.console_text = scrolledtext.ScrolledText(console_frame, 
                                                     bg='#000000', fg='#00ff41',
                                                     font=('Consolas', 10),
                                                     wrap=tk.WORD)
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tasks tab
        tasks_frame = tk.Frame(notebook, bg='#1a1a1a')
        notebook.add(tasks_frame, text="Tasks")
        
        self.tasks_text = scrolledtext.ScrolledText(tasks_frame, 
                                                   bg='#000000', fg='#ffff00',
                                                   font=('Consolas', 10),
                                                   wrap=tk.WORD)
        self.tasks_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # System tab
        system_frame = tk.Frame(notebook, bg='#1a1a1a')
        notebook.add(system_frame, text="System")
        
        self.system_text = scrolledtext.ScrolledText(system_frame, 
                                                    bg='#000000', fg='#00ffff',
                                                    font=('Consolas', 10),
                                                    wrap=tk.WORD)
        self.system_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg='#1a1a1a')
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(input_frame, text="Command:", 
                font=('Arial', 10), fg='#ffffff', bg='#1a1a1a').pack(side=tk.LEFT)
        
        self.command_entry = tk.Entry(input_frame, font=('Arial', 10), 
                                     bg='#333333', fg='#ffffff')
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        self.command_entry.bind('<Return>', self.send_command)
        
        self.send_button = tk.Button(input_frame, text="Send", 
                                    command=self.send_command,
                                    bg='#0066cc', fg='white')
        self.send_button.pack(side=tk.RIGHT)
        
        # Initial console message
        self.log_to_console("🤖 Advanced JARVIS GUI Ready")
        self.log_to_console("Click 'Start JARVIS' to begin")
    
    def start_message_processor(self):
        """Start processing messages from queue."""
        self.process_queue()
        self.root.after(100, self.start_message_processor)
    
    def process_queue(self):
        """Process messages from the queue."""
        try:
            while True:
                message_type, message = self.message_queue.get_nowait()
                
                if message_type == "console":
                    self.console_text.insert(tk.END, f"{message}\n")
                    self.console_text.see(tk.END)
                elif message_type == "tasks":
                    self.tasks_text.delete(1.0, tk.END)
                    self.tasks_text.insert(tk.END, message)
                elif message_type == "system":
                    self.system_text.insert(tk.END, f"{message}\n")
                    self.system_text.see(tk.END)
                elif message_type == "status":
                    self.status_label.config(text=f"Status: {message}")
                    if "Online" in message:
                        self.status_label.config(fg='#00ff41')
                    else:
                        self.status_label.config(fg='#ff4444')
                        
        except queue.Empty:
            pass
    
    def log_to_console(self, message):
        """Log message to console."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.message_queue.put(("console", formatted_message))
    
    def update_tasks(self, tasks_info):
        """Update tasks display."""
        self.message_queue.put(("tasks", tasks_info))
    
    def log_system(self, message):
        """Log system message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.message_queue.put(("system", formatted_message))
    
    def update_status(self, status):
        """Update status."""
        self.message_queue.put(("status", status))
    
    def start_jarvis(self):
        """Start JARVIS in a separate thread."""
        if self.jarvis_thread and self.jarvis_thread.is_alive():
            return
        
        self.log_to_console("🚀 Starting Advanced JARVIS...")
        self.update_status("Starting...")
        
        # Create custom JARVIS with GUI integration
        self.jarvis = GUIIntegratedJARVIS(self)
        
        self.jarvis_thread = threading.Thread(target=self.jarvis.start, daemon=True)
        self.jarvis_thread.start()
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
    
    def stop_jarvis(self):
        """Stop JARVIS."""
        if self.jarvis:
            self.log_to_console("🛑 Stopping JARVIS...")
            self.jarvis.running = False
            self.update_status("Stopping...")
        
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def send_command(self, event=None):
        """Send command to JARVIS."""
        command = self.command_entry.get().strip()
        if command and self.jarvis and self.jarvis.running:
            self.log_to_console(f"👤 User: {command}")
            # Process command through JARVIS
            threading.Thread(target=self.jarvis.process_gui_command, args=(command,), daemon=True).start()
            self.command_entry.delete(0, tk.END)
    
    def run(self):
        """Run the GUI."""
        self.root.mainloop()

class GUIIntegratedJARVIS(AdvancedJARVIS):
    """JARVIS with GUI integration."""
    
    def __init__(self, gui):
        self.gui = gui
        super().__init__()
        
        # Override voice engine to also log to GUI
        original_speak = self.voice_engine.speak
        
        def gui_speak(text, priority='normal', interruptible=True):
            self.gui.log_to_console(f"🤖 JARVIS: {text}")
            original_speak(text, priority, interruptible)
        
        self.voice_engine.speak = gui_speak
    
    def start(self):
        """Start with GUI integration."""
        self.gui.update_status("Online")
        self.gui.log_to_console("✅ Advanced JARVIS Online")
        super().start()
        self.gui.update_status("Offline")
        self.gui.log_to_console("❌ JARVIS Offline")
    
    def process_gui_command(self, command):
        """Process command from GUI."""
        try:
            self._process_command_with_context(command)
            
            # Update tasks display
            if hasattr(self, 'task_manager'):
                tasks_status = self.task_manager.get_task_status()
                self.gui.update_tasks(tasks_status)
                
        except Exception as e:
            self.gui.log_to_console(f"❌ Error: {e}")

def main():
    """Main entry point for GUI version."""
    app = JARVISGui()
    app.run()

if __name__ == "__main__":
    main()
    original_speak(text, priority, interruptible)
    self.voice_engine.speak = gui_speak
    
    def start(self):
        """Start with GUI integration."""
        self.gui.update_status("Online")
        self.gui.log_to_console("✅ Advanced JARVIS Online")
        super().start()
        self.gui.update_status("Offline")
        self.gui.log_to_console("❌ JARVIS Offline")
    
    def process_gui_command(self, command):
        """Process command from GUI."""
        try:
            self._process_command_with_context(command)
            
            # Update tasks display
            if hasattr(self, 'task_manager'):
                tasks_status = self.task_manager.get_task_status()
                self.gui.update_tasks(tasks_status)
                
        except Exception as e:
            self.gui.log_to_console(f"❌ Error: {e}")

def main():
    """Main entry point for GUI version."""
    app = JARVISGui()
    app.run()

if __name__ == "__main__":
    main()