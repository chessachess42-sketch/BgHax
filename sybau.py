#!/usr/bin/env python3

import subprocess
import sys

def run_metasploit_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.stderr.decode('utf-8')

def main():
    # Start Metasploit console
    msfconsole_output = run_metasploit_command('msfconsole -q')

    if "msf > " not in msfconsole_output:
        print("Failed to start Metasploit console.")
        sys.exit(1)

    # Example command to use Metasploit
    msf_command = 'use auxiliary/scanner/portscan/syn'
    msfconsole_output += run_metasploit_command(f'echo "{msf_command}" | msfconsole -q')

    # Set options for the module
    msf_options = {
        'RHOSTS': '192.168.1.1-254',  # Target IP range
        'THREADS': '10'  # Number of threads
    }
    for option, value in msf_options.items():
        msfconsole_output += run_metasploit_command(f'echo "set {option} {value}" | msfconsole -q')

    # Run the module
    msfconsole_output += run_metasploit_command('echo "run" | msfconsole -q')

    print(msfconsole_output)

if __name__ == "__main__":
    main()