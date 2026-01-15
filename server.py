#!/usr/bin/env python3
"""
Simple HTTP Chat Server
Handles message posting and retrieval for a basic chat system.
"""

import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from urllib.parse import parse_qs, urlparse

# In-memory message storage
messages = []
messages_lock = threading.Lock()

class ChatHandler(BaseHTTPRequestHandler):
    """HTTP request handler for chat operations."""
    
    def _send_response(self, status_code, data):
        """Send JSON response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def _send_html(self, html_content):
        """Send HTML response."""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def do_GET(self):
        """Handle GET requests - retrieve messages or serve chat UI."""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            # Serve a simple HTML chat interface
            self._serve_chat_ui()
        elif parsed_path.path == '/messages':
            # Return all messages
            query_params = parse_qs(parsed_path.query)
            since_index = int(query_params.get('since', [0])[0])
            
            with messages_lock:
                new_messages = messages[since_index:]
            
            self._send_response(200, {
                'messages': new_messages,
                'total': len(messages)
            })
        elif parsed_path.path == '/status':
            self._send_response(200, {'status': 'online', 'message_count': len(messages)})
        else:
            self._send_response(404, {'error': 'Not found'})
    
    def do_POST(self):
        """Handle POST requests - send new messages."""
        if self.path == '/send':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(post_data)
                username = data.get('username', 'Anonymous')
                message = data.get('message', '')
                
                if not message.strip():
                    self._send_response(400, {'error': 'Message cannot be empty'})
                    return
                
                new_message = {
                    'id': len(messages),
                    'username': username,
                    'message': message,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                with messages_lock:
                    messages.append(new_message)
                
                print(f"[{new_message['timestamp']}] {username}: {message}")
                self._send_response(200, {'success': True, 'message': new_message})
                
            except json.JSONDecodeError:
                self._send_response(400, {'error': 'Invalid JSON'})
        else:
            self._send_response(404, {'error': 'Not found'})
    
    def _serve_chat_ui(self):
        """Serve a simple web-based chat interface."""
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTTP Chat</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #e8e8e8;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        h1 {
            text-align: center;
            color: #00d9ff;
            font-weight: 300;
            letter-spacing: 4px;
            margin-bottom: 20px;
            text-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
        }
        .chat-box {
            flex: 1;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid #00d9ff33;
            border-radius: 12px;
            padding: 20px;
            overflow-y: auto;
            margin-bottom: 20px;
            max-height: 60vh;
            backdrop-filter: blur(10px);
        }
        .message {
            margin-bottom: 15px;
            padding: 12px 16px;
            background: rgba(0, 217, 255, 0.05);
            border-left: 3px solid #00d9ff;
            border-radius: 0 8px 8px 0;
            animation: slideIn 0.3s ease;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-10px); }
            to { opacity: 1; transform: translateX(0); }
        }
        .message .username {
            color: #00d9ff;
            font-weight: 600;
            font-size: 0.9em;
        }
        .message .time {
            color: #666;
            font-size: 0.75em;
            margin-left: 10px;
        }
        .message .text {
            margin-top: 6px;
            color: #d0d0d0;
            line-height: 1.5;
        }
        .input-area {
            display: flex;
            gap: 10px;
        }
        input, button {
            padding: 14px 18px;
            border: 1px solid #00d9ff44;
            border-radius: 8px;
            font-family: inherit;
            font-size: 14px;
            background: rgba(0, 0, 0, 0.4);
            color: #e8e8e8;
            outline: none;
            transition: all 0.2s;
        }
        input:focus {
            border-color: #00d9ff;
            box-shadow: 0 0 15px rgba(0, 217, 255, 0.2);
        }
        input::placeholder { color: #666; }
        #username { width: 140px; }
        #message { flex: 1; }
        button {
            background: linear-gradient(135deg, #00d9ff 0%, #0099cc 100%);
            color: #0f0f0f;
            font-weight: 600;
            cursor: pointer;
            border: none;
            min-width: 100px;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 217, 255, 0.4);
        }
        .status {
            text-align: center;
            color: #00d9ff;
            font-size: 0.8em;
            margin-bottom: 10px;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ HTTP CHAT</h1>
        <div class="status" id="status">Connecting...</div>
        <div class="chat-box" id="chatBox"></div>
        <div class="input-area">
            <input type="text" id="username" placeholder="Username" value="User">
            <input type="text" id="message" placeholder="Type your message..." autofocus>
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script>
        let lastMessageCount = 0;
        
        async function fetchMessages() {
            try {
                const res = await fetch('/messages?since=' + lastMessageCount);
                const data = await res.json();
                
                if (data.messages.length > 0) {
                    const chatBox = document.getElementById('chatBox');
                    data.messages.forEach(msg => {
                        const div = document.createElement('div');
                        div.className = 'message';
                        div.innerHTML = `
                            <span class="username">${escapeHtml(msg.username)}</span>
                            <span class="time">${msg.timestamp}</span>
                            <div class="text">${escapeHtml(msg.message)}</div>
                        `;
                        chatBox.appendChild(div);
                    });
                    chatBox.scrollTop = chatBox.scrollHeight;
                    lastMessageCount = data.total;
                }
                document.getElementById('status').textContent = `Connected • ${data.total} messages`;
            } catch (e) {
                document.getElementById('status').textContent = 'Disconnected';
            }
        }
        
        async function sendMessage() {
            const username = document.getElementById('username').value || 'Anonymous';
            const message = document.getElementById('message').value;
            
            if (!message.trim()) return;
            
            try {
                await fetch('/send', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username, message})
                });
                document.getElementById('message').value = '';
                fetchMessages();
            } catch (e) {
                alert('Failed to send message');
            }
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        document.getElementById('message').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
        // Poll for new messages every 2 seconds
        setInterval(fetchMessages, 2000);
        fetchMessages();
    </script>
</body>
</html>'''
        self._send_html(html)
    
    def log_message(self, format, *args):
        """Override to customize logging."""
        pass  # Suppress default logging


def run_server(host='0.0.0.0', port=8080):
    """Start the chat server."""
    server = HTTPServer((host, port), ChatHandler)
    print(f"""
╔══════════════════════════════════════════════════════════╗
║              HTTP Chat Server Started                    ║
╠══════════════════════════════════════════════════════════╣
║  Server running at: http://localhost:{port}               ║
║                                                          ║
║  Endpoints:                                              ║
║    GET  /          - Web chat interface                  ║
║    GET  /messages  - Fetch all messages                  ║
║    GET  /status    - Server status                       ║
║    POST /send      - Send a message                      ║
║                                                          ║
║  Press Ctrl+C to stop the server                         ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer shutting down...")
        server.shutdown()


if __name__ == '__main__':
    run_server()
