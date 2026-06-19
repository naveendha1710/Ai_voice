import webbrowser
import urllib.parse

class BrowserControl:
    """
    Handles browser-related operations like opening websites
    and performing searches.
    """
    
    def open_website(self, website):
        """
        Opens the specified website in the default browser.
        
        Args:
            website (str): Website URL to open
            
        Returns:
            str: Response message
        """
        try:
            # Add http:// if not present
            if not website.startswith(('http://', 'https://')):
                website = 'https://' + website
            
            webbrowser.open(website)
            return f"Opening {website}"
        except Exception as e:
            return f"Failed to open {website}. Error: {str(e)}"
    
    def search_google(self, query):
        """
        Searches Google for the specified query.
        
        Args:
            query (str): Search query
            
        Returns:
            str: Response message
        """
        try:
            # Encode the query for URL
            encoded_query = urllib.parse.quote_plus(query)
            search_url = f"https://www.google.com/search?q={encoded_query}"
            
            webbrowser.open(search_url)
            return f"Searching Google for '{query}'"
        except Exception as e:
            return f"Failed to search Google. Error: {str(e)}"
    
    def search_youtube(self, query):
        """
        Searches YouTube for the specified query.
        
        Args:
            query (str): Search query
            
        Returns:
            str: Response message
        """
        try:
            # Encode the query for URL
            encoded_query = urllib.parse.quote_plus(query)
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            
            webbrowser.open(search_url)
            return f"Searching YouTube for '{query}'"
        except Exception as e:
            return f"Failed to search YouTube. Error: {str(e)}"