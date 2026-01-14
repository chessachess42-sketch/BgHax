import socket
import re
import sys
from urllib.parse import urlparse

def extract_hostname(url):
    """
    Extract hostname from various URL formats.
    Handles:
    - Direct IPs (192.168.1.1)
    - Hostnames (example.com)
    - Full URLs (https://example.com/path)
    - URLs with ports (example.com:8080)
    """
    # Remove protocol if present
    if '://' in url:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if hostname:
            return hostname
    else:
        # Handle URLs without protocol but with port
        if ':' in url and '/' not in url.split(':')[0]:
            parts = url.split(':')
            if len(parts) == 2 and parts[1].isdigit():
                return parts[0]
        
        # Handle plain hostnames or IPs
        hostname = url.split('/')[0]
        return hostname
    
    return None

def resolve_ip(hostname):
    """
    Resolve hostname to IP address.
    Returns both IPv4 and IPv6 if available.
    """
    try:
        # Get all address info
        addr_info = socket.getaddrinfo(hostname, None)
        
        # Extract unique IPs
        ips = set()
        for info in addr_info:
            ip = info[4][0]
            ips.add(ip)
        
        return list(ips)
    except socket.gaierror as e:
        return None

def is_valid_ip(ip):
    """
    Validate if string is a valid IP address (IPv4 or IPv6)
    """
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, ip)
            return True
        except socket.error:
            return False

def fetch_ip_from_url(url):
    """
    Main function to fetch IP from any URL format
    """
    # Extract hostname
    hostname = extract_hostname(url)
    
    if not hostname:
        return None, "Invalid URL format"
    
    # Check if it's already an IP
    if is_valid_ip(hostname):
        return [hostname], f"Direct IP: {hostname}"
    
    # Resolve hostname to IP
    ips = resolve_ip(hostname)
    
    if ips:
        return ips, f"Resolved {hostname} to {len(ips)} IP(s)"
    else:
        return None, f"Could not resolve hostname: {hostname}"

def main():
    """
    Command line interface
    """
    if len(sys.argv) < 2:
        print("Usage: python ip_fetcher.py <url_or_hostname>")
        print("Examples:")
        print("  python ip_fetcher.py google.com")
        print("  python ip_fetcher.py https://github.com/user/repo")
        print("  python ip_fetcher.py 192.168.1.1")
        print("  python ip_fetcher.py example.com:8080/path")
        sys.exit(1)
    
    url = sys.argv[1]
    ips, message = fetch_ip_from_url(url)
    
    print(f"Input: {url}")
    print(f"Result: {message}")
    
    if ips:
        print("\nIP Address(es):")
        for i, ip in enumerate(ips, 1):
            print(f"  {i}. {ip}")
            
            # Try to get reverse DNS
            try:
                reverse_dns = socket.gethostbyaddr(ip)[0]
                print(f"     Reverse DNS: {reverse_dns}")
            except:
                pass
    else:
        print("No IP addresses found")
        sys.exit(1)

if __name__ == "__main__":
    main()