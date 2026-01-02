import requests
import re
from bs4 import BeautifulSoup

def get_ip_from_uid(uid):
    # Define the Blockman Go URL pattern
    base_url = f"https://blockmango.com/user/{uid}"

    try:
        # Send a GET request to the Blockman Go user profile page
        response = requests.get(base_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Search for the IP address in the page content
            # This is a hypothetical example; adjust the regular expression as needed
            ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
            ip_address = ip_pattern.search(soup.get_text())

            if ip_address:
                return ip_address.group()
            else:
                return "IP address not found on the page."
        else:
            return f"Failed to retrieve data. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    # Example usage
    user_id = input("6892835886: ")
    ip_address = get_ip_from_uid(user_id)
    print(f"The IP address for user ID {user_id} is: {ip_address}")
