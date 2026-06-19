#!/usr/bin/env python3
"""
Simple launcher for Advanced JARVIS - bypasses debugger issues
"""

import sys
import os

def main():
    print("🤖 JARVIS Launcher")
    print("1. Console Mode")
    print("2. GUI Mode") 
    print("3. Exit")
    
    choice = input("\nSelect mode (1-3): ").strip()
    
    if choice == "1":
        try:
            from advanced_jarvis import main as jarvis_main
            jarvis_main()
        except Exception as e:
            print(f"Error: {e}")
            
    elif choice == "2":
        try:
            from jarvis_gui import main as gui_main
            gui_main()
        except Exception as e:
            print(f"Error: {e}")
            
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()