@echo off
echo ========================================
echo    Advanced JARVIS AI Assistant
echo ========================================
echo.
echo Choose your interface:
echo 1. Console Mode (Voice + Text)
echo 2. GUI Mode (Visual Interface)
echo 3. Exit
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Starting Advanced JARVIS in Console Mode...
    python advanced_jarvis.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Advanced JARVIS with GUI...
    python jarvis_gui.py
) else if "%choice%"=="3" (
    echo Goodbye!
    exit
) else (
    echo Invalid choice. Please run the script again.
)

pause