# 🤖 Advanced JARVIS AI Assistant

A highly advanced, context-aware AI assistant inspired by JARVIS from Iron Man, built with Python and OpenAI integration.

## 🌟 Advanced Features

### 🧠 **Context-Aware Intelligence**
- **Conversation Memory**: Remembers previous interactions and context
- **Follow-up Commands**: Handle commands like "continue with that" or "what was I doing before?"
- **User Preferences**: Learns and adapts to your preferences over time
- **Session Tracking**: Maintains context throughout your session

### 🎯 **Proactive AI Behavior**
- **Smart Reminders**: Set intelligent reminders with natural language
- **System Monitoring**: Proactive alerts for battery, memory, and disk space
- **Time-based Suggestions**: Contextual suggestions based on time of day
- **Idle Detection**: Offers helpful suggestions during idle periods

### 🛠️ **Advanced System Control**
- **Hardware Control**: Volume, brightness, WiFi management
- **System Optimization**: Clean temp files, manage startup programs
- **Process Management**: Monitor and control running applications
- **Screenshot Capture**: Take screenshots on command

### 🎤 **Enhanced Voice Engine**
- **Natural Speech**: Human-like text-to-speech with emphasis
- **Interruption Handling**: Can be interrupted and respond to clarifications
- **Voice Customization**: Adjustable speed, volume, and voice selection
- **Speech Queuing**: Manages multiple speech requests intelligently

### 📋 **Multi-Task Management**
- **Parallel Execution**: Handle multiple commands simultaneously
- **Task Tracking**: Monitor active, queued, and completed tasks
- **Status Updates**: Real-time task progress reporting
- **Task Cancellation**: Cancel queued or running tasks

### 🖥️ **GUI Interface**
- **Real-time Monitoring**: Live console, task, and system logs
- **Visual Controls**: Start/stop JARVIS with GUI buttons
- **Multi-tab Interface**: Organized information display
- **Command Input**: Type commands directly in the GUI

## 🚀 Quick Start

### 1. **Automated Setup**
```bash
python setup.py
```

### 2. **Configure OpenAI API Key**
Edit `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. **Choose Your Interface**

**Console Mode (Voice + Text):**
```bash
python advanced_jarvis.py
```

**GUI Mode (Visual Interface):**
```bash
python jarvis_gui.py
```

**Interactive Launcher:**
```bash
start_advanced_jarvis.bat
```

## 💬 Command Examples

### **Simple Commands**
- "What's the time?"
- "Set volume to 50"
- "Take a screenshot"
- "Clean temp files"
- "System status"

### **Context-Aware Commands**
- "What was I working on earlier?"
- "Continue with that task"
- "Remind me in 30 minutes to check emails"

### **Multi-Step Commands**
- "Search for Python tutorials and open notepad to take notes"
- "Set volume to 80 and also open calculator"
- "Tell me the weather and then save it to a file"

### **System Control**
- "Set brightness to 70"
- "Turn off WiFi"
- "Show me active tasks"
- "Cancel task abc123"

### **Voice Control**
- "Speak slower"
- "Change voice to David"
- "Stop talking"

## 🏗️ Architecture

```
Advanced JARVIS/
├── 🧠 Core Intelligence
│   ├── Context Manager (Memory & Preferences)
│   ├── Proactive Agent (Monitoring & Suggestions)
│   ├── Task Manager (Multi-tasking)
│   ├── Voice Engine (Advanced TTS)
│   └── System Controller (Hardware Control)
├── 🎯 Command Processing
│   ├── Enhanced Commands (Context-aware)
│   ├── GPT Integration (AI Breakdown)
│   └── Action Executor (Real Actions)
├── 🖥️ Interfaces
│   ├── Console Mode (Voice + Text)
│   ├── GUI Mode (Visual Interface)
│   └── Batch Launcher (Choose Mode)
└── 🔧 Automation Modules
    ├── System Control
    ├── File Access
    └── Browser Control
```

## 🔧 Advanced Configuration

### **Voice Customization**
```python
# In user_preferences.json
{
  "voice_speed": 160,
  "voice_volume": 0.9,
  "preferred_voice": "David"
}
```

### **System Monitoring**
```python
# Proactive monitoring settings
{
  "battery_alert_threshold": 20,
  "memory_alert_threshold": 85,
  "reminder_frequency": 30
}
```

### **Task Management**
```python
# Task execution settings
{
  "max_concurrent_tasks": 3,
  "task_timeout": 300,
  "auto_cleanup": true
}
```

## 🛡️ Security Features

- **No eval() execution** of AI-generated code
- **Sanitized JSON parsing** for task lists
- **Input validation** for all system operations
- **Error handling** to prevent crashes
- **Secure API key storage** in .env files
- **Permission-based** system access

## 📊 System Requirements

### **Minimum Requirements**
- Windows 10/11
- Python 3.8+
- 4GB RAM
- Internet connection (for OpenAI)

### **Recommended Requirements**
- Windows 11
- Python 3.10+
- 8GB RAM
- SSD storage
- Microphone (for voice input)
- Speakers/Headphones

## 🔍 Troubleshooting

### **Common Issues**

1. **OpenAI API Issues**
   ```bash
   python test_openai.py
   ```

2. **Voice Engine Problems**
   ```bash
   python -c "import pyttsx3; pyttsx3.init().say('test'); pyttsx3.init().runAndWait()"
   ```

3. **System Control Issues**
   ```bash
   # Run as Administrator for full system control
   ```

4. **GUI Not Starting**
   ```bash
   pip install tkinter
   ```

## 🚀 Future Enhancements

- **Wake Word Detection** ("Hey JARVIS")
- **Email Integration** (Gmail, Outlook)
- **Calendar Management** (Google Calendar, Outlook)
- **Smart Home Control** (IoT devices)
- **Camera Integration** (Computer vision)
- **Mobile App** (Remote control)
- **Plugin System** (Custom extensions)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgements

- Inspired by JARVIS from Iron Man
- Built with Python and OpenAI
- Uses various open-source libraries
- Community contributions welcome

---

**🎯 Ready to experience the future of AI assistants? Start your Advanced JARVIS today!**