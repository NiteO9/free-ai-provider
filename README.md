Enter```markdown
# ChatSmith OpenAI Provider

A lightweight OpenAI-compatible API provider that bridges ChatSmith models to the OpenAI Chat Completions interface.

The project allows applications designed for the OpenAI API to communicate with ChatSmith models without requiring modifications to the client. It focuses on compatibility with modern AI applications, coding agents, developer tools, and OpenAI-based SDKs.

---

## Overview

ChatSmith OpenAI Provider acts as a protocol translation layer between ChatSmith and the OpenAI Chat Completions API.

It converts incoming OpenAI requests into ChatSmith requests, processes the responses, and returns OpenAI-compatible responses while preserving features such as streaming, tool calling, and agent workflows.

The goal of the project is to provide a stable compatibility layer rather than simply exposing another chatbot endpoint.

---

## Features

| Feature | Status |
|---------|--------|
| OpenAI Chat Completions API | Supported |
| Streaming Responses (SSE) | Supported |
| Tool Calling | Supported |
| Multiple Tool Calls | Supported |
| Function Calling | Supported |
| Tool Choice | Supported |
| JSON Tool Extraction | Supported |
| Automatic JSON Repair | Supported |
| OpenAI Compatible Response Format | Supported |
| Conversation Context Handling | Supported |
| Session Management | Supported |
| Authentication Layer | Supported |
| Request Validation | Supported |
| Error Handling | Supported |
| Automatic Authentication Refresh | Supported |
| Stateless HTTP API | Supported |
| Low Dependency Design | Supported |
| Production Ready Architecture | Supported |
| Compatible with OpenAI SDKs | Supported |
| Compatible with Coding Agents | Supported |
| REST API | Supported |
| CORS Support | Supported |

---

## Supported Clients

The provider is designed to work with software that supports the OpenAI Chat Completions API.

Examples include:

- Claude Code
- Pi Coding Agent
- Continue
- Cline
- Roo Code
- Aider
- OpenCode
- OpenAI Python SDK
- OpenAI JavaScript SDK
- Any OpenAI-compatible client

---

## Architecture

```

OpenAI Client

ChatSmith OpenAI Provider

Request Translation Layer

Authentication Layer

ChatSmith Backend API

Response Translation Layer

OpenAI Response

```

---

## Request Flow

1. Receive an OpenAI Chat Completions request.
2. Validate the request.
3. Authenticate with ChatSmith.
4. Convert the request into the ChatSmith format.
5. Send the request to the ChatSmith backend.
6. Receive the ChatSmith response.
7. Normalize the response.
8. Convert the response into the OpenAI format.
9. Return the final response to the client.

---

## Tool Calling

The provider supports OpenAI Function Calling / Tool Calling.

Supported capabilities include:

- Tool discovery
- Tool choice
- Single tool execution
- Multiple tool execution
- Tool call identifiers
- JSON argument extraction
- Tool call normalization
- OpenAI-compatible tool responses

---

## Streaming

The provider supports Server-Sent Events (SSE).

Streaming capabilities include:

- Incremental text generation
- Streaming tool calls
- OpenAI chunk format
- Proper finish reasons
- Streaming completion termination

---

## Compatibility

The project is designed to maximize compatibility with existing OpenAI-based tooling.

Supported API endpoints include:

- `GET /health`
- `GET /v1/models`
- `POST /v1/chat/completions`

---

## Technologies

| Technology | Purpose |
|------------|---------|
| Python | Core implementation |
| Flask | HTTP server |
| Requests | Backend communication |
| JSON | Protocol translation |
| Server-Sent Events | Streaming |
| OpenAI Chat Completions API | Client compatibility |

---

## Design Goals

- OpenAI API compatibility
- Clean protocol translation
- Lightweight implementation
- Easy deployment
- Low memory usage
- Extensible architecture
- Reliable streaming
- Robust tool calling
- Production-oriented design
- Minimal external dependencies

---

## Use Cases

- AI Coding Agents
- Local AI Providers
- API Compatibility Layer
- OpenAI SDK Integration
- Custom AI Backends
- Development Tools
- AI IDE Integration
- Automation Systems
- Research Projects
- Experimental Model Gateways

---

## Project Structure

```

.
├── server.py
├── README.md
└── requirements.txt

```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Clone the Repository

```bash
git clone https://github.com/yourusername/chatsmith-openai-provider.git
cd chatsmith-openai-provider
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Requirements File

Create a requirements.txt file with the following content:

```txt
flask==2.3.2
requests==2.31.0
```

Configuration

The provider uses hardcoded configuration values for the ChatSmith backend. If you need to customize the configuration, edit the constants at the top of server.py:

```python
FIREBASE_API_KEY = "your-api-key"
FIREBASE_PROJECT = "your-project"
FIREBASE_APP_ID = "your-app-id"
ANDROID_PACKAGE = "your-package"
ANDROID_CERT = "your-cert"
DEVICE_ID = "your-device-id"
SECRET_KEY = "your-secret-key"
```

Running the Provider

```bash
python server.py
```

The server will start on http://0.0.0.0:8000 by default.

---

Usage

Health Check

```bash
curl http://localhost:8000/health
```

List Models

```bash
curl http://localhost:8000/v1/models
```

Chat Completion

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello"}
    ]
  }'
```

Streaming Chat

```bash
curl -N -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Tell me a story"}
    ],
    "stream": true
  }'
```

Tool Calling

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Write a file called test.txt"}
    ],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "write",
          "description": "Write content to a file",
          "parameters": {
            "type": "object",
            "properties": {
              "path": {"type": "string"},
              "content": {"type": "string"}
            },
            "required": ["path", "content"]
          }
        }
      }
    ]
  }'
```

---

Docker Deployment

Build the Docker Image

```bash
docker build -t chatsmith-provider .
```

Run the Container

```bash
docker run -d -p 8000:8000 chatsmith-provider
```

Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 8000

CMD ["python", "server.py"]
```

---

Deployment Options

Local Development

```bash
python server.py
```

Production Server

Using Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 server:app
```

Using systemd

Create a service file at /etc/systemd/system/chatsmith.service:

```ini
[Unit]
Description=ChatSmith OpenAI Provider
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/project
ExecStart=/usr/bin/python3 /path/to/project/server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable chatsmith
sudo systemctl start chatsmith
```

Using Supervisor

Create a configuration file at /etc/supervisor/conf.d/chatsmith.conf:

```ini
[program:chatsmith]
command=python3 /path/to/project/server.py
directory=/path/to/project
autostart=true
autorestart=true
stderr_logfile=/var/log/chatsmith.err.log
stdout_logfile=/var/log/chatsmith.out.log
```

---

VPS Deployment

Using SSH

1. Copy files to your VPS:

```bash
scp -r . user@your-vps:/opt/chatsmith-provider
```

2. SSH into your VPS:

```bash
ssh user@your-vps
```

3. Install dependencies:

```bash
cd /opt/chatsmith-provider
pip install -r requirements.txt
```

4. Run the server:

```bash
nohup python server.py > logs.txt 2>&1 &
```

---

Integration with AI Tools

Pi Coding Agent

Add to ~/.pi/agent/models.json:

```json
{
  "providers": {
    "chatsmith": {
      "name": "ChatSmith Provider",
      "baseUrl": "http://localhost:8000/v1",
      "api": "openai-completions",
      "apiKey": "none",
      "models": [
        {
          "id": "deepseek-reasoner",
          "name": "ChatSmith (DeepSeek Reasoner)",
          "contextWindow": 32768,
          "maxTokens": 8192,
          "input": ["text"],
          "reasoning": true,
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          }
        }
      ]
    }
  }
}
```

Continue Extension

Add to Continue configuration:

```json
{
  "models": [
    {
      "title": "ChatSmith",
      "provider": "openai",
      "model": "deepseek-reasoner",
      "apiBase": "http://localhost:8000/v1",
      "apiKey": "none"
    }
  ]
}
```

OpenAI SDK

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="none"
)

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)
```

---

Testing

Run Tests

```bash
curl http://localhost:8000/health
curl http://localhost:8000/v1/models
curl -X POST http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

Test Streaming

```bash
curl -N -X POST http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"messages": [{"role": "user", "content": "Hello"}], "stream": true}'
```

Test Tool Calling

```bash
curl -X POST http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"messages": [{"role": "user", "content": "Write a file"}], "tools": [{"type": "function", "function": {"name": "write", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}}}}]}'
```

---

API Reference

Endpoints

GET /health

Returns the health status of the provider.

Response:

```json
{
  "status": "healthy",
  "provider": "chatsmith",
  "model": "deepseek-reasoner",
  "streaming": true,
  "tools": true
}
```

GET /v1/models

Returns the list of available models.

Response:

```json
{
  "object": "list",
  "data": [
    {
      "id": "deepseek-reasoner",
      "object": "model",
      "created": 1234567890,
      "owned_by": "chatsmith"
    }
  ]
}
```

POST /v1/chat/completions

Creates a chat completion.

Request Body:

```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello"}
  ],
  "stream": false,
  "tools": [],
  "tool_choice": "auto"
}
```

Response:

```json
{
  "id": "chatcmpl-1234567890",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "deepseek-reasoner",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 10,
    "total_tokens": 10
  }
}
```

---

Troubleshooting

Common Issues

ModuleNotFoundError: No module named 'flask'

```bash
pip install flask
```

ModuleNotFoundError: No module named 'requests'

```bash
pip install requests
```

Port 8000 Already in Use

```bash
# Find the process using port 8000
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>

# Or use a different port
python server.py --port 8001
```

Connection Refused

Ensure the server is running:

```bash
curl http://localhost:8000/health
```

Authentication Failed

Check the Firebase and ChatSmith credentials in the configuration section of server.py.

---

License

This project is provided as-is for educational, research, and interoperability purposes.

The software is not affiliated with or endorsed by OpenAI, ChatSmith, Firebase, or Google.

All trademarks and registered trademarks are the property of their respective owners.

The project is intended solely for testing and interoperability with third-party services.

Users are solely responsible for compliance with applicable terms of service.

No warranty, express or implied, is provided for any purpose.

Use at your own risk.

---

Contributing

Contributions are welcome. Please open an issue or submit a pull request on GitHub.

Guidelines:

· Keep the code clean and minimal
· Maintain compatibility with OpenAI API
· Document new features
· Test thoroughly before submitting
· Follow the existing code style

---

Authors

Maintained by the ChatSmith OpenAI Provider community.

---

Disclaimer

This project is an independent open-source project and is not affiliated with, endorsed by, or sponsored by OpenAI, ChatSmith, or Google.

The provider is designed for interoperability and educational purposes only.

Users are responsible for ensuring compliance with all applicable terms of service, laws, and regulations.

The provider does not guarantee compatibility, stability, or performance.

Use of this software is at your own risk.

---

Acknowledgments

· OpenAI for the Chat Completions API specification
· ChatSmith for the backend services
· The open-source community for their contributions
· Pi Coding Agent for testing and validation
· All contributors and users of this project

```
