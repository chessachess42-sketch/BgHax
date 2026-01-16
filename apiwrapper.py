import requests
import json
import hashlib
import time
from typing import Dict, Optional, Union, List

class BlockmanGoAPI:
    """
    Author- Act 

A Python wrapper for interacting with the real Blockman Go API.
    This tool connects to the official Blockman Go API endpoints.
    """
    
    # Possible base URLs for Blockman Go API
    POSSIBLE_BASE_URLS = [
        "https://gw.sandboxol.com",
        "https://api.blockmango.com",
        "https://api.blockman-go.com",
        "https://blockman-go.com/api",
        "https://gw.blockmango.com",
        "https://api.sandboxol.com",
    ]
    
    # Possible endpoint patterns
    POSSIBLE_ENDPOINT_PATTERNS = [
        "{endpoint}",
        "v1/{endpoint}",
        "api/v1/{endpoint}",
        "api/{endpoint}",
        "blockman/{endpoint}",
    ]
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize the API client.
        
        Args:
            base_url: The base URL for the Blockman Go API (optional)
        """
        self.base_url = base_url or self.POSSIBLE_BASE_URLS[0]
        self.session = requests.Session()
        self.user_id = None
        self.access_token = None
        self.device_id = None
        self.working_endpoints = {}
    
    def set_auth(self, user_id: str, access_token: str, device_id: str = None) -> None:
        """
        Set authentication credentials for API requests.
        
        Args:
            user_id: Your Blockman Go user ID
            access_token: Your access token
            device_id: Optional device ID for additional authentication
        """
        self.user_id = user_id
        self.access_token = access_token
        self.device_id = device_id
        
        # Set required headers for authentication
        self.session.headers.update({
            "userId": user_id,
            "accessToken": access_token,
            "User-Agent": "BlockmanGO/3.3.2 (Android)",
            "Content-Type": "application/json"
        })
        
        if device_id:
            self.session.headers["deviceId"] = device_id
    
    def _generate_sign(self, params: Dict) -> str:
        """
        Generate X-Sign header for API authentication.
        This is required for some endpoints.
        
        Args:
            params: Parameters to include in the signature
            
        Returns:
            Generated signature string
        """
        # This is a simplified version of sign generation
        # The actual algorithm might be more complex
        timestamp = str(int(time.time()))
        params_str = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
        sign_string = f"{self.access_token}{timestamp}{params_str}"
        return hashlib.md5(sign_string.encode()).hexdigest()
    
    def discover_api_endpoints(self) -> Dict:
        """
        Try to discover the correct API endpoints by testing different patterns.
        
        Returns:
            Dictionary of working endpoints
        """
        print("Discovering API endpoints...")
        
        # Common endpoints to test
        test_endpoints = [
            "server/list",
            "game/list",
            "user/info",
            "news/list",
        ]
        
        working_endpoints = {}
        
        for base_url in self.POSSIBLE_BASE_URLS:
            print(f"Testing base URL: {base_url}")
            
            for endpoint in test_endpoints:
                for pattern in self.POSSIBLE_ENDPOINT_PATTERNS:
                    full_endpoint = pattern.format(endpoint=endpoint)
                    url = f"{base_url}/{full_endpoint}"
                    
                    try:
                        response = self.session.get(url, timeout=5)
                        if response.status_code == 200:
                            print(f"✓ Working endpoint found: {url}")
                            working_endpoints[endpoint] = full_endpoint
                            break
                    except requests.exceptions.RequestException:
                        pass
                
                # If we found a working endpoint for this base URL, assume it's the correct one
                if endpoint in working_endpoints and working_endpoints[endpoint]:
                    self.base_url = base_url
                    self.working_endpoints = working_endpoints
                    print(f"Using base URL: {base_url}")
                    return working_endpoints
        
        print("Could not find working endpoints. You may need to provide the correct base URL.")
        return {}
    
    def get(self, endpoint: str, params: Optional[Dict] = None, require_sign: bool = False) -> Dict:
        """
        Send a GET request to the API.
        
        Args:
            endpoint: The API endpoint to request
            params: Optional parameters to include in the request
            require_sign: Whether to generate X-Sign header
            
        Returns:
            The JSON response from the API
        """
        # Use discovered endpoint pattern if available
        if endpoint in self.working_endpoints:
            endpoint = self.working_endpoints[endpoint]
        
        url = f"{self.base_url}/{endpoint}"
        
        if require_sign and params:
            timestamp = str(int(time.time()))
            sign = self._generate_sign(params)
            self.session.headers["X-Sign"] = sign
            self.session.headers["X-Timestamp"] = timestamp
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint: str, data: Optional[Dict] = None, require_sign: bool = False) -> Dict:
        """
        Send a POST request to the API.
        
        Args:
            endpoint: The API endpoint to request
            data: Optional data to include in the request
            require_sign: Whether to generate X-Sign header
            
        Returns:
            The JSON response from the API
        """
        # Use discovered endpoint pattern if available
        if endpoint in self.working_endpoints:
            endpoint = self.working_endpoints[endpoint]
        
        url = f"{self.base_url}/{endpoint}"
        
        if require_sign and data:
            timestamp = str(int(time.time()))
            sign = self._generate_sign(data)
            self.session.headers["X-Sign"] = sign
            self.session.headers["X-Timestamp"] = timestamp
        
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_server_list(self) -> Dict:
        """
        Get the list of available servers.
        
        Returns:
            Server list as a dictionary
        """
        return self.get("server/list")
    
    def get_game_list(self) -> Dict:
        """
        Get the list of available games.
        
        Returns:
            Game list as a dictionary
        """
        return self.get("game/list")
    
    def get_user_info(self) -> Dict:
        """
        Get current user information.
        
        Returns:
            User information as a dictionary
        """
        return self.get("user/info")
    
    def get_news(self) -> Dict:
        """
        Get news and announcements.
        
        Returns:
            News data as a dictionary
        """
        return self.get("news/list")

# Example usage
if __name__ == "__main__":
    # Initialize the API client
    api = BlockmanGoAPI()
    
    # If you have authentication credentials, uncomment the following line:
    # api.set_auth("your_user_id", "your_access_token", "your_device_id")
    
    try:
        # Try to discover working endpoints
        working_endpoints = api.discover_api_endpoints()
        
        if working_endpoints:
            # Get server list
            print("\nServer List:")
            servers = api.get_server_list()
            print(json.dumps(servers, indent=2))
            
            # Get game list
            print("\nGame List:")
            games = api.get_game_list()
            print(json.dumps(games, indent=2))
            
            # Get news
            print("\nNews:")
            news = api.get_news()
            print(json.dumps(news, indent=2))
            
            # Get user info (if authenticated)
            # print("\nUser Info:")
            # user_info = api.get_user_info()
            # print(json.dumps(user_info, indent=2))
        else:
            print("Could not find working endpoints. You may need to:")
            print("1. Check the official Blockman Go app for the correct API endpoints")
            print("2. Use a network traffic analyzer to capture the actual API calls")
            print("3. Provide the correct base URL manually")
            
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")