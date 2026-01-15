#!/usr/bin/env python3
"""
Simple HTTP Chat Client
Command-line client for interacting with the chat server.
"""

import json
import sys
import threading
import time
import urllib.request
import urllib.error

class ChatClient:
    """HTTP Chat Client for sending and receiving messages."""
    
    def __init__(self, server_url='http://localhost:8080'):
        self.server_url = server_url.rstrip('/')
        self.username = 'Anonymous'
        self.last_message_id = 0
        self.running = True
    
    def send_message(self, message):
        """Send a message to the server."""
        data = json.dumps({
            'username': self.username,
            'message': message
        }).encode('utf-8')
        
        try:
            req = urllib.request.Request(
                f'{self.server_url}/send',
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.URLError as e:
            print(f"\n❌ Failed to send message: {e}")
            return None
    
    def get_messages(self, since=0):
        """Fetch messages from the server."""
        try:
            url = f'{self.server_url}/messages?since={since}'
            with urllib.request.urlopen(url, timeout=5) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.URLError:
            return None
    
    def get_status(self):
        """Get server status."""
        try:
            url = f'{self.server_url}/status'
            with urllib.request.urlopen(url, timeout=5) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.URLError:
            return None
    
    def poll_messages(self):
        """Continuously poll for new messages in background."""
        while self.running:
            data = self.get_messages(self.last_message_id)
            if data and data.get('messages'):
                for msg in data['messages']:
                    if msg['username'] != self.username:  # Don't show own messages again
                        print(f"\n\033[36m[{msg['timestamp']}] {msg['username']}: {msg['message']}\033[0m")
                        print(f"\n{self.username}> ", end='', flush=True)
                self.last_message_id = data.get('total', self.last_message_id)
            time.sleep(2)
    
    def run_interactive(self):
        """Run the interactive chat client."""
        print("""
╔══════════════════════════════════════════════════════════╗
║              HTTP Chat Client                            ║
╠══════════════════════════════════════════════════════════╣
║  Commands:                                               ║
║    /name <username>  - Change your username              ║
║    /status           - Check server status               ║
║    /history          - Show message history              ║
║    /clear            - Clear screen                      ║
║    /quit or /exit    - Exit the client                   ║
║                                                          ║
║  Just type to send messages!                             ║
╚══════════════════════════════════════════════════════════╝
        """)
        
        # Check server connection
        status = self.get_status()
        if status:
            print(f"✅ Connected to server: {self.server_url}")
            print(f"📊 Current message count: {status.get('message_count', 0)}")
        else:
            print(f"❌ Cannot connect to server at {self.server_url}")
            print("   Make sure the server is running!")
            return
        
        # Get username
        name = input("\nEnter your username (or press Enter for 'Anonymous'): ").strip()
        self.username = name if name else 'Anonymous'
        print(f"\n👋 Welcome, {self.username}!")
        
        # Load existing messages
        data = self.get_messages()
        if data and data.get('messages'):
            print(f"\n📜 Loading {len(data['messages'])} previous messages...\n")
            for msg in data['messages'][-10:]:  # Show last 10 messages
                print(f"  [{msg['timestamp']}] {msg['username']}: {msg['message']}")
            self.last_message_id = data.get('total', 0)
            print()
        
        # Start background polling
        poll_thread = threading.Thread(target=self.poll_messages, daemon=True)
        poll_thread.start()
        
        # Main input loop
        try:
            while True:
                user_input = input(f"{self.username}> ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    cmd_parts = user_input.split(' ', 1)
                    cmd = cmd_parts[0].lower()
                    
                    if cmd in ['/quit', '/exit']:
                        print("\n👋 Goodbye!")
                        break
                    elif cmd == '/name':
                        if len(cmd_parts) > 1 and cmd_parts[1].strip():
                            self.username = cmd_parts[1].strip()
                            print(f"✅ Username changed to: {self.username}")
                        else:
                            print("Usage: /name <new_username>")
                    elif cmd == '/status':
                        status = self.get_status()
                        if status:
                            print(f"✅ Server: {status.get('status', 'unknown')}")
                            print(f"📊 Messages: {status.get('message_count', 0)}")
                        else:
                            print("❌ Cannot reach server")
                    elif cmd == '/history':
                        data = self.get_messages()
                        if data and data.get('messages'):
                            print(f"\n📜 All {len(data['messages'])} messages:\n")
                            for msg in data['messages']:
                                print(f"  [{msg['timestamp']}] {msg['username']}: {msg['message']}")
                            print()
                        else:
                            print("No messages yet!")
                    elif cmd == '/clear':
                        print('\033[2J\033[H', end='')  # Clear terminal
                    else:
                        print(f"Unknown command: {cmd}")
                else:
                    # Send message
                    result = self.send_message(user_input)
                    if result and result.get('success'):
                        self.last_message_id += 1
                    
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
        finally:
            self.running = False


def main():
    """Main entry point."""
    server_url = 'http://localhost:8080'
    
    # Allow custom server URL via command line
    if len(sys.argv) > 1:
        server_url = sys.argv[1]
    
    client = ChatClient(server_url)
    client.run_interactive()


if __name__ == '__main__':
    main()
