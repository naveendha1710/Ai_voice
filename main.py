import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Main entry point - redirects to Advanced JARVIS."""
    print("🤖 JARVIS AI Assistant")
    print("=" * 30)
    print("This is the legacy entry point.")
    print("For the full Advanced JARVIS experience, use:")
    print("  • python advanced_jarvis.py (Console Mode)")
    print("  • python jarvis_gui.py (GUI Mode)")
    print("  • start_advanced_jarvis.bat (Choose Mode)")
    print("=" * 30)
    
    choice = input("\nStart Advanced JARVIS now? (y/n): ").lower().strip()
    
    if choice in ['y', 'yes']:
        print("\n🚀 Starting Advanced JARVIS...")
        try:
            from advanced_jarvis import main as advanced_main
            advanced_main()
        except ImportError as e:
            print(f"❌ Error importing Advanced JARVIS: {e}")
            print("Please ensure all dependencies are installed: pip install -r requirements.txt")
        except Exception as e:
            print(f"❌ Error starting Advanced JARVIS: {e}")
    else:
        print("\n👋 Goodbye! Run 'python advanced_jarvis.py' when ready.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")