# HTTP Client-Server Chat Application

A simple real-time chat application using Python's built-in HTTP server capabilities. No external dependencies required!

## 📁 Files

| File | Description |
|------|-------------|
| `server.py` | HTTP server that handles messages and serves a web UI |
| `client.py` | Command-line chat client |
| `INSTRUCTIONS.md` | This file |

---

## 🚀 Quick Start

### Step 1: Start the Server

Open a terminal and run:

```bash
python3 server.py
```

You should see:
```
╔══════════════════════════════════════════════════════════╗
║              HTTP Chat Server Started                    ║
╠══════════════════════════════════════════════════════════╣
║  Server running at: http://localhost:8080                ║
...
```

### Step 2: Connect Clients

You have **two options** to chat:

#### Option A: Web Browser (Recommended)
1. Open your browser
2. Go to: **http://localhost:8080**
3. Enter a username and start chatting!

#### Option B: Command-Line Client
Open a **new terminal** and run:

```bash
python3 client.py
```

Follow the prompts to enter your username and start chatting.

---

## 💬 Using the Command-Line Client

### Available Commands

| Command | Description |
|---------|-------------|
| `/name <username>` | Change your display name |
| `/status` | Check server connection status |
| `/history` | View all messages |
| `/clear` | Clear the terminal screen |
| `/quit` or `/exit` | Exit the client |

### Example Session

```
Enter your username (or press Enter for 'Anonymous'): Alice

👋 Welcome, Alice!

Alice> Hello everyone!
Alice> /status
✅ Server: online
📊 Messages: 1
Alice> /quit

👋 Goodbye!
```

---

## 🌐 API Endpoints

The server exposes these HTTP endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web-based chat interface |
| `GET` | `/messages` | Get all messages (JSON) |
| `GET` | `/messages?since=N` | Get messages after index N |
| `GET` | `/status` | Server status check |
| `POST` | `/send` | Send a new message |

### Example API Usage with cURL

**Send a message:**
```bash
curl -X POST http://localhost:8080/send \
  -H "Content-Type: application/json" \
  -d '{"username": "Bob", "message": "Hello from cURL!"}'
```

**Get all messages:**
```bash
curl http://localhost:8080/messages
```

**Check server status:**
```bash
curl http://localhost:8080/status
```

---

## 🔧 Customization

### Change the Port

Edit `server.py` and modify the `run_server()` call at the bottom:

```python
if __name__ == '__main__':
    run_server(port=3000)  # Change to your preferred port
```

### Connect to a Remote Server

```bash
python3 client.py http://192.168.1.100:8080
```

---

## 📋 Requirements

- **Python 3.6+** (No external packages needed!)
- Works on macOS, Linux, and Windows

---

## 🏗️ Architecture

```
┌─────────────────┐         HTTP         ┌─────────────────┐
│                 │◄────────────────────►│                 │
│  Chat Server    │    GET /messages     │  Web Browser    │
│  (server.py)    │    POST /send        │  (localhost)    │
│                 │                      │                 │
└────────┬────────┘                      └─────────────────┘
         │
         │  HTTP
         │
┌────────▼────────┐
│                 │
│  CLI Client     │
│  (client.py)    │
│                 │
└─────────────────┘
```

---

## ⚠️ Notes

- Messages are stored in memory and will be lost when the server stops
- This is designed for learning purposes, not production use
- The web UI polls for new messages every 2 seconds

---

## 🎉 Have Fun Chatting!

Open multiple terminals or browser tabs to simulate multiple users chatting with each other.
