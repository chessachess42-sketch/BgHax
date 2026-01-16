import requests
import json
import hashlib
import time
from typing import Dict, Optional, Union

class BlockmanGoAPI:
    """
   Author- Act

 A Python wrapper for interacting with the real Blockman Go API.
    This tool connects to the official Blockman Go API endpoints.
    """
    
    def __init__(self, base_url: str = "https://gw.sandboxol.com"):
        """
        Initialize the API client.
        
        Args:
            base_url: The base URL for the Blockman Go API
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.user_id = None
        self.access_token = None
        self.device_id = None
    
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
        This is required for some endpoints as mentioned in the search results.
        
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
        url = f"{self.base_url}/{endpoint}"
        
        if require_sign and data:
            timestamp = str(int(time.time()))
            sign = self._generate_sign(data)
            self.session.headers["X-Sign"] = sign
            self.session.headers["X-Timestamp"] = timestamp
        
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_user_info(self) -> Dict:
        """
        Get current user information.
        
        Returns:
            User information as a dictionary
        """
        return self.get("v1/user/info")
    
    def get_server_list(self) -> Dict:
        """
        Get the list of available servers.
        
        Returns:
            Server list as a dictionary
        """
        return self.get("v1/server/list")
    
    def get_game_list(self) -> Dict:
        """
        Get the list of available games.
        
        Returns:
            Game list as a dictionary
        """
        return self.get("v1/game/list")
    
    def get_leaderboard(self, game_id: str, limit: int = 10) -> Dict:
        """
        Get the leaderboard for a specific game.
        
        Args:
            game_id: The ID of the game
            limit: Maximum number of entries to return
            
        Returns:
            Leaderboard data as a dictionary
        """
        params = {"gameId": game_id, "limit": limit}
        return self.get("v1/leaderboard", params)
    
    def get_room_info(self, room_id: str) -> Dict:
        """
        Get information about a specific room.
        
        Args:
            room_id: The ID of the room
            
        Returns:
            Room information as a dictionary
        """
        return self.get(f"v1/room/{room_id}")
    
    def join_room(self, room_id: str, password: Optional[str] = None) -> Dict:
        """
        Join a specific room.
        
        Args:
            room_id: The ID of the room to join
            password: Optional password if the room is private
            
        Returns:
            Response as a dictionary
        """
        data = {"roomId": room_id}
        if password:
            data["password"] = password
        return self.post("v1/room/join", data, require_sign=True)
    
    def get_news(self) -> Dict:
        """
        Get news and announcements.
        
        Returns:
            News data as a dictionary
        """
        return self.get("v1/news/list")
    
    def get_shop_items(self) -> Dict:
        """
        Get items from the shop.
        
        Returns:
            Shop items data as a dictionary
        """
        return self.get("v1/shop/items")

# Example usage
if __name__ == "__main__":
    # Initialize the API client with the official endpoint
    api = BlockmanGoAPI()
    
    # If you have authentication credentials, uncomment the following line:
    # api.set_auth("your_user_id", "your_access_token", "your_device_id")
    
    try:
        # Get server list
        print("Server List:")
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
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")