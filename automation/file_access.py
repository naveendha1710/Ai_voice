import os
import glob
import time
from datetime import datetime

class FileAccess:
    """
    Handles file system operations like accessing recent files
    and opening downloads.
    """
    
    def __init__(self):
        """
        Initialize with user directories.
        """
        self.downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        self.documents_dir = os.path.join(os.path.expanduser("~"), "Documents")
    
    def open_last_download(self):
        """
        Opens the most recently downloaded file.
        
        Returns:
            str: Response message
        """
        try:
            # Get all files in the Downloads directory
            files = glob.glob(os.path.join(self.downloads_dir, "*"))
            
            if not files:
                return "No files found in your Downloads folder."
            
            # Sort files by modification time (most recent first)
            latest_file = max(files, key=os.path.getmtime)
            
            # Get the file name without the path
            file_name = os.path.basename(latest_file)
            
            # Open the file with the default application
            os.startfile(latest_file)
            
            return f"Opening your most recent download: {file_name}"
        except Exception as e:
            return f"Failed to open the last downloaded file. Error: {str(e)}"
    
    def list_recent_files(self, count=5, file_type="documents"):
        """
        Lists the most recent files of the specified type.
        
        Args:
            count (int): Number of files to list
            file_type (str): Type of files to list (documents, files, etc.)
            
        Returns:
            str: Response message with the list of files
        """
        try:
            # Determine which directory to search based on file_type
            if file_type.lower() in ["documents", "document", "docs", "doc"]:
                search_dir = self.documents_dir
                search_pattern = "*.*"  # All files
            else:
                # Default to all user files
                search_dir = os.path.expanduser("~")
                search_pattern = "*.*"
            
            # Get all files matching the pattern
            files = []
            for ext in ["*.txt", "*.docx", "*.pdf", "*.xlsx", "*.pptx"]:
                files.extend(glob.glob(os.path.join(search_dir, "**", ext), recursive=True))
            
            if not files:
                return f"No {file_type} found in your {os.path.basename(search_dir)} folder."
            
            # Sort files by modification time (most recent first)
            files.sort(key=os.path.getmtime, reverse=True)
            
            # Limit to the requested count
            recent_files = files[:count]
            
            # Format the response
            response = f"Here are your {count} most recent {file_type}:\n"
            for i, file_path in enumerate(recent_files, 1):
                file_name = os.path.basename(file_path)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M")
                response += f"{i}. {file_name} (modified: {mod_time})\n"
            
            return response
        except Exception as e:
            return f"Failed to list recent {file_type}. Error: {str(e)}"