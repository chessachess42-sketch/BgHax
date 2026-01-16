#!/usr/bin/env python3
import os
import sys
import time
import json
import requests
import subprocess
from datetime import datetime

class OTGUnlocker:
    def __init__(self):
        self.target_device = None
        self.api_endpoint = "https://api.github.com"  # GitHub API endpoint
        self.session = requests.Session()
        self.attempts = 0
        self.success = False
        self.start_time = None
        self.results = []
        
    def setup_github_environment(self):
        """Setup environment for GitHub-based execution"""
        print("Initializing GitHub-based execution environment...")
        
        # Check if running in GitHub Actions
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            print("Detected GitHub Actions environment")
            print(f"Repository: {os.environ.get('GITHUB_REPOSITORY', 'Unknown')}")
            print(f"Workflow: {os.environ.get('GITHUB_WORKFLOW', 'Unknown')}")
            return True
        
        # Check for GitHub token
        if not os.environ.get('GITHUB_TOKEN'):
            print("Warning: No GITHUB_TOKEN found. Some features may not work.")
            return False
            
        return True
    
    def register_device(self, device_id):
        """Register a device for unlocking via GitHub API"""
        if not os.environ.get('GITHUB_TOKEN'):
            print("Cannot register device without GitHub token")
            return False
            
        headers = {
            "Authorization": f"token {os.environ.get('GITHUB_TOKEN')}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Create a new issue to register the device
        data = {
            "title": f"Device Registration: {device_id}",
            "body": f"Registering device {device_id} for remote unlocking via OTG.\nTimestamp: {datetime.now().isoformat()}",
            "labels": ["device-registration", "otg-unlock"]
        }
        
        try:
            repo = os.environ.get('GITHUB_REPOSITORY', 'yourusername/yourrepo')
            response = self.session.post(
                f"{self.api_endpoint}/repos/{repo}/issues",
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                issue_data = response.json()
                print(f"Device registered successfully. Issue ID: {issue_data['id']}")
                return issue_data['id']
            else:
                print(f"Failed to register device: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error registering device: {str(e)}")
            return False
    
    def send_unlock_command(self, device_id, pin):
        """Send unlock command to device via GitHub API"""
        if not os.environ.get('GITHUB_TOKEN'):
            print("Cannot send command without GitHub token")
            return False
            
        headers = {
            "Authorization": f"token {os.environ.get('GITHUB_TOKEN')}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Create a new issue with the unlock command
        data = {
            "title": f"Unlock Command: {device_id}",
            "body": f"Execute unlock command on device {device_id} with PIN: {pin}\nTimestamp: {datetime.now().isoformat()}",
            "labels": ["unlock-command", "otg-unlock"]
        }
        
        try:
            repo = os.environ.get('GITHUB_REPOSITORY', 'yourusername/yourrepo')
            response = self.session.post(
                f"{self.api_endpoint}/repos/{repo}/issues",
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                issue_data = response.json()
                print(f"Unlock command sent successfully. Issue ID: {issue_data['id']}")
                return issue_data['id']
            else:
                print(f"Failed to send unlock command: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error sending unlock command: {str(e)}")
            return False
    
    def check_unlock_status(self, command_id):
        """Check if unlock command was successful via GitHub API"""
        if not os.environ.get('GITHUB_TOKEN'):
            print("Cannot check status without GitHub token")
            return False
            
        headers = {
            "Authorization": f"token {os.environ.get('GITHUB_TOKEN')}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            repo = os.environ.get('GITHUB_REPOSITORY', 'yourusername/yourrepo')
            response = self.session.get(
                f"{self.api_endpoint}/repos/{repo}/issues/{command_id}/comments",
                headers=headers
            )
            
            if response.status_code == 200:
                comments = response.json()
                for comment in comments:
                    if "SUCCESS" in comment['body'].upper():
                        print(f"Unlock successful: {comment['body']}")
                        return True
                    elif "FAILED" in comment['body'].upper():
                        print(f"Unlock failed: {comment['body']}")
                        return False
                
                # No status comment found yet
                print("No status update received yet")
                return None
            else:
                print(f"Failed to check status: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error checking status: {str(e)}")
            return False
    
    def brute_force_pin(self, device_id, pin_length=4):
        """Brute force PIN using GitHub API"""
        print(f"Starting brute force attack on device {device_id}")
        print(f"PIN length: {pin_length} digits")
        
        self.start_time = time.time()
        self.attempts = 0
        
        # Generate all possible PIN combinations
        digits = '0123456789'
        
        def generate_pins(length):
            if length == 1:
                for d in digits:
                    yield d
            else:
                for prefix in generate_pins(length-1):
                    for d in digits:
                        yield prefix + d
        
        for pin in generate_pins(pin_length):
            if self.success:
                break
                
            self.attempts += 1
            print(f"Attempt #{self.attempts}: Trying PIN {pin}")
            
            # Send unlock command
            command_id = self.send_unlock_command(device_id, pin)
            if not command_id:
                print("Failed to send unlock command")
                continue
            
            # Wait for status update
            status = None
            max_wait = 30  # Maximum wait time in seconds
            wait_time = 0
            
            while status is None and wait_time < max_wait:
                time.sleep(2)
                wait_time += 2
                status = self.check_unlock_status(command_id)
            
            if status:
                self.success = True
                elapsed_time = time.time() - self.start_time
                print(f"\nSUCCESS! Device unlocked with PIN: {pin}")
                print(f"Total attempts: {self.attempts}")
                print(f"Time elapsed: {elapsed_time:.2f} seconds")
                
                # Store result
                self.results.append({
                    'pin': pin,
                    'attempts': self.attempts,
                    'time': elapsed_time,
                    'success': True
                })
                return True
            elif status is False:
                # PIN was incorrect
                print(f"PIN {pin} was incorrect")
                self.results.append({
                    'pin': pin,
                    'attempts': self.attempts,
                    'time': time.time() - self.start_time,
                    'success': False
                })
                
        if not self.success:
            elapsed_time = time.time() - self.start_time
            print(f"\nFailed to unlock device after {self.attempts} attempts")
            print(f"Time elapsed: {elapsed_time:.2f} seconds")
            
        return False
    
    def save_results(self):
        """Save results to a file"""
        results_file = f"unlock_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump({
                'device': self.target_device,
                'attempts': self.attempts,
                'success': self.success,
                'start_time': self.start_time,
                'results': self.results
            }, f, indent=2)
        print(f"Results saved to {results_file}")
    
    def run(self):
        """Main method to run the unlocker"""
        print("OTG Phone Unlocker - GitHub Edition")
        print("===================================")
        
        # Setup GitHub environment
        if not self.setup_github_environment():
            print("Failed to setup GitHub environment")
            return
            
        # Get device ID
        device_id = input("Enter device ID to unlock: ")
        if not device_id:
            print("No device ID provided")
            return
            
        self.target_device = device_id
        
        # Register device
        registration_id = self.register_device(device_id)
        if not registration_id:
            print("Failed to register device")
            return
            
        # Get PIN length
        try:
            pin_length = int(input("Enter PIN length (default 4): ") or "4")
        except ValueError:
            print("Invalid PIN length, using default (4)")
            pin_length = 4
            
        # Start brute force attack
        self.brute_force_pin(device_id, pin_length)
        
        # Save results
        self.save_results()

if __name__ == "__main__":
    print("OTG Phone Unlocker - GitHub Edition")
    print("===================================")